import os
from datetime import datetime
import config

def find_log_files(start_time_str, end_time_str):
    """根据精确到分钟的时间范围查找日志文件"""
    found_files = []
    try:
        # 解析包含分钟的输入时间
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d-%H-%M')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d-%H-%M')
    except ValueError:
        print(f"错误: 时间格式 '{start_time_str}' 或 '{end_time_str}' 不正确。请使用 YYYY-MM-DD-HH-MM 格式。")
        return []

    if not os.path.exists(config.LOG_DIRECTORY):
        print(f"错误: 日志目录 '{config.LOG_DIRECTORY}' 不存在。")
        return []

    for filename in os.listdir(config.LOG_DIRECTORY):
        if filename.endswith('.log'):
            try:
                # 文件名包含秒，所以解析格式不同
                file_time = datetime.strptime(filename.split('.')[0], '%Y%m%d_%H%M%S')
                if start_time <= file_time <= end_time:
                    found_files.append(os.path.join(config.LOG_DIRECTORY, filename))
            except ValueError:
                continue
    
    return found_files