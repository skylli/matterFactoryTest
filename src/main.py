import json
import time
import sys, readchar, logging
import threading
from devices import onoff_test
from logger import logger as log 

# Global variable to store input characters
input_chars = ""
# Lock for thread-safe access to input_chars
input_chars_lock = threading.Lock()
def read_config(file_path):
    """Read the JSON config file and return the content."""
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
            return config
    except Exception as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)

def qrcode_scan_thread():
    # Step 3: Continuously read keyboard input and process accordingly
    global input_chars
    input_chars = ''
    last_input_time = time.time()

    while True:
        char = readchar.readkey() # User input, but not displayed on the screen
        current_time = time.time()
        if char is None:
            time.sleep(0.1)
        else:
            with input_chars_lock:
                if current_time - last_input_time < 5:
                    input_chars += char
                    # print("add: " + input_chars)
                else:
                    # print("dump: " + input_chars)
                    input_chars = ''
                    input_chars += char
            last_input_time = time.time()
        # time.sleep(0.0001)  # Slight sleep to avoid high CPU usage

def main_handle(thread, conf):
    global input_chars, input_chars_lock
    last_length = 0
    last_change_time = time.time()
    print("开始测试 " + conf.get("device_name") +  " 设备...")
    try:
        while True:
            time.sleep(0.1)  # Slight sleep to avoid high CPU usage
            # with input_chars_lock:
            current_length = len(input_chars)
            current_time = time.time()

            if current_length != last_length:
                last_length = current_length
                last_change_time = current_time
                
            if (current_time - last_change_time) >= 0.5:
                if current_length > 0:
                    qrcode = None
                    with input_chars_lock:
                        qrcode = input_chars
                        input_chars = ""
                    if qrcode is not None:
                        print("qrcode=", qrcode)
                        onoff_test(qrcode, conf)
                        print("继续测试 " + conf.get("device_name") +  " 设备...")
                    last_length = 0  # Reset last_length after clearing input_chars

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        thread.join()

def main():
    # Step 1: Read the config.json file from the terminal input
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_config.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    config = read_config(config_path)

    if config.get("debug"):
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    # Step 2: Extract and print device_name from the config
    device_name = config.get('device_name')
    # ssid =  config.get('ssid')
    # password =config.get('password')
    # chip_tool = config.get('chip_tool')
    if not device_name:
        print("Error: 'device_name' not found in config file")
        sys.exit(1)
    
    print(f"Device Name: {device_name}")
    # Start the writer thread
    thread = threading.Thread(target=qrcode_scan_thread)
    thread.daemon = True
    thread.start()

    main_handle(thread, config)

if __name__ == "__main__":
    main()
