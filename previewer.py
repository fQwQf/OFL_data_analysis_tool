def display_preview(data, config_summary):
    """在终端中以表格形式显示配置和数据预览。"""
    try:
        from tabulate import tabulate
    except ImportError:
        print("\n提示: 请运行 'pip install tabulate' 以获得更好的表格预览效果。")
        _simple_preview(data, config_summary)
        return

    # 1. 显示配置摘要
    if config_summary:
        print("\n--- Experiment Configuration Summary ---")
        config_table = [[k, v] for k, v in config_summary.items()]
        print(tabulate(config_table, headers=["Parameter", "Value"], tablefmt="grid"))

    # 2. 显示轮次数据
    if not data:
        print("\n没有轮次数据可供预览。")
        return
    
    headers = set()
    for row in data:
        headers.update(row.keys())
    
    sorted_headers = sorted(list(headers))
    if 'round' in sorted_headers:
        sorted_headers.insert(0, sorted_headers.pop(sorted_headers.index('round')))
        
    table_data = [{h: row.get(h, 'N/A') for h in sorted_headers} for row in data]

    print("\n--- Round Metrics Preview ---")
    print(tabulate(table_data, headers="keys", tablefmt="grid", numalign="right"))

def _simple_preview(data, config_summary):
    if config_summary:
        print("\n--- Experiment Configuration Summary ---")
        for k, v in config_summary.items():
            print(f"{k}: {v}")
    
    if not data:
        print("\n没有轮次数据可供预览。")
        return

    print("\n--- Round Metrics Preview (Simple) ---")
    headers = data[0].keys()
    print(" | ".join(headers))
    for row in data:
        print(" | ".join(str(row.get(h, 'N/A')) for h in headers))