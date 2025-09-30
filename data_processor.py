import numpy as np

def process_rounds_data(all_rounds_data, mode, num_samples=10, max_round=None):
    """
    根据模式筛选轮次数据
    :param all_rounds_data: 包含所有轮次指标的列表
    :param mode: 'all' 或 'sampled'
    :param num_samples: 在 'sampled' 模式下要选取的样本数
    :param max_round: 采样的最大轮次上限
    :return: 筛选后的数据列表
    """
    # 步骤1: 如果设置了最大轮次，先过滤数据
    if max_round is not None:
        filtered_data = [r for r in all_rounds_data if r.get('round', -1) <= max_round]
    else:
        filtered_data = all_rounds_data
    
    # 步骤2: 根据模式进行处理
    if mode == 'all':
        return filtered_data
    
    elif mode == 'sampled':
        total_rounds = len(filtered_data)
        if total_rounds <= num_samples:
            return filtered_data
        
        indices = np.linspace(0, total_rounds - 1, num_samples, dtype=int)
        indices[0] = 0
        indices[-1] = total_rounds - 1
        
        sampled_data = [filtered_data[i] for i in np.unique(indices)]
        return sampled_data
        
    else:
        print("警告: 无效的模式，将返回所有数据。")
        return filtered_data