import sqlite3
import config


def update_warehouse(job_list):
    """Saves a list of job dictionaries directly to the database."""
    if not job_list:
        print("[!] No jobs provided to warehouse.")
        return

    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
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
    for d in job_list:
        try:
            skills = ", ".join(d.get("skills_list", []))
            cursor.execute(
                """
                INSERT OR IGNORE INTO global_jobs (job_id, title, company, location, link, skills)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    str(d.get("job_id")),
                    d.get("job_title"),
                    d.get("company"),
                    d.get("location"),
                    d.get("application_link"),
                    skills,
                ),
            )
            if cursor.rowcount > 0:
                count += 1
        except Exception as e:
            print(f"  [!] Database Error: {e}")

    conn.commit()
    conn.close()
    print(f"[✓] Warehouse Updated: {count} new records added.")


if __name__ == "__main__":
    # For local testing only
    test_jobs = [{"job_id": "test", "job_title": "DevOps", "company": "CME"}]
    update_warehouse(test_jobs)
