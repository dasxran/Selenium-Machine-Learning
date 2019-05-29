import docker
from time import sleep
client = docker.from_env()

container = client.containers.run(
    'dasxran/tensorflow:trainimages',
    'python /image_classifier/scripts/return_pct.py --graph=/image_classifier/outputModel/retrained_graph.pb '
    '--labels=/image_classifier/outputModel/retrained_labels.txt --input_layer=Placeholder '
    '--output_layer=final_result --image=/image_classifier/testData/image1.png --lookfor=magnifyingglass',
    detach=False, auto_remove=False, remove=True, tty=True, stdin_open=True, volumes={
        'C:/Users/user/PycharmProjects/seleniumMachineLearning/tfImageClassifier': {
            'bind': '/image_classifier',
            'mode': 'rw',
        }
    })

#  detach=False mode
print(float(container.decode().split('\r\n')[-2]))

#  detach=True mode
#sleep(10)
#dockerRes = container.logs()
#print(float(dockerRes.decode().split('\r\n')[-2]))
#container.remove()
