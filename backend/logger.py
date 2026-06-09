import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Common Date-wise Logger
date_str = datetime.now().strftime("%Y-%m-%d")
common_logger = logging.getLogger("common")
common_logger.setLevel(logging.INFO)
if not common_logger.handlers:
    fh = logging.FileHandler(os.path.join(LOG_DIR, f"app_{date_str}.log"))
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    common_logger.addHandler(fh)

def get_user_logger(interview_id: str, candidate_name: str):
    safe_name = "".join([c for c in candidate_name if c.isalpha() or c.isdigit() or c == ' ']).strip().replace(' ', '_')
    logger = logging.getLogger(f"user_{interview_id}")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(os.path.join(LOG_DIR, f"user_{safe_name}_{interview_id[:8]}.log"))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
