# src/utils/logger.py
import logging
import sys
import structlog

def get_logger(name: str):
    # Route standard Python logs (from web3, etc.) through our custom formatter
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            # Add log level (INFO, ERROR)
            structlog.stdlib.add_log_level,
            # Add the name of the file generating the log
            structlog.stdlib.add_logger_name,
            # Keep the timestamp short and readable
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            # The magic formatter
            structlog.dev.ConsoleRenderer(
                colors=True,
                pad_event=50,  # <-- This aligns all your variables into a neat right column
                sort_keys=True # Keeps variable output order predictable
            )
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger(name)
