from os import path, curdir, remove
from glob import glob
from time import sleep
from PIL import Image
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from shutil import copy
import docker

ROOT_DIR: str = path.abspath(curdir)

def scrapeImages(weblink):

    #  clean up imageScrapingData directory
    files = glob(ROOT_DIR + '/imageScrapingData/*')
    for file in files:
        remove(file)

    driver: WebDriver
    desiredCap = {
        "browserName": "chrome"
    }

    try:
        # Local webdriver
        driver = webdriver.Chrome(executable_path=ROOT_DIR + '/chromedriver.exe')

        # Remote webdriver for docker image
        # driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',desired_capabilities=desiredCap)

        driver.get(weblink)
        sleep(2)
        driver.save_screenshot(ROOT_DIR + '/imageScrapingData/fullscreen.png')  # take full screen screenshot

        elements: List[WebElement] = driver.find_elements_by_xpath("//button | //input")  # get all button or input tags

        intCounter: int = 0
        element: WebElement

        result = []
        for element in elements:  # loop for each element
            if element.size['width'] > 0 and element.size['height'] > 0:  # check element is visible (height/weight > 0 px)
                intCounter += 1

                x = element.location['x']
                y = element.location['y']
                width = element.location['x'] + element.size['width']
                height = element.location['y'] + element.size['height']

                im = Image.open(ROOT_DIR + '/imageScrapingData/fullscreen.png')
                im = im.crop((int(x), int(y), int(width), int(height)))

                elementImagePath: str = '{0}/imageScrapingData/image{1}.png'.format(ROOT_DIR, str(intCounter))
                im.save(elementImagePath)

                imageTestPath: str = '{0}/tfImageClassifier/testData/{1}'.format(ROOT_DIR, path.basename(elementImagePath))

                copy(elementImagePath, imageTestPath)  # copy image to Tensorflow testData folder
                sleep(1)

                dblPct = getTfPctDocker(path.basename(imageTestPath))

                remove(imageTestPath)  # delete file after tf processing

                result.append(
                    {'element': element, 'elementImage': elementImagePath, 'location': element.location,
                     'size': element.size, 'probability':dblPct})

        print(result)

        seq = [x['probability'] for x in result]
        maxPct = (max(seq))

        for item in result:
            if item.get('probability') == maxPct:
                highlight(item.get('element'))


    finally:
        driver.close()
        driver.quit()


def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)
    original_style = element.get_attribute('style')
    for x in range(10):
        apply_style("border: 3px solid blue;")
        sleep(.4)
        apply_style(original_style)
        sleep(.4)


def getTfPctDocker(testImageName):
    client = docker.from_env()

    container = client.containers.run(
        'dasxran/tensorflow:trainimages',
        'python /image_classifier/scripts/return_pct.py --graph=/image_classifier/outputModel/retrained_graph.pb '
        '--labels=/image_classifier/outputModel/retrained_labels.txt --input_layer=Placeholder '
        '--output_layer=final_result --image=/image_classifier/testData/' + testImageName,
        detach=False, auto_remove=False, remove=True, tty=True, stdin_open=True, volumes={
            ROOT_DIR + '/tfImageClassifier': {
                'bind': '/image_classifier',
                'mode': 'rw',
            }
        })
    try:
        dblPct = float(container.decode().split('\r\n')[-2])
    except ValueError:
        print("That's not an percennt value!")
    return dblPct


# Provide your retails web url
scrapeImages('https://www.amazon.ca/')
