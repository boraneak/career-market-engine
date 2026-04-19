import requests
import config


def run_ingester():
    print(f"[*] Fetching latest roles from SimplifyJobs GitHub...")
    try:
        response = requests.get(config.GITHUB_URL, timeout=15)
        if response.status_code == 200:
            print(f"[✓] Data fetched successfully ({len(response.text)} characters)")
            return response.text
        else:
            print(f"[!] HTTP Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"[!] Ingest Error: {e}")
        return None


if __name__ == "__main__":
    data = run_ingester()
    if data:
        print(f"Captured {len(data)} characters in memory.")
