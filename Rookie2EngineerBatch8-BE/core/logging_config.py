import logging
import sys
from typing import Any, Dict
from core.config import get_settings

def setup_logging(
    level: int = get_settings().LOG_LEVEL,
    format: str = get_settings().LOG_FORMAT,
    config: Dict[str, Any] | None = None
) -> None:
    """
    Setup logging configuration for the entire application.
    
    Args:
        level: The logging level (default: INFO)
        format: The log message format (default: timestamp - logger - level - message)
        config: Optional custom logging configuration dictionary
    """
    default_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': format
            },
        },
        'handlers': {
            'console': {
                'level': level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': sys.stdout
            },
            'file': {
                'level': level,
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'loggers': {
            '': {  # Root logger
                'handlers': ['console', 'file'],
                'level': level,
                'propagate': True
            },
            'uvicorn': {
                'handlers': ['console', 'file'],
                'level': level,
                'propagate': False
            },
            'fastapi': {
                'handlers': ['console', 'file'],
                'level': level,
                'propagate': False
            }
        }
    }
    
    from logging.config import dictConfig
    dictConfig(config or default_config)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.
    
    Args:
        name: The name of the logger (typically __name__)
    
    Returns:
        logging.Logger: A configured logger instance
    """
    return logging.getLogger(name) 