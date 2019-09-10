import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Constants #

CHROME_PATH        = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
CHROME_DRIVER_PATH = "D:/Libraries/git/aternos-automation/bin/chromedriver"

FRIEND_ACCESS_SCRIPT = """
function my_script() {
    apost('/panel/ajax/friends/access.php', {user: "thecodestercraft"}, function (result) {
        data = JSON.parse(result);
        if (!data.success) {
            if (!data.error) {
                data.error = LANGUAGE.error;
            }

            alert({
                text: data.error,
                color: "red",
                buttons: ["okay"]
            });
            return;
        }

        setTimeout(function () {
            location.href = data.location;
        }, 300);
    });
}
my_script();
"""

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
    elif(sys.argv[1] == "status"):
        get_status()
    else:
        print("ERROR: Invalid Arguments")
    #endif

    print("script done!")
    stop_driver()
#end main()

def start():
    global driver
    print("starting server...")
    time.sleep(2)
    driver.execute_script("start();")
#end start()

def stop():
    global driver
    print("stopping server...")
    time.sleep(2)
    driver.execute_script("stop();")
#end start()

def restart():
    global driver
    print("restarting server...")
    time.sleep(2)
    driver.execute_script("restart();")
#end start()

def get_status():
    global driver
    time.sleep(2)
    
    isQueueing = driver.execute_script("return $('.status').hasClass(\"queueing\");")
    print(str(isQueueing))

    isLoading = driver.execute_script("return $('.status').hasClass(\"loading\");")
    print(str(isLoading))

    isOnline   = driver.execute_script("return $('.status').hasClass(\"online\");")
    print(str(isOnline))

    isOffline  = driver.execute_script("return $('.status').hasClass(\"offline\");")
    print(str(isOffline))

    if(isOnline):
        status = "ONLINE"
    elif(isQueueing or isLoading):
        status = "QUEUED"
    elif (isOffline):
        status = "OFFLINE"
    else:
        status = "UNHANDLED"
    #endif

    print("status = " + status)

    return status
#endf get_status()

def login():
    # attempt to open server page #
    driver.get("https://aternos.org/friends/")

    if(not ("Login" in driver.title)):
        driver.execute_script(FRIEND_ACCESS_SCRIPT)
        return # already signed in
    #endif

    print("signing in...")
    driver.execute_script("$(\"#user\").val(\""     + USERNAME + "\");")
    driver.execute_script("$(\"#password\").val(\"" + PASSWORD + "\");")
    driver.execute_script("login();")
    time.sleep(2)

    # accept EULA #
    #result = driver.execute_script("acceptEULA();")
    #print(str(result))
    #time.sleep(2)

    # goto friend's server page #
    print("going to friend's page...")
    driver.get("https://aternos.org/friends/")
    time.sleep(2)
    driver.execute_script(FRIEND_ACCESS_SCRIPT)
#end login()

def stop_driver():
    driver.close()
#end stop_driver()

if __name__ == "__main__": main() #don't run on import
