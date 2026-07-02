import re

def clean_url(text):
    if not text:
        return ""

    # Example:
    # [https://abc.com](https://abc.com)

    if "(" in text and ")" in text:
        return text.split("(")[1].split(")")[0]

    return text