# Pykd script to find the IAT (Import Address Table)'s VMA for the specified module in WinDbg
#
# Example: 
# 1. Assuming that, for example, this script is located in C:\find_iat.py
# 2. First, load the pykd extension in WinDbg:          .load pykd
# 3. Use the script to find the VMA for ntdll's IAT:    !py C:\find_iat.py ntdll 

import sys
import pykd

def find_iat_x64(module_name):
    try:
        # Get the DllBase of the module
        module = pykd.module(module_name)
        dll_base = module.begin()
        
        # Find the offset of IMAGE_NT_HEADERS
        e_lfanew = pykd.ptrDWord(dll_base + 0x3C)
        nt_headers = dll_base + e_lfanew
        
        # Get the offset of the Optional Header
        optional_header = nt_headers + 0x18
        
        # The DataDirectory array starts at offset 0x70 from the Optional Header
        data_directory = optional_header + 0x70
        
        # The IMAGE_DATA_DIRECTORY of the IAT is entry 12 (offset 0x60)
        iat_entry = data_directory + 0x60
        
        # Read the RVA of the IAT
        iat_rva = pykd.ptrDWord(iat_entry)
        
        # Calculate the VMA of the IAT
        iat_vma = dll_base + iat_rva
        
        print(f"IAT VMA of {module_name}: {iat_vma:#x}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: !py find_iat_x64.py <module_name>")
    else:
        find_iat_x64(sys.argv[1])
