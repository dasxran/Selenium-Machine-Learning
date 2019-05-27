from os import path, curdir, remove
from glob import glob
from time import sleep
from PIL import Image
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

ROOT_DIR: str = path.abspath(curdir)

#  clean up data directory
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

    driver.get('https://www.amazon.com')
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

            result.append(
                {'element': element, 'elementImage': elementImagePath, 'location': element.location,
                 'size': element.size})

    print(result)

    for item in result:
        print(item.get('elementImage'))

finally:
    driver.close()
    driver.quit()