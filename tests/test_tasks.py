import contextlib
import csv
from io import StringIO
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


class TasksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name) / "project"
        shutil.copytree(ROOT, self.folder,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "tests"))
        self.previous_directory = Path.cwd()
        os.chdir(self.folder)
        self.addCleanup(self.temp.cleanup)
        self.addCleanup(os.chdir, self.previous_directory)

    def run_task(self, number, answers=()):
        output = StringIO()
        with contextlib.redirect_stdout(output), patch("builtins.input", side_effect=answers):
            data = runpy.run_path(str(self.folder / f"task{number}.py"))
        return data, output.getvalue()

    def run_process(self, number, answers=""):
        result = subprocess.run(
            [sys.executable, f"task{number}.py"], input=answers,
            text=True, encoding="utf-8", capture_output=True, timeout=10,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def fixture(self, source, destination):
        shutil.copyfile(self.folder / "test_data" / source, destination)

    def test_all_25_programs_start(self):
        answers = {7: "sample_directory\n.py\n", 9: "12.5\n"}
        for number in range(1, 26):
            with self.subTest(task=number):
                self.run_process(number, answers.get(number, ""))

    def test_text_statistics(self):
        data, _ = self.run_task(1)
        self.assertEqual([data[key] for key in (
            "line_counter", "word_counter", "symbol_counter", "max_length_line")],
            [4, 7, 50, 18])

    def test_empty_spaces_and_no_final_newline(self):
        for source, expected in [("empty.txt", [0, 0, 0, 0]),
                                 ("spaces.txt", [3, 0, 6, 3])]:
            with self.subTest(source=source):
                self.fixture(source, "text.txt")
                data, _ = self.run_task(1)
                self.assertEqual([data[key] for key in (
                    "line_counter", "word_counter", "symbol_counter", "max_length_line")], expected)
        Path("text.txt").write_text("first\nlast", encoding="utf-8")
        data, _ = self.run_task(1)
        self.assertEqual(data["line_counter"], 2)
        self.assertEqual(data["symbol_counter"], 10)

    def test_number_statistics_and_bad_lines(self):
        self.run_task(2)
        self.assertEqual(Path("result.txt").read_text(encoding="utf-8"),
                         "Среднее арифметическое: 10.0\nМинимальное значение: -5\nМаксимальное значение: 25\n")
        for source in ["empty.txt", "numbers_invalid.txt"]:
            self.fixture(source, "numbers.txt")
            self.run_task(2)
            self.assertEqual(Path("result.txt").read_text(encoding="utf-8"), "НЕТ КОРРЕКТНЫХ ЧИСЕЛ")

    def test_student_csv(self):
        data, _ = self.run_task(3)
        self.assertEqual(data["max_score_name"], "David")
        self.assertAlmostEqual(data["mean_score"], 86.8)
        self.assertAlmostEqual(data["groups"]["101"]["average_score"], 248 / 3)
        self.assertEqual(data["groups"]["102"]["average_score"], 93)

    def test_student_csv_empty_and_zero_scores(self):
        Path("students.csv").write_text("name,group,score\n\nZero,101,0\n", encoding="utf-8")
        data, _ = self.run_task(3)
        self.assertEqual(data["max_score_name"], "Zero")
        for content in ["", "name,group,score\n"]:
            Path("students.csv").write_text(content, encoding="utf-8")
            _, output = self.run_task(3)
            self.assertIn("Нет данных", output)

    def test_product_csv_and_preserved_header(self):
        self.run_task(4)
        with open("expensive.csv", encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual([row["name"] for row in rows], ["Laptop", "Chair", "Table", "Lamp"])
        Path("text.csv").write_text("price,name,category,stock\n100,No,test,1\n100.01,Yes,test,2\n", encoding="utf-8")
        self.run_task(4)
        with open("expensive.csv", encoding="utf-8", newline="") as stream:
            rows = list(csv.reader(stream))
        self.assertEqual(rows, [["price", "name", "category", "stock"], ["100.01", "Yes", "test", "2"]])

    def test_student_json(self):
        _, output = self.run_task(5)
        data = json.loads(Path("new_text.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data), 5)
        self.assertEqual([row["passed"] for row in data], [True, True, True, True, False])
        self.assertTrue(all(type(row["passed"]) is bool for row in data))
        self.assertIn("Alice", output)
        Path("students.json").write_text("[]", encoding="utf-8")
        self.run_task(5)
        self.assertEqual(json.loads(Path("new_text.json").read_text(encoding="utf-8")), [])

    def test_directory_statistics(self):
        data, _ = self.run_task(6)
        self.assertEqual(data["counter_files"], 2)
        self.assertEqual(data["counter_directory"], 2)
        self.assertEqual([path.name for path in data["py_files"]], ["main.py"])
        self.assertEqual(data["total_size_files"],
                         Path("sample_directory/main.py").stat().st_size +
                         Path("sample_directory/notes.txt").stat().st_size)

    def test_recursive_search_both_extension_formats(self):
        for extension in ["py", ".py"]:
            data, output = self.run_task(7, ["sample_directory", extension])
            self.assertEqual({row["path"].name for row in data["extension_files"]}, {"main.py", "helper.py"})
            self.assertIn("helper.py", output)
            self.assertTrue(all(row["size"] > 0 for row in data["extension_files"]))
        _, output = self.run_task(7, ["sample_directory", ".missing"])
        self.assertIn("Файлы не найдены", output)
        self.assertIn("Указан неверный путь", self.run_process(7, "missing_directory\n").stdout)
        self.assertIn("Указан неверный путь", self.run_process(7, "data.txt\n").stdout)

    def test_safe_read_and_real_failures(self):
        module, _ = self.run_task(8)
        read_file = module["read_file"]
        self.assertEqual(read_file("data.txt"), "first\nsecond\nthird\n")
        self.assertEqual(read_file("test_data/empty.txt"), "")
        for path, messages in [("missing.txt", ("Файл не найден",)),
                               ("sample_directory", ("каталог", "Недостаточно прав")),
                               ("data.txt/child", ("не является каталогом", "Файл не найден")),
                               ("test_data/invalid_utf8.bin", ("Ошибка декодировки",))]:
            with self.subTest(path=path), contextlib.redirect_stdout(StringIO()) as output:
                self.assertIsNone(read_file(path))
                self.assertTrue(any(message in output.getvalue() for message in messages))

    def test_read_permission_and_os_errors(self):
        module, _ = self.run_task(8)
        for error, message in [(PermissionError("denied"), "Недостаточно прав"),
                               (IsADirectoryError("directory"), "Это каталог"),
                               (NotADirectoryError("not directory"), "не является каталогом"),
                               (OSError("I/O error"), "Ошибка операционной системы")]:
            with patch("builtins.open", side_effect=error), contextlib.redirect_stdout(StringIO()) as output:
                self.assertIsNone(module["read_file"]("data.txt"))
                self.assertIn(message, output.getvalue())

    def test_parse_number(self):
        module, _ = self.run_task(9, ["12.5"])
        self.assertEqual(module["parse_number"](" -2.5 "), -2.5)
        with self.assertRaises(ValueError):
            module["parse_number"]("abc")
        _, output = self.run_task(9, ["abc"])
        self.assertIn("ValueError", output)

    def test_bank_exception_hierarchy(self):
        module, _ = self.run_task(10)
        self.assertEqual(module["withdraw"](100, 30), 70)
        self.assertEqual(module["withdraw"](100, 100), 0)
        for amount in [0, -1]:
            with self.assertRaises(module["InvalidAmountError"]):
                module["withdraw"](100, amount)
        with self.assertRaises(module["InsufficientFundsError"]):
            module["withdraw"](100, 101)
        for name in ["InvalidAmountError", "InsufficientFundsError", "AccountBlockedError"]:
            self.assertTrue(issubclass(module[name], module["BankError"]))

    def test_user_ids_not_timestamp_numbers(self):
        data, _ = self.run_task(11)
        self.assertEqual(data["id_users"], ["123", "456", "123", "789", "456"])
        self.assertEqual(data["error_id_users"], ["456", "789"])
        self.assertEqual(len(data["error_str"]), 2)
        Path("logs.txt").write_text("2026-09-23 ERROR User 42 failed 3 times\n", encoding="utf-8")
        data, _ = self.run_task(11)
        self.assertEqual(data["id_users"], ["42"])
        self.assertEqual(data["error_id_users"], ["42"])

    def test_unique_email_addresses(self):
        data, _ = self.run_task(12)
        self.assertEqual(data["emails"], ["alice@example.com", "bob@test.org", "admin@company.ru", "first.last+tag@mail.example.org"])

    def test_both_timers_preserve_exception(self):
        module, output = self.run_task(13)
        self.assertEqual(output.count("Время выполнения:"), 2)
        for context in [module["Timer"](), module["timer"]()]:
            with contextlib.redirect_stdout(StringIO()) as output:
                with self.assertRaisesRegex(RuntimeError, "test error"):
                    with context:
                        raise RuntimeError("test error")
                self.assertIn("Время выполнения:", output.getvalue())

    def test_log_success_and_exception_propagation(self):
        module, _ = self.run_task(14)
        with module["log_operation"]("operation.log", "Success"):
            pass
        with self.assertRaisesRegex(ValueError, "broken"):
            with module["log_operation"]("operation.log", "Failure"):
                raise ValueError("broken")
        self.assertEqual(Path("operation.log").read_text(encoding="utf-8"),
                         "START: Success\nEND: Success\nSTART: Failure\nERROR: Failure\n")

    def test_file_like_objects(self):
        module, _ = self.run_task(15)
        count_lines = module["count_lines"]
        with open("data.txt", encoding="utf-8") as stream:
            self.assertEqual(count_lines(stream), 3)
            self.assertEqual(count_lines(stream), 0)
        self.assertEqual(count_lines(StringIO("first\nsecond\nthird")), 3)
        self.assertEqual(count_lines(StringIO("")), 0)
        self.assertEqual(count_lines(StringIO("\n\n")), 2)

    def test_log_levels(self):
        data, _ = self.run_task(16)
        self.assertEqual([data[key] for key in ("info_counter", "warning_counter", "error_counter")], [3, 1, 2])
        self.assertEqual(data["users_error"], ["456", "789"])

    def test_large_file_statistics(self):
        data, _ = self.run_task(17)
        self.assertEqual([data[key] for key in ("total", "min_value", "max_value", "count", "mean_value")], [50, -5, 25, 5, 10])
        for source in ["empty.txt", "numbers_invalid.txt"]:
            self.fixture(source, "task17.txt")
            _, output = self.run_task(17)
            self.assertIn("Нет корректных чисел", output)

    def access_stats(self):
        self.run_process(18)
        return json.loads(Path("statstask18.json").read_text(encoding="utf-8"))

    def test_access_log_all_methods_and_4xx(self):
        data = self.access_stats()
        self.assertEqual(data["REQUESTS_BY_METHOD"], {"GET": 4, "POST": 1, "PUT": 1, "DELETE": 1})
        self.assertEqual(data["GET_requests"], 4)
        self.assertEqual(data["POST_requests"], 1)
        self.assertEqual(data["4xx_ERRORS"], 3)
        self.assertEqual(data["MOST_POPULAR_URL"], "/login")
        log = Path("loggingtask18.log").read_text(encoding="utf-8")
        self.assertIn("END READING FILE", log)
        self.assertIn("WARNING", log)
        self.assertIn("JSON written", log)

    def test_access_log_empty_malformed_and_missing(self):
        for content in ["", "broken\n", "2026-09-23 10:00:01 1.2.3.4 GET /bad 1404\n"]:
            Path("access.log").write_text(content, encoding="utf-8")
            data = self.access_stats()
            self.assertEqual(data["REQUESTS_BY_METHOD"], {})
            self.assertEqual(data["4xx_ERRORS"], 0)
            self.assertIsNone(data["MOST_POPULAR_URL"])
        Path("statstask18.json").unlink()
        Path("access.log").unlink()
        self.run_process(18)
        self.assertFalse(Path("statstask18.json").exists())
        self.assertIn("File not found", Path("loggingtask18.log").read_text(encoding="utf-8"))

    def test_access_log_decode_error(self):
        self.fixture("invalid_utf8.bin", "access.log")
        self.run_process(18)
        self.assertFalse(Path("statstask18.json").exists())
        self.assertIn("File not readable", Path("loggingtask18.log").read_text(encoding="utf-8"))

    def test_phone_formats(self):
        data, _ = self.run_task(19)
        self.assertEqual(data["numbers"], ["+7 999 123-45-67", "8 999 123-45-67", "+7 (999) 123-45-67", "8 (999) 123-45-67"])

    def test_exact_date_format(self):
        data, _ = self.run_task(20)
        self.assertEqual(data["date_list"], ["15.09.2026", "21.09.2026", "03.10.2026"])
        Path("task20.txt").write_text("115.09.2026 15.09.20266 1.11.2026 03.10.2026", encoding="utf-8")
        data, _ = self.run_task(20)
        self.assertEqual(data["date_list"], ["03.10.2026"])

    def test_login_boundaries(self):
        module, _ = self.run_task(21)
        for login, valid in [("user_123", True), ("admin", True), ("abcd", True),
                             ("a" * 16, True), ("123user", False), ("ab", False),
                             ("user-name", False), ("a" * 17, False), ("Aяasd", False),
                             ("abcd\n", False), ("", False)]:
            with self.subTest(login=login), contextlib.redirect_stdout(StringIO()):
                self.assertIs(module["is_valid_login"](login), valid)

    def test_urls(self):
        data, _ = self.run_task(22)
        self.assertEqual(data["https_list"], ["https://python.org", "http://example.com/page", "https://example.com/docs/index.html"])

    def test_space_normalization(self):
        _, output = self.run_task(23)
        self.assertEqual(output.splitlines(), ["Это строка с большим количеством пробелов.", "Текст с пробелами"])

    def test_whole_product_identifier(self):
        path = Path("task24.py")
        source = path.read_text(encoding="utf-8")
        path.write_text(source.replace('"PRD-54321"', '"PRD-54321", "xPRD-12345", "PRD-123456", "PRD-12345x"'), encoding="utf-8")
        data, _ = self.run_task(24)
        self.assertEqual(data["good_products"], ["PRD-12345", "PRD-00123", "PRD-54321"])

    def test_named_log_groups(self):
        data, _ = self.run_task(25)
        self.assertEqual(len(data["logs_done"]), 5)
        self.assertEqual(data["logs_done"][1], {
            "datetime": "2026-09-24 10:16:04", "level": "ERROR",
            "user_id": "456", "message": "authentication failed"})


if __name__ == "__main__":
    unittest.main()
