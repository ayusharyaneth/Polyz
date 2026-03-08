# src/utils/logger.py
import logging
import sys
import warnings
import structlog

# Globally mute unclosed session memory warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

def get_logger(name: str):
    # Gag all the noisy 3rd-party libraries so they only report fatal crashes
    for noisy_module in ["httpx", "httpcore", "aiohttp", "web3", "urllib3", "asyncio"]:
        logging.getLogger(noisy_module).setLevel(logging.CRITICAL)

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.dev.ConsoleRenderer(colors=True)
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger()
