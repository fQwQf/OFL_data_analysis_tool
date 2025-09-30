LOG_DIRECTORY = "../FAFI_ICML25/logs"
OUTPUT_DIRECTORY = "./analysed_logs"

EXTRACT_CLIENT_ACCURACY = False

CONFIG_KEYS_TO_EXTRACT = [
    'exp_name',
    'algorithm',
    'aggregation_method',
    'server.model_name',
    'server.lr',
    'server.local_epochs',
    'lambda_align_initial'
]