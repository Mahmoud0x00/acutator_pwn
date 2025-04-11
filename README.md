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
   pip3 install -r requirements.txt
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


## 🖼️ Example Output

```bash
$ python3 actuator_pwn.py https://example.com/actuator/httptrace

  
 █████   ██████ ████████ ██    ██  █████  ████████  ██████  ██████  ██████  ██     ██ ███    ██ 
██   ██ ██         ██    ██    ██ ██   ██    ██    ██    ██ ██   ██ ██   ██ ██     ██ ████   ██ 
███████ ██         ██    ██    ██ ███████    ██    ██    ██ ██████  ██████  ██  █  ██ ██ ██  ██ 
██   ██ ██         ██    ██    ██ ██   ██    ██    ██    ██ ██   ██ ██      ██ ███ ██ ██  ██ ██ 
██   ██  ██████    ██     ██████  ██   ██    ██     ██████  ██   ██ ██       ███ ███  ██   ████                                                                                                                                                                
        
          Actuator PWN v1.0
          by @mahmoud0x00
        
        
[+] Saving requests to: Output/requests_20250411141905_bnzjh4.json
```

## 📂 Output Directory

All output files (JSON or SQLite database) are saved in the `Output` directory for better organization.

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🤝 Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue to improve this project.

## 📧 Contact

If you have any questions or feedback, please reach out to [@mahmoud0x00](https://x.com/mahmoud0x00).
