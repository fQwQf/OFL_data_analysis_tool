import os
import csv
import config

def save_to_csv(data, config_summary, original_filename):
    """将提取的配置和数据保存到CSV文件。"""
    writable_data = [row.copy() for row in data]

    if not writable_data and config_summary:
        writable_data = [config_summary]
    elif writable_data and config_summary:
        for row in writable_data:
            row.update(config_summary)

    if not writable_data:
        print("没有可供保存的数据。")
        return

    os.makedirs(config.OUTPUT_DIRECTORY, exist_ok=True)
    
    base_name = os.path.basename(original_filename)
    output_filename = f"summary_{base_name.replace('.log', '.csv')}"
    output_path = os.path.join(config.OUTPUT_DIRECTORY, output_filename)

    headers = set()
    for row in writable_data:
        headers.update(row.keys())
    
    sorted_headers = sorted(config.CONFIG_KEYS_TO_EXTRACT)
    other_headers = sorted(list(headers - set(sorted_headers)))
    if 'round' in other_headers:
        other_headers.insert(0, other_headers.pop(other_headers.index('round')))
    
    final_headers = sorted_headers + other_headers

    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=final_headers, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(writable_data)
        print(f"\n关键信息已成功保存至: {output_path}")
    except IOError as e:
        print(f"错误: 无法写入文件 {output_path}。原因: {e}")