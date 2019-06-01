#  for test

os.system("scripts/label_image.py --graph=outputModel/retrained_graph.pb --labels=outputModel/retrained_labels.txt --input_layer=Placeholder --output_layer=final_result --image=testData/image1.png")