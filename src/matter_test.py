import subprocess
import re
import logging, os
from logger import logger as log
from logger import print_red_bold
class MatterTester:

    def __init__(self, qrcode, chip_tool , ssid, pwd) -> None:
        self.chip_tool = chip_tool
        self.qrcode = qrcode
        self.ssid ="hex:" +  self.string_to_hex( ssid)
        self.pwd = "hex:" +  self.string_to_hex(pwd)
        self.node_id = "0x07"
        self.manual_code = ''

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
            qr_version_match = re.search(r"CHIP:SPL: Version:\s+(\d+)", output)
            long_discriminator_match = re.search(r"CHIP:SPL: Long discriminator:\s+(\d+)", output)
            passcode_match = re.search(r"CHIP:SPL: Passcode:\s+(\d+)", output)
            
            if long_discriminator_match and passcode_match:
                self.qr_version = int(qr_version_match.group(1))
                self.long_discriminator = int(long_discriminator_match.group(1))
                self.passcode = int(passcode_match.group(1))
                
                # Print the extracted values
                print(f"version: {self.qr_version} Long discriminator: {self.long_discriminator} Passcode: {self.passcode}")
                return True
            else:
                print("Failed to extract required values from the command output.")
                return False
        
        except subprocess.CalledProcessError as e:
            # Print the error output if the command fails
            print(f"Shell command failed with error: {e.stderr}")
            return False
    def get_manual_code(self, shellcmd):
        try:
            # Execute the shell command
            result = subprocess.run(shellcmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Extract the output from stdout
            output = result.stdout
            
            # Search for the manual code in the output
            for line in output.splitlines():
                if "CHIP:TOO: Manual Code:" in line:
                    # Extract and return the manual code value
                    manual_code =  line.split("CHIP:TOO: Manual Code:")[1].strip()
                    if len(manual_code) != 11:
                        return None
                    
                    # Format the manual code as required
                    formatted_code = f"{manual_code[:4]}-{manual_code[4:7]}-{manual_code[7:]}"
                    # print(f"Manual Code: {formatted_code}" )
                    return formatted_code

            # If the manual code is not found, return None
            return None
        except subprocess.CalledProcessError:
            # If the command fails, return None
            return None
    
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
    def pairing(self, debug=False) -> bool:
        if False == self.parse_qrcode(self.qrcode):
            print("非法 qrcode !!")
            return False
        # get manual 
        cmd = self.chip_tool + " payload generate-manualcode "
        cmd += " --discriminator " + str(self.long_discriminator )
        cmd += " --setup-pin-code " + str(self.passcode )
        cmd += " --version " + str(self.qr_version )
        cmd += " --commissioning-mode 0 "
        log.debug("shell cmd: " + str(cmd))
        manual_code = self.get_manual_code(cmd)
        if manual_code:
            self.manual_code = manual_code
            print_red_bold("Manual Code: " + str(manual_code))
        
        cmd = self.chip_tool + "  pairing ble-wifi  " + str(self.node_id) + " "
        cmd += self.ssid + " " + self.pwd + " "
        cmd += str(self.passcode) + " " + str(self.long_discriminator)
        cmd += " --bypass-attestation-verifier true"
        log.debug("shell cmd: " + str(cmd))
        if False == self.execute_shell_command( cmd , debug ):
            print("蓝牙配网失败 !!!")
            return False
        return True
    
    def onoff(self, on=True, debug=False):
        onoff = ' on ' if on == True else ' off '
        cmd = self.chip_tool + " onoff " + onoff + str(self.node_id) + ' 1 '
        log.debug("shell cmd: " + str(cmd))
        if False == self.execute_shell_command( cmd, debug):
            print("onff 失败 !!!")
            return False
        return True

    def factory_rest(self, debug=False):
        
        cmd = self.chip_tool + " pairing  unpair " +  str(self.node_id) 
        log.debug("shell cmd: " + str(cmd))
        self.execute_shell_command( cmd, debug)
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
    ret = mdev.pairing()
    # if True == ret:
    # print("pairing: ", ret)
        # mdev.onoff(False)
        # mdev.onoff(True)
    # ret = mdev.factory_rest()
    # print(ret)