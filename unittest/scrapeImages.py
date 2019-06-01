from os import path, curdir
from time import sleep
from PIL import Image
from selenium import webdriver

ROOT_DIR = path.dirname(path.abspath(curdir))


def scrapeImages(weblink):

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
            if element.size['width'] > 0 and element.size['height'] > 0:  # get visible element (height/weight > 0 px)
                intCounter += 1

                x = element.location['x']
                y = element.location['y']
                width = element.location['x'] + element.size['width']
                height = element.location['y'] + element.size['height']

                im = Image.open(ROOT_DIR + '/imageScrapingData/fullscreen.png')
                im = im.crop((int(x), int(y), int(width), int(height)))

                elementImagePath = '{0}/imageScrapingData/image{1}.png'.format(ROOT_DIR, str(intCounter))
                im.save(elementImagePath)

                result.append(
                    {'elementImage': elementImagePath, 'location': element.location, 'size': element.size})

        print(result)

    finally:
        driver.close()
        driver.quit()


# Provide your retails web url
scrapeImages('https://www.amazon.ca/')