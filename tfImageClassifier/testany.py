#  for test
import subprocess
from os import path, curdir

ROOT_DIR = path.abspath(curdir).replace("\\", "/")

proc = subprocess.Popen(['python', "scripts/label_image.py ",
                         "--graph=outputModel/retrained_graph.pb ",
                         "--labels=outputModel/retrained_labels.txt ",
                         "--input_layer=Placeholder ",
                         "--output_layer=final_result ",
                         "--image=testData/image1.png"],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

print(proc.communicate()[0])
