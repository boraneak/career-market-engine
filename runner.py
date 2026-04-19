import ingester
import parser
import warehouse


def main():
    # 1. Fetch
    text = ingester.run_ingester()
    if not text:
        return

    # 2. Parse
    jobs = parser.parse_markdown_to_jobs(text)
    if not jobs:
        return

    # 3. Store
    warehouse.update_warehouse(jobs)


if __name__ == "__main__":
    main()
