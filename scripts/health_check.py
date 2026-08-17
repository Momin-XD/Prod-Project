import argparse
import sys
import time
import requests

def run_health_check(target_url, max_retries=10, delay_seconds=3):
    print(f"[*] Initiating health check on: {target_url}")
    for attempt in range(1, max_retries + 1):
        try:
            start_time = time.time()
            response = requests.get(target_url, timeout=5)
            latency = round((time.time() - start_time) * 1000, 2)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    print(f"[SUCCESS] Health check passed on attempt {attempt}/{max_retries}")
                    print(f"    - Response Code : {response.status_code}")
                    print(f"    - Latency       : {latency} ms")
                    return 0
            print(f"[WARNING] Attempt {attempt}: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[RETRY] Attempt {attempt}/{max_retries} failed: {str(e)}")
        time.sleep(delay_seconds)
    print(f"[ERROR] Health check failed after {max_retries} attempts.")
    return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    sys.exit(run_health_check(target_url=args.url))
