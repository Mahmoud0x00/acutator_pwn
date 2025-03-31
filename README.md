# 🚀 Actuator PWN

Actuator PWN is a tool designed to fetch and monitor data from the `/actuator/httptrace` endpoint. It validates the URL, ensures the response matches the expected `traces[]` format, and saves the output in either JSON or SQLite database format. The tool also provides options to control the refresh rate and runtime duration.

## 📋 Requirements

Ensure you have Python installed on your system. Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

## 🛠️ Usage

1. Clone the repository or download the source code:
   ```bash
   git clone https://github.com/your-username/actuator-fetcher.git
   cd actuator-fetcher
   ```

2. Run the script with the following command:
   ```bash
   python src/actuator_pwn.py <url> [--interval <seconds>] [--save <json|db>] [--filename <name>] [--runtime <duration>]
   ```

### Example Commands:
- Save data to a JSON file every 5 seconds for 10 minutes:
  ```bash
  python src/actuator_pwn.py http://example.com/actuator/httptrace --interval 5 --save json --runtime "10 minutes"
  ```

- Save data to an SQLite database indefinitely:
  ```bash
  python src/actuator_pwn.py http://example.com/actuator/httptrace --save db
  ```

## ✨ Features

- **Dynamic Fetching**: Fetches data from the `/actuator/httptrace` endpoint at user-defined intervals.
- **Flexible Saving Options**: Save data in either JSON format or an SQLite database.
- **Runtime Control**: Specify how long the script should run using natural language (e.g., "10 minutes", "2 hours").


## 🖼️ Example Output

```
                 _                  _                _____ __          __ _   _ 
     /\         | |                | |              |  __ \\ \        / /| \ | |
    /  \    ___ | |_  _   _   __ _ | |_  ___   _ __ | |__) |\ \  /\  / / |  \| |
   / /\ \  / __|| __|| | | | / _` || __|/ _ \ | '__||  ___/  \ \/  \/ /  | . ` |
  / ____ \| (__ | |_ | |_| || (_| || |_| (_) || |   | |       \  /\  /   | |\  |
 /_/    \_\\___| \__| \__,_| \__,_| \__|\___/ |_|   |_|        \/  \/    |_| \_|

[+] Saving requests to: Output/requests_20250331123456.json
[+] Request URI: http://example.com/api/resource?key=value
[+] Request URI: http://example.com/api/resource?token=123
[!] Runtime completed. Stopping the script.
```

## 📂 Output Directory

All output files (JSON or SQLite database) are saved in the `Output` directory for better organization.

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🤝 Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to improve this project.

## 📧 Contact

For any inquiries or feedback, reach out to [@mahmoud0x00](https://x.com/mahmoud0x00).