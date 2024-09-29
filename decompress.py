from DBPM import *
import argparse
from os import system
parser = argparse.ArgumentParser()
parser.add_argument('-i','--infile')

file = parser.parse_args().infile
f = open(f"{file}","rb")
todecompress = f.read()
f.close()
system(f"precomp -r {file}huff")
f = open(f"temp{file}huff","r")
tohuffman = eval(f.read())
f.close()
system(f"del temp{file}huff")

# Decompress the data
decompressed_data = remove_marker_with_corruption(huffman_decompress(todecompress, tohuffman))
f = open(f"out_{file.replace('.dbpm','')}","wb")
f.write(decompressed_data)
f.close()
system(f"precomp.exe -r out_{file.replace('.dbpm','')}")
system(f"del out_{file.replace('.dbpm','')}")
system(f"rename temp1_{file.replace('.dbpm','')} out_{file.replace('.dbpm','')}")
