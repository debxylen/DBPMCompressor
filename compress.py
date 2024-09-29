from DBPM import *
import argparse
from os import system
parser = argparse.ArgumentParser()
parser.add_argument('-i','--infile')
file = parser.parse_args().infile

system(f"copy {file} temp1_{file}")
system(f"precomp.exe temp1_{file}")
system(f"del temp1_{file}")

f = open(f"temp1_{'.'.join(file.split('.')[:-1])}.pcf","rb")
input_data = f.read()
f.close()
system(f"del temp1_{'.'.join(file.split('.')[:-1])}.pcf")

# Compress the data
compressed_data, huffman_codes = huffman_compress(input_data+b"[0DBPM_COMPRESSOR_END0]")

f = open(f"{file}.dbpm","wb")
f.write(compressed_data)
f.close()

f = open(f"{file}.dbpmhuff","w")
f.write(str(huffman_codes))
f.close()

system(f"copy {file}.dbpmhuff temp{file}.dbpmhuff")
system(f"precomp temp{file}.dbpmhuff")
system(f"del {file}.dbpmhuff")
system(f"del temp{file}.dbpmhuff")
system(f"rename temp{file}.pcf {file}.dbpmhuff")

print(f"Original Size: {len(input_data)} bytes")
print(f"Compressed Size: {len(compressed_data)} bytes")

