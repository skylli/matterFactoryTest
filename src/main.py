import json
import time
import sys, tty, termios, logging
import threading
from devices import onoff_test
from logger import logger as log 

# Global variable to store input characters
input_chars = ""
old_settings = None
std_fd = None
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
    global input_chars, old_settings, std_fd
    input_chars = ''
    last_input_time = time.time()

    std_fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(std_fd)
    tty.setraw(sys.stdin.fileno())
    while True:
        char = sys.stdin.read(1)
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
        time.sleep(0.003)  # Slight sleep to avoid high CPU usage

def main_handle(thread, conf):
    global input_chars, input_chars_lock
    global old_settings, std_fd
    last_length = 0
    last_change_time = time.time()

    try:
        while True:
            time.sleep(0.007)  # Slight sleep to avoid high CPU usage
            with input_chars_lock:
                current_length = len(input_chars)
            current_time = time.time()

            if current_length != last_length:
                last_length = current_length
                last_change_time = current_time
            elif current_time - last_change_time >= 0.5:
                if current_length > 0:
                    qrcode = None
                    with input_chars_lock:
                        qrcode = input_chars
                        print(input_chars)
                        input_chars = ""
                    if qrcode is not None:
                        onoff_test(qrcode, conf)
                        # termios.tcsetattr(std_fd, termios.TCSADRAIN, old_settings)
                        # tty.setraw(sys.stdin.fileno())
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

    log.setLevel(logging.DEBUG)
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
