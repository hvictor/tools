# Input:    arbitrary string
# Output:   Sequence of push operations to store the string on the stack
# 
# WARNING:  This script does not avoid null bytes in the code pushing the last QWORD. 
#           You will have to avoid it by using a specific null-byte avoidance technique.
#           Example:    1. Determine the negated value of the QWORD containing NULL bytes.
#                       2. mov rax, <negated QWORD>; neg rax; push rax;
# WARNING:  If the string length is a multiple of 8 bytes, the pushed string will not
#           contain any null bytes. You will have to push a zero QWORD to terminate the string.

import sys

def string_to_qwords(input_string):
    # Add zero-padding to make the length a multiple of 8 bytes.
    padding_length = (8 - len(input_string) % 8) % 8
    padded_string = input_string + '\0' * padding_length

    # Split the string into chunks of 8 bytes
    chunks = [padded_string[i:i+8] for i in range(0, len(padded_string), 8)]

    # Initialize the list of QWORDs, initially empty
    qwords = []

    # For every 8-byte chunk of the input string,
    # build the corresponding QWORD in little-endian format
    for chunk in chunks:
        # 1. Convert the characters to ASCII codes
        # 2. Reverse their order to obtain the little-endian ordering
        # 3. Format the bytes as QWORD
        qword = ''.join(f'{ord(c):02x}' for c in reversed(chunk))

        # Add the QWORD to the list
        qwords.append((qword, chunk))

    return qwords

def main():
    # If no input string is provided, show the Usage message
    if len(sys.argv) != 2:
        print("Usage: python string_to_qwords.py <string>")
        sys.exit(1)

    # Extract the input string from the arguments
    input_string = sys.argv[1]

    # Generate the corresponding list of QWORDs
    qwords = string_to_qwords(input_string)

    # Print the PUSH instructions to construct the string
    # onto the stack
    print("QWORDs to push to construct the string in memory:")
    for qword, chunk in reversed(qwords):
        print(f"push 0x{qword.upper()} = {repr(chunk)} (reversed)")

if __name__ == "__main__":
    main()