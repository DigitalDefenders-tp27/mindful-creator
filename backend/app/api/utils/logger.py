import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name, level=logging.INFO):
    """
    Set up a logger with the specified name and level.
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
        
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if logs directory exists
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        try:
            os.mkdir(logs_dir)
        except Exception:
            pass
    
    if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
        file_handler = RotatingFileHandler(
            f"{logs_dir}/{name}.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger 