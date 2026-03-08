# src/utils/logger.py
import logging
import structlog
from rich.logging import RichHandler

def get_logger(name: str):
    # Set up Rich to hijack standard Python logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            RichHandler(
                rich_tracebacks=True,       # Draws beautiful UI boxes around errors
                tracebacks_show_locals=True,# Shows variable states when an error happens
                show_path=False,            # Hides file paths to keep the console wide and clean
                markup=True
            )
        ]
    )

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            # structlog's dev renderer plays incredibly nicely with Rich
            structlog.dev.ConsoleRenderer(
                colors=True,
                force_colors=True,
            )
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger(name)
