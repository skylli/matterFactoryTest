def string_to_hex(input_string):
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

# Example usage
input_string = "!@#9527sky"
hex_result = string_to_hex(input_string)
print(f"Hexadecimal representation: {hex_result}")
