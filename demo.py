def print_red_bold_with_crossmark(text):
    # ANSI escape sequence for green color and bold
    RED_BOLD = "\033[1;31m"
    # ANSI escape sequence to reset color and style
    RESET = "\033[0m"
    # Unicode character for crossmark
    CROSSMARK = "\u2716"
    print(f"{RED_BOLD}{text} {CROSSMARK}{RESET}")

# Example usage
print_red_bold_with_crossmark("This is a green bold message with a crossmark")
