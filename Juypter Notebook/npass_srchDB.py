from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException,NoSuchElementException,MoveTargetOutOfBoundsException

def isNP(cmpdName,driver):    
    driver.get(url)
    windows = driver.window_handles
    cmpdname = driver.find_element_by_name("CompoundName")
    cmpdname.send_keys(cmpdName)
    search_btn = driver.find_element_by_name('search_by_property')
    search_btn.send_keys("\n")
    driver.switch_to.window(windows[1])
    try:
        WebDriverWait(driver, 1).until(lambda driver: matchCnt(driver)>0 )
        driver.implicitly_wait(1.5)
        return True
    except TimeoutException:
        print('{} was not found in NPASS DB'.format(cmpdName))
        return False
    finally:
        driver.close()
        
        
def matchCnt(driver):
    matches = driver.find_element_by_tag_name("h2").text
    match_count = int(matches.split(':')[1].strip())
    print("{} matches were found".format(match_count))
    return match_count