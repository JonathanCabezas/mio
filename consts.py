import re


#
# Colors
#

COLOR_CODES = {"RESET": "\033[0m", "BOLD": "\033[1m"}

COLORS = ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE"]
for i in range(8):
    COLOR_CODES[COLORS[i]] = "\033[3%dm" % i

SUCCESS = "SUCCESS"
FAILURE = "FAILURE"

SUCCESS_KEYWORDS = ["succes", "reussi"]

FAILURE_KEYWORDS = ["fail", "rate", "echec"]

#
# Regular Expressions
#

BRACES_PATTERN = re.compile(r"(.*?)({.*?})([^{]*)")

#
# Dates
#

DEFAULT_DATE_FORMAT = "[%a, %d %b %Y %H:%M:%S]"
CUSTOM_ASCTIME = "custom_asctime"

#
# Indentation
#

"""
In Unicode

There are a variety of Unicode bullet characters from Wikipedia page:

    U+2022 • BULLET (&bull;, &bullet;)
    U+2023 ‣ TRIANGULAR BULLET
    U+2043 ⁃ HYPHEN BULLET (&hybull;)
    U+25CB ○ WHITE CIRCLE (&cir;)
    U+25CF ● BLACK CIRCLE
    U+25E6 ◦ WHITE BULLET

Fallbacks characters: https://github.com/sindresorhus/figures
"""

BULLET_CHARACTERS = ["•", "►", "⁃"]
INDENTATION = "  "
