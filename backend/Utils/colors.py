# utils/color.py

RESET = "\033[0m"

COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bold": "\033[1m",
    "underline": "\033[4m",
}

def color_text(text, *styles):
    combined = ''.join(styles)
    return f"{combined}{text}{RESET}"

def cprint(text, *styles):
    print(color_text(text, *styles))
