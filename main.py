import os
from log_finder import find_log_files
from log_parser import LogParser
from data_processor import process_rounds_data
from output_writer import save_to_csv
from previewer import display_preview

def get_user_input():
    print("--- 机器学习日志关键信息提取脚本 ---")
    start_time = input("请输入开始时间 (格式 YYYY-MM-DD-HH-MM): ")
    end_time = input("请输入结束时间 (格式 YYYY-MM-DD-HH-MM, 若与开始相同可直接回车): ")
    if not end_time:
        end_time = start_time
    while True:
        mode = input("请选择提取模式 ('all' 或 'sampled'): ").lower()
        if mode in ['all', 'sampled']:
            break
        print("无效输入，请输入 'all' 或 'sampled'。")
    num_samples = 10
    max_round = None
    if mode == 'sampled':
        try:
            max_round_str = input("请输入采样的最大轮次上限 (可选, 直接回车则不限制): ")
            if max_round_str:
                max_round = int(max_round_str)
            num_samples_str = input(f"请输入抽样数量 (默认 {num_samples}): ")
            if num_samples_str:
                num_samples = int(num_samples_str)
        except ValueError:
            print(f"输入无效，将使用默认值。")
    preview = input("是否在终端预览结果? (y/n, 默认 n): ").lower() == 'y'
    return start_time, end_time, mode, num_samples, max_round, preview

def main():
    start_time, end_time, mode, num_samples, max_round, preview = get_user_input()
    log_files = find_log_files(start_time, end_time)

    if not log_files:
        print("\n在指定时间范围内未找到任何日志文件。")
        return

    print(f"\n找到 {len(log_files)} 个匹配的日志文件，正在处理...")

    for log_file in log_files:
        print("\n" + "="*40)
        print(f"正在解析: {os.path.basename(log_file)}")
        
        parser = LogParser(log_file)
        parser.parse()
        
        config_summary = parser.get_config_summary()
        all_rounds_data = parser.key_metrics_per_round

        if not all_rounds_data and not config_summary:
            print("未能从此文件中提取任何有效数据。")
            continue
            
        print(f"共解析出 {parser.get_total_rounds()} 轮的数据。")
        
        final_data = process_rounds_data(all_rounds_data, mode, num_samples, max_round)
        
        if preview:
            display_preview(final_data, config_summary)

        save_to_csv(final_data, config_summary, log_file)
        
    print("\n所有文件处理完毕！")

if __name__ == "__main__":
    main()