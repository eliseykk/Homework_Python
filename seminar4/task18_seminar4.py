import re
from collections import Counter
import json
import logging

logging.basicConfig(
    filename = "loggingtask18.log",
    filemode = "a",
    encoding = "utf-8",
    level=logging.INFO)
def read_file():
    try:
        with open("access.log", "r", encoding="utf-8") as file:
            logging.info(f"START READING FILE")
            read = []
            pattern = (
                r"^[0-9]{4}-[0-9]{2}-[0-9]{2}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}\s+"
                r"([0-9]{1,3}(?:\.[0-9]{1,3}){3})"
                r"\s+([A-Z]+)"
                r"\s+(/\S*)"
                r"\s+([0-9]{3})\s*$"
            )
            for line in file:
                logging.info(f"Processing line: {line}")
                request = re.findall(pattern, line)
                if request:
                    read.extend(request)
                else:
                    logging.warning(f"Incorrect line: {line.rstrip()}")
            logging.info(f"END READING FILE")
    except FileNotFoundError:
        logging.error(f"File not found")
        return None
    except (OSError, UnicodeDecodeError):
        logging.error(f"File not readable")
        return None
    return read
read = read_file()
if read is not None:
    get_counter = 0
    post_counter = 0
    error4xx_counter = 0
    most_popular_URL = ""
    method_counter = Counter()
    for request in read:
        method_counter[request[1]] += 1
        match request[1]:
            case 'GET':
                get_counter += 1
            case 'POST':
                post_counter += 1
        if re.fullmatch(r"4[0-9]{2}", request[3]):
            error4xx_counter += 1

    URL_list = [read[i][2] for i in range(len(read))]
    URL_counter = Counter(URL_list)
    most_popular_URL = URL_counter.most_common(1)[0][0] if URL_counter else None

    format_json = {"GET_requests": get_counter, "POST_requests": post_counter, "REQUESTS_BY_METHOD": dict(method_counter), "MOST_POPULAR_URL": most_popular_URL, "4xx_ERRORS": error4xx_counter}
    try:
        with open("statstask18.json", "w", encoding="utf-8") as file:
            json.dump(format_json, file)
    except OSError:
        logging.error(f"JSON cannot be written")
    else:
        logging.info(f"JSON written")

