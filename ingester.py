import requests
import config
from logger import logger
from typing import Optional


def run_ingester() -> Optional[str]:
    """
    Fetches job listings from SimplifyJobs GitHub repository.
    
    Returns:
        str: Raw markdown content if successful, None otherwise
    """
    logger.info(f"Fetching latest roles from SimplifyJobs GitHub...")
    try:
        response = requests.get(config.GITHUB_URL, timeout=15)
        if response.status_code == 200:
            logger.info(f"Data fetched successfully ({len(response.text)} characters)")
            return response.text
        else:
            logger.error(f"HTTP Error: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        logger.error(f"Request timeout while fetching from {config.GITHUB_URL}")
        return None
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during ingestion: {e}", exc_info=True)
        return None


if __name__ == "__main__":
    data = run_ingester()
    if data:
        logger.info(f"Successfully captured {len(data)} characters")
    else:
        logger.error("Failed to ingest data")
