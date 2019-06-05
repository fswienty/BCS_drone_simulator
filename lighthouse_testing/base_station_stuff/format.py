import os
import sys
import re


with open(os.path.join(sys.path[0], "bs_position.txt"), encoding="utf-8") as f:
    text = f.read()

match = re.findall(r'-?\d.\d+', text)
numberList = [float(i) for i in match]
print(numberList[0:3])
print([numberList[3:6], numberList[6:9], numberList[9:12]])
print(numberList[12:15])
print([numberList[15:18], numberList[18:21], numberList[21:24]])    


# bs1 = LighthouseBsGeometry()
# bs1.origin = [2.248076915740967, 2.6118149757385254, 1.7803560495376587]
# bs1.rotation_matrix = [[0.5808780193328857, -0.43165698647499084, 0.690110981464386], [-0.014093000441789627, 0.8423519730567932, 0.5387439727783203], [-0.81386798620224, -0.32267001271247864, 0.48322099447250366]]
#
# bs2 = LighthouseBsGeometry()
# bs2.origin = [-2.594325065612793, 2.966259002685547, -1.4438459873199463]
# bs2.rotation_matrix = [[-0.4975239932537079, 0.47656500339508057, -0.7248139977455139], [-0.0567610003054142, 0.8158929944038391, 0.5754110217094421], [0.8655909895896912, 0.32742199301719666, -0.3788749873638153]]