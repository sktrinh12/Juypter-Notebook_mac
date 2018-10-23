#from bs4 import BeautifulSoup as bs
from selenium import webdriver
#from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
#import urllib
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

def create_driver_session(session_id, executor_url):
    '''Sends a command to be executed by a command.CommandExecutor.
    Args:driver_command: The name of the command to execute as a string.
    params: A dictionary of named parameters to send with the command.
    Returns:The command’s JSON response loaded into a dictionary object'''
    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute #template function
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response (dummy response)
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)
    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute
    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id
    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute
    return new_driver

def matchCnt(driver,cmpdName):
    matches = driver.find_element_by_tag_name("h2").text
    match_count = int(matches.split(':')[1].strip())
    print("{} matches were found for {}".format(match_count,cmpdName))
    return match_count

def selenNPASS(cmpdName,driver=None):
	if driver is not None: #attach to existing session
		executor_url = driver.command_executor._url
		session_id = driver.session_id
		driver = create_driver_session(session_id, executor_url)
	else:
		driver = webdriver.Firefox(executable_path=r'C:/Program Files/Mozilla Firefox/geckoDriver/geckodriver.exe')
	driver.get(npass_url)
	driver.implicitly_wait(1.5)
	cmpdname = driver.find_element_by_name("CompoundName")
	cmpdname.send_keys(cmpdName)
	search_btn = driver.find_element_by_name('search_by_property')
	search_btn.send_keys(Keys.RETURN)
	#ActionChains(driver).key_down(Keys.CONTROL).send_keys('2').key_up(Keys.CONTROL).perform()
	windows = driver.window_handles
	driver.switch_to.window(windows[1])
	try:
		element = WebDriverWait(driver, 1).until(lambda driver: matchCnt(driver,cmpdName)>0 )
		if element:
			return True
	except TimeoutException:
		print('{} was not found in NPASS DB'.format(cmpdName))
		return False
	finally:
		driver.close()
		driver.switch_to.window(windows[0])
	#innerHTML = driver.execute_script("return document.body.innerHTML")
	#bs(innerHTML,'html.parser')
	
def splitTxt(cmpdName):
	if '/' in cmpdName:
		cmpdName1 = cmpdName.split('/')[0].strip()
		cmpdName2 = cmpdName.split('/')[1].strip()
		return [cmpdName1,cmpdName2]
	else:
		return [cmpdName]
	
	
def dblNameSelenNpass(cmpdName,driver):
	cname = splitTxt(cmpdName)
	if len(cname) >1:
		first_cnameRslt = selenNPASS(cname[0],driver)
		if first_cnameRslt:
			return first_cnameRslt #return True
		else:
			sec_cnameRslt = selenNPASS(cname[1],driver)
			return sec_cnameRslt #return True
	else:
		return selenNPASS(cname[0],driver)
			
