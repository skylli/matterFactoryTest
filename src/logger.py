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