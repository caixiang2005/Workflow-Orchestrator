import logging
import sys

def setup_logging():
    """配置全局日志格式和输出处理器"""
    # 创建根 Logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # 控制台处理器（默认输出到终端）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # 文件处理器（可选，生产环境可开启）
    # file_handler = logging.FileHandler("app.log", encoding="utf-8")
    # file_handler.setLevel(logging.INFO)

    # 统一的格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    # file_handler.setFormatter(formatter)

    # 添加到根日志器
    root_logger.addHandler(console_handler)
    # root_logger.addHandler(file_handler)