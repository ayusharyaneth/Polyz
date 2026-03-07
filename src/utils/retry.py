# src/utils/retry.py
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from src.utils.logger import get_logger
import aiohttp
import asyncpg

logger = get_logger(__name__)

def log_attempt_failed(retry_state):
    logger.warning(f"Retrying: {retry_state.fn.__name__} after exception: {retry_state.outcome.exception()}")

network_retry = retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((aiohttp.ClientError, asyncpg.PostgresError, TimeoutError)),
    after=log_attempt_failed
)
