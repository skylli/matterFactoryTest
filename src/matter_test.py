import subprocess
import re
import logging, os
from logger import logger as log
class MatterTester:

    def __init__(self, qrcode, chip_tool , ssid, pwd) -> None:
        self.chip_tool = chip_tool
        self.qrcode = qrcode
        self.ssid ="hex:" +  self.string_to_hex( ssid)
        self.pwd = "hex:" +  self.string_to_hex(pwd)
        self.node_id = "0x07"

    def string_to_hex(self, input_string):
        """
        Convert a string to its hexadecimal ASCII representation.
        
        Args:
        - input_string (str): The input string to convert.
        
        Returns:
        - str: The hexadecimal ASCII representation of the input string.
        """
        # Convert each character to its hexadecimal representation and join them together
        hex_output = ''.join(format(ord(char), '02x') for char in input_string)
        return hex_output

    def parse_qrcode(self, qrcode):
        """Parse the QR code using the specified shell command and extract long_discriminator and passcode."""
        cmd =self.chip_tool + " payload parse-setup-payload " + qrcode
        log.debug("shell : " + str(cmd))
        try:
            # Execute the shell command
            result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Extracting the relevant values from the command output
            output = result.stdout
            
            # Using regular expressions to find the required values
            long_discriminator_match = re.search(r"CHIP:SPL: Long discriminator:\s+(\d+)", output)
            passcode_match = re.search(r"CHIP:SPL: Passcode:\s+(\d+)", output)
            
            if long_discriminator_match and passcode_match:
                self.long_discriminator = int(long_discriminator_match.group(1))
                self.passcode = int(passcode_match.group(1))
                
                # Print the extracted values
                print(f"Long discriminator: {self.long_discriminator}")
                print(f"Passcode: {self.passcode}")
                return True
            else:
                print("Failed to extract required values from the command output.")
                return False
        
        except subprocess.CalledProcessError as e:
            # Print the error output if the command fails
            print(f"Shell command failed with error: {e.stderr}")
            return False

    def execute_shell_command(self, cmd, debug=True):
        """
        Execute a shell command and handle the output based on the debug flag.
        
        Args:
        - cmd (str): The shell command to execute.
        - debug (bool): If True, prints the command's output to the terminal.
        
        Returns:
        - bool: True if the command executed successfully (exit code 0), False otherwise.
        """
        try:
            # Execute the shell command
            result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Print the command's output if debug is True
            if debug:
                print("Command Output:\n", result.stdout)
            
            print("Execution successful")
            return True

        except subprocess.CalledProcessError as e:
            # Print the error output if the command fails
            print("Command failed with error:\n", e.stderr)
            return False
        # Example usage
        # qrcode = "MT:WUXK5GAN16UEPW0PO10"
        # parse_qrcode(qrcode)
    def pairing(self) -> bool:
        if False == self.parse_qrcode(self.qrcode):
            print("非法 qrcode !!")
            return False
        cmd = self.chip_tool + "  pairing ble-wifi  " + str(self.node_id) + " "
        cmd += self.ssid + " " + self.pwd + " "
        cmd += str(self.passcode) + " " + str(self.long_discriminator)
        cmd += " --bypass-attestation-verifier true"
        log.debug("shell cmd: " + str(cmd))
        if False == self.execute_shell_command( cmd  ):
            print("蓝牙配网失败 !!!")
            return False
        return True
    
    def onoff(self, on=True):
        onoff = ' on ' if on == True else ' off '
        cmd = self.chip_tool + " onoff " + onoff + str(self.node_id) + ' 1 '
        log.debug("shell cmd: " + str(cmd))
        if False == self.execute_shell_command( cmd  ):
            print("onff 失败 !!!")
            return False
        return True

    def factory_rest(self):
        
        cmd = self.chip_tool + " pairing  unpair " +  str(self.node_id) 
        log.debug("shell cmd: " + str(cmd))
        self.execute_shell_command( cmd  )
        os.system('rm -rf /tmp/chip_*')
        return True
    
#1. get code
#2. connect.
#3. get info
#4. control
#5. reset.
#6. remove.
if __name__ == "__main__":
    mdev = MatterTester("MT:WUXK5GAN16UEPW0PO10", 
                        "/home/sky/data/prj/matter/sdk/connectedhomeip/out/debug/standalone/chip-tool",
                        "sky", "!@#9527sky")
    # ret = mdev.pairing()
    # if True == ret:
    # print("pairing: ", ret)
        # mdev.onoff(False)
        # mdev.onoff(True)
    ret = mdev.factory_rest()
    print(ret)