from os import path, curdir, remove
from glob import glob
from time import sleep
from PIL import Image
from selenium import webdriver
from shutil import copy
import docker
import win32ui
import win32con

ROOT_DIR = path.abspath(curdir)


def scrapeImages(weblink, lookfor):

    #  clean up imageScrapingData directory
    files = glob(ROOT_DIR + '/imageScrapingData/*')
    for file in files:
        remove(file)

    desiredCap = {
        "browserName": "chrome"
    }

    try:
        # Local webdriver
        driver = webdriver.Chrome(executable_path=ROOT_DIR + '/driver/chromedriver.exe')

        # Remote webdriver for docker image
        # driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',desired_capabilities=desiredCap)

        driver.get(weblink)
        sleep(2)
        driver.save_screenshot(ROOT_DIR + '/imageScrapingData/fullscreen.png')  # take full screen screenshot

        elements = driver.find_elements_by_xpath("//button | //input")  # get all button or input tags

        intCounter = 0

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

                elementImagePath = '{0}/imageScrapingData/image{1}.png'.format(ROOT_DIR, str(intCounter))
                im.save(elementImagePath)

                imageTestPath = '{0}/tfImageClassifier/testData/{1}'.format(ROOT_DIR, path.basename(elementImagePath))

                copy(elementImagePath, imageTestPath)  # copy image to Tensorflow testData folder
                sleep(1)

                dblPct = getTfPctLocal(path.basename(imageTestPath),lookfor)

                remove(imageTestPath)  # delete file after tf processing

                result.append(
                    {'element': element, 'elementImage': elementImagePath, 'location': element.location,
                     'size': element.size, 'probability': dblPct})

        print(result)

        seq = [x['probability'] for x in result]
        maxPct = (max(seq))

        if win32ui.MessageBox("Element found with max " + str(round(maxPct * 100, 2)) + "% accuracy.",
                              "Identify Webpage Element", win32con.MB_OK) == win32con.IDOK:
            sleep(2)

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
    for x in range(5):
        apply_style("border: 3px solid blue;")
        sleep(.3)
        apply_style(original_style)
        sleep(.3)


def getTfPctLocal(testImageName,lookfor):

        
    try:
        dblPct = float(container.decode().split('\r\n')[-2])
    except ValueError:
        print("That's not an percent value!")
    return dblPct


# Provide your retails web url
scrapeImages('https://www.amazon.ca/', 'magnifyingglass')
