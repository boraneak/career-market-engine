import ingester
import parser
import warehouse
from logger import logger


def main():
    """
    Orchestrates the full ETL pipeline:
    1. Fetch job listings (Ingester)
    2. Parse with AI (Parser)
    3. Store in database (Warehouse)
    """
    logger.info("=" * 60)
    logger.info("Starting Career Market Engine Pipeline")
    logger.info("=" * 60)
    
    try:
        # 1. Fetch
        text = ingester.run_ingester()
        if not text:
            logger.error("Pipeline failed: Ingester returned no data")
            return False

        # 2. Parse
        jobs = parser.parse_markdown_to_jobs(text)
        if not jobs:
            logger.warning("Pipeline warning: Parser returned 0 jobs")
            return False

        # 3. Store
        warehouse.update_warehouse(jobs)
        
        logger.info("=" * 60)
        logger.info("Pipeline completed successfully")
        logger.info("=" * 60)
        return True
        
    except Exception as e:
        logger.error(f"Pipeline failed with exception: {e}", exc_info=True)
        logger.error("=" * 60)
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
