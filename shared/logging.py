import json

def log_info(message, data=None):
    """
    Simple logger that accepts a message and optional data.
    """
    if data is not None:
        print(f"{message}: {json.dumps(data)}")
    else:
        print(message)