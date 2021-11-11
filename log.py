from enum import Enum

# Log enum class
class Log(Enum):
    LOG = 0
    WARN = 1
    ERR = 2

def log(log_type: Log, log_message: str):
    """
        ### log
        prints log message\n\n
        args:
            * log_type: int - 0 if simple LOG, 1 if warning and 2 if error
            * log_message: str - log message to print
    """
    msg = ""
    if log_type == Log.LOG:
        msg = f"[LOG] {log_message}\n"
    elif log_type == Log.WARN:
        msg = f"[WARNING] {log_message}\n"
    elif log_type == Log.ERR:
        msg = f"[ERROR] {log_message}\n"
    
    print(msg)