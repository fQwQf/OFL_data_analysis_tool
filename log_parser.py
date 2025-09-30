import re
import ast
import config

class LogParser:
    """解析单个日志文件以提取关键信息。"""
    def __init__(self, filepath):
        self.filepath = filepath
        self.full_config = None
        self.extracted_config_summary = {}
        self.key_metrics_per_round = []
        self._content = self._read_file()

    def _read_file(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return f.readlines()
        except FileNotFoundError:
            return None
    
    def _get_nested_key(self, data_dict, key_path):
        """安全地使用点分割路径从嵌套字典中检索值。"""
        keys = key_path.split('.')
        val = data_dict
        for key in keys:
            if isinstance(val, dict) and key in val:
                val = val[key]
            else:
                return 'N/A'
        return val

    def parse(self):
        """执行完整的解析操作。"""
        if self._content is None:
            print(f"无法读取文件: {self.filepath}")
            return
        
        self._parse_full_config()
        self._extract_config_summary()
        self._parse_algorithm()
        self._parse_aggregation_method()
        self._parse_rounds()

    def _parse_full_config(self):
        """解析完整的实验配置字典。"""
        for line in self._content:
            match = re.search(r"\[INFO\]\s+config: (\{.*\})", line)
            if match:
                try:
                    self.full_config = ast.literal_eval(match.group(1))
                    return
                except (ValueError, SyntaxError):
                    print(f"警告: 无法解析文件 {self.filepath} 中的配置信息。")
        self.full_config = {}

    def _extract_config_summary(self):
        """根据 config.py 中的设置提取关键配置项。"""
        if not self.full_config:
            return
        
        special_keys = {'algorithm', 'aggregation_method'}
        
        for key_path in config.CONFIG_KEYS_TO_EXTRACT:
            if key_path in special_keys:
                continue
            value = self._get_nested_key(self.full_config, key_path)
            self.extracted_config_summary[key_path] = value

    def _parse_algorithm(self):
        """从特定的日志行中解析算法名称。"""
        for line in self._content[:30]:
            match = re.search(r"\[INFO\]\s+(OneshotOurs.*)", line)
            if match:
                self.extracted_config_summary['algorithm'] = match.group(1).strip()
                return
        if 'algorithm' in config.CONFIG_KEYS_TO_EXTRACT:
            self.extracted_config_summary.setdefault('algorithm', 'N/A')

    def _parse_aggregation_method(self):
        """解析服务端使用的聚合方法（例如 IFFI）。"""
        # 示例: [INFO]  V7 Training | Using ADVANCED IFFI server aggregation.
        for line in self._content:
            match = re.search(r"Using (.*) server aggregation", line)
            if match:
                method = match.group(1).strip()
                self.extracted_config_summary['aggregation_method'] = method
                return
        
        if 'aggregation_method' in config.CONFIG_KEYS_TO_EXTRACT:
            self.extracted_config_summary.setdefault('aggregation_method', 'N/A')

    def _parse_rounds(self):
        """解析每一轮的关键指标。"""
        current_round_data = {}
        client_accuracies = {}

        for line in self._content:
            line = line.strip()

            if config.EXTRACT_CLIENT_ACCURACY:
                client_match = re.search(r"Epoch \d+ .* test accuracy: ([\d.]+)", line)
                if "Starts Local Trainning" in line:
                     client_id_match = re.search(r"Client (\d+)", line)
                     if client_id_match:
                         current_client_id = f"client_{client_id_match.group(1)}_acc"
                elif client_match and 'current_client_id' in locals():
                    client_accuracies[current_client_id] = float(client_match.group(1))

            round_start_match = re.search(r"Round (\d+) starts", line)
            if round_start_match:
                if current_round_data:
                    self.key_metrics_per_round.append(current_round_data)
                round_num = int(round_start_match.group(1))
                current_round_data = {"round": round_num}
                client_accuracies = {}

            variance_match = re.search(r"Model variance: mean: ([\d.eE+-]+)", line)
            if variance_match:
                current_round_data["model_variance_mean"] = float(variance_match.group(1))

            protos_std_match = re.search(r"g_protos_std: ([\d.]+)", line)
            if protos_std_match:
                current_round_data["g_protos_std"] = float(protos_std_match.group(1))
            
            global_acc_match = re.search(r"The test accuracy \(with prototype\) of .*: ([\d.]+)", line)
            if global_acc_match:
                current_round_data["global_test_accuracy"] = float(global_acc_match.group(1))
                if config.EXTRACT_CLIENT_ACCURACY:
                    current_round_data.update(client_accuracies)

        if current_round_data and "global_test_accuracy" in current_round_data:
            self.key_metrics_per_round.append(current_round_data)

    def get_config_summary(self):
        return self.extracted_config_summary

    def get_total_rounds(self):
        return len(self.key_metrics_per_round)