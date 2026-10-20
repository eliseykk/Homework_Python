import re
text = "Полезные сайты: https://python.org, http://example.com/page, https://example.com/docs/index.html и ftp://files.example.com/data."
https_list = re.findall(r"https?://[^\s,]+", text)
print(https_list)