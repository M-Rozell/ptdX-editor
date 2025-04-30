# Colors for console output

RESET = "\033[0m"

COLORS = {
    "red": "\033[31m",
    "blue": "\033[34m",
    "cyan": "\033[36m",
    "green": "\033[32m",
    "white": "\033[37m",
    "yellow": "\033[33m",
    "magenta": "\033[35m",   
    "bold": "\033[1m",
    "underline": "\033[4m",
}

def color_text(text, *styles):
    combined = ''.join(styles)
    return f"{combined}{text}{RESET}"

def cprint(text, *styles):
    print(color_text(text, *styles))
