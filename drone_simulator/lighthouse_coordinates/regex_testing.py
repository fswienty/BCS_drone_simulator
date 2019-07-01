import os
import sys
import re


with open(os.path.join(sys.path[0], "bs_position.txt"), encoding="utf-8") as f:
    text = f.read()

match = re.search(r'-?\d', "drone45-434")
if match:
    print(match.group())

match = re.findall(r'\+?-?\d+', "drone45-43+4654-6567+8")
print(match)