import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Constants #

CHROME_PATH        = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
CHROME_DRIVER_PATH = "D:/Libraries/git/aternos-automation/bin/chromedriver"

# Global Variables #
try:
    del driver
    del chrome_options
except Exception:
    pass
#end tryexcept

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = CHROME_PATH
driver = webdriver.Chrome(CHROME_DRIVER_PATH,options=chrome_options)

# Methods #

def main():
    if(len(sys.argv) != 2):
        print("ERROR: Invalid Arguments")
        return
    #endif

    login()

    if(sys.argv[1] == "start"):
        start()
    elif(sys.argv[1] == "stop"):
        stop()
    elif(sys.argv[1] == "restart"):
        restart()
    else:
        print("ERROR: Invalid Arguments")
    #endif

    input("")
    stop_driver()
#end main()

def start():
    global driver
    print("starting server...")

    result = driver.execute_script("start();")
    print(str(result))
#end start()

def stop():
    global driver
    print("stopping server...")

    result = driver.execute_script("stop();")
    print(str(result))
#end start()

def restart():
    global driver
    print("restarting server...")
    
    result = driver.execute_script("restart();")
    print(str(result))
#end start()

def login():
    # attempt to open server page #
    driver.get("https://aternos.org/server/")

    if(not ("Login" in driver.title)):
        return # already signed in
    #endif

    print("signing in...")

    # set username #
    result = driver.execute_script("$(\"#user\").val(\"" + USERNAME + "\");")
    print(str(result))

    # set password #
    result = driver.execute_script("$(\"#password\").val(\"" + PASSWORD + "\");")
    print(str(result))

    # login #
    result = driver.execute_script("login();")
    print(str(result))

    # accept EULA #
    result = driver.execute_script("acceptEULA();")
    print(str(result))
#end login()

def stop_driver():
    driver.close()
#end stop_driver()

if __name__ == "__main__": main() #don't run on import