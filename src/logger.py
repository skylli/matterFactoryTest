import logging
import sys

# 创建logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # 设置logger的默认级别

# 创建控制台处理器并设置级别为DEBUG
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.DEBUG)

# 创建格式器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 给处理器设置格式器
console_handler.setFormatter(formatter)

# 给logger添加处理器
logger.addHandler(console_handler)

def set_log_level(level):
    logger.setLevel(level)
    
    
def print_red_bold(text):
    # ANSI escape sequence for red color and bold
    RED_BOLD = "\033[1;31m"
    # ANSI escape sequence to reset color and style
    RESET = "\033[0m"
    print(f"{RED_BOLD}{text}{RESET}")


def print_green_bold_with_checkmark(text):
    # ANSI escape sequence for green color and bold
    GREEN_BOLD = "\033[1;32m"
    # ANSI escape sequence to reset color and style
    RESET = "\033[0m"
    # Unicode character for checkmark
    CHECKMARK = "\u2713"
    print(f"{GREEN_BOLD}{text} {CHECKMARK}{RESET}")
    
def print_red_bold_with_crossmark(text):
    # ANSI escape sequence for green color and bold
    RED_BOLD = "\033[1;31m"
    # ANSI escape sequence to reset color and style
    RESET = "\033[0m"
    # Unicode character for crossmark
    CROSSMARK = "\u2716"
    print(f"{RED_BOLD}{text} {CROSSMARK}{RESET}")