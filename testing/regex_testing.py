import os
import sys
import re



match = re.search(r'-?\d', "drone45-434")
if match:
    print(match.group())

match = re.findall(r'-?\d+', "drone45-43+4654-6567+8")
print(match)
