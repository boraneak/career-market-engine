import sqlite3
import config
from logger import logger
from typing import List, Dict, Any


def update_warehouse(job_list: List[Dict[str, Any]]) -> None:
    """
    Saves a list of job dictionaries to SQLite database with deduplication.
    
    Args:
        job_list: List of job dictionaries from parser
    """
    if not job_list:
        logger.warning("No jobs provided to warehouse")
        return

    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        
        logger.info(f"Creating/connecting to database: {config.DB_PATH}")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS global_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT UNIQUE,
                title TEXT,
                company TEXT,
                location TEXT,
                link TEXT,
                skills TEXT
            )
        """)

        count = 0
        duplicates = 0
        
        for job in job_list:
            try:
                skills = ", ".join(job.get("skills_list", []))
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO global_jobs (job_id, title, company, location, link, skills)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        str(job.get("job_id")),
                        job.get("job_title"),
                        job.get("company"),
                        job.get("location"),
                        job.get("application_link"),
                        skills,
                    ),
                )
                
                if cursor.rowcount > 0:
                    count += 1
                else:
                    duplicates += 1
                    
            except Exception as e:
                logger.error(f"Database error inserting job {job.get('job_id')}: {e}", exc_info=True)

        conn.commit()
        conn.close()
        
        logger.info(f"Warehouse updated: {count} new records, {duplicates} duplicates skipped")

    except sqlite3.OperationalError as e:
        logger.error(f"Database operational error: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Unexpected error updating warehouse: {e}", exc_info=True)


if __name__ == "__main__":
    # For local testing only
    test_jobs = [{"job_id": "test", "job_title": "DevOps", "company": "CME", "location": "Remote", "application_link": "http://example.com", "skills_list": ["Python"]}]
    update_warehouse(test_jobs)
