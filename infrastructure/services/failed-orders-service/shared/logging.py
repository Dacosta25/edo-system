import json

def log_info(message, data=None):
    if data is not None:
        print(f"{message}: {json.dumps(data)}")
    else:
        print(message)
