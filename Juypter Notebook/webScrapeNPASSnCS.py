from bs4 import BeautifulSoup as bs
from selenium import webdriver
#from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import urllib
#import requests

chemspider_url = 'http://www.chemspider.com/Search.aspx?q='

def bsoupReq(cmpdname):
    req = urllib.request.Request(chemspider_url+cmpdname,
                                 headers={'User-Agent' : "Magic Browser"}) 
    con = urllib.request.urlopen( req )
    html = bs(con,'html.parser')
    return html
	
def checkCmpdSrc(soupPage,cmpdname):
    try:
        lstDetailSection=[]
        for j in soupPage.findAll('h2',{'class':'section-head'}):
            lstDetailSection.append(j.find('span').text)
        return ('Compound Source:' in lstDetailSection)
    except Exception as e:
        print(e)
		
def classifyDrg(cmpdname):
    bsoupreq = bsoupReq(cmpdname)
    return checkCmpdSrc(bsoupreq,cmpdname)
	
	
npass_url = 'http://bidd2.nus.edu.sg/NPASS/search.php'

def matchCnt(driver):
    matches = driver.find_element_by_tag_name("h2").text
    match_count = int(matches.split(':')[1].strip())
    print("{} matches were found".format(match_count))
    return match_count

def selenNPASS(driver,cmpdName):
	try:
		driver
	except NameError:
		driver = webdriver.Firefox(executable_path=r'C:/Program Files/Mozilla Firefox/geckoDriver/geckodriver.exe')
	finally:
		driver.get(npass_url)
		cmpdname = driver.find_element_by_name("CompoundName")
		cmpdname.send_keys(cmpdName)
		search_btn = driver.find_element_by_name('search_by_property')
		search_btn.send_keys(Keys.RETURN)
		#ActionChains(driver).key_down(Keys.CONTROL).send_keys('2').key_up(Keys.CONTROL).perform()
		windows = driver.window_handles
		driver.switch_to.window(windows[1])
		try:
			element = WebDriverWait(driver, 1).until(lambda driver: matchCnt(driver)>0 )
			if element:
				return True
		except TimeoutException:
			print('{} was not found in NPASS DB'.format(cmpdName))
			return False
		finally:
			driver.close()
			driver.switch_to.window(windows[0])
			return driver
		#innerHTML = driver.execute_script("return document.body.innerHTML")
		#bs(innerHTML,'html.parser')
	
def splitTxt(cmpdName):
	if '/' in cmpdName:
		cmpdName1 = cmpdName.split('/')[0].strip()
		cmpdName2 = cmpdName.split('/')[1].strip()
		return [cmpdName1,cmpdName2]
	else:
		return [cmpdName]
	
	
def dblNameSelenNpass(cmpdName):
	cname = splitTxt(cmpdName)
	if len(cname) >1:
		first_cnameRslt = selenNPASS(cname[0])
		if first_cnameRslt:
			return first_cnameRslt
		else:
			sec_cnameRslt = selenNPASS(cname[1])
			return sec_cnameRslt
	else:
		return selenNPASS(cname[0])
			
