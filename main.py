#!/usr/bin/env python
import os
import traceback
import sys
import time

from flask import Flask
from selenium import webdriver

# Constants #


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

# globals #
app = Flask(__name__)

busy = False

print("creating webdriver...")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

if os.name == 'nt':
    chrome_options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome("./test/chromedriver.exe",options=chrome_options)
else:
    driver = webdriver.Chrome(options=chrome_options)
#endif

#driver = webdriver.Firefox(FIREFOX_DRIVER_PATH)
print("webdriver created")

@app.route('/')
def root():
    return "/start - start the server\n/status - get server status"

@app.route('/start')
def do_start():
    try:
        lock_busy()
        login()
        start()
        unlock_busy()
        return "success"
    except Exception as e:
        return str(e)
    #end tryexcept
#end do_start()

@app.route('/stop')
def do_stop():
    try:
        lock_busy()
        login()
        stop()
        unlock_busy()
        return "success"
    except Exception as e:
        return str(e)
    #end tryexcept
#end do_stop()

@app.route('/restart')
def do_restart():
    try:
        lock_busy()
        login()
        restart()
        unlock_busy()
        return "success"
    except Exception as e:
        return str(e)
    #end tryexcept
#end do_restart()

@app.route('/status')
def do_status():
    try:
        lock_busy()
        login()
        status = get_status()
        unlock_busy()
        return status
    except Exception as e:
        return str(e)
    #end tryexcept
#end do_status()

def lock_busy():
    global busy
    start_wait_time = time.time()
    while(busy):
        time.sleep(0.5)
        if(start_wait_time > 10):
            print("10s elapsed... ignoring mutex...")
            busy = False
        #endif
    busy = True
#end lock_busy()

def unlock_busy():
    global busy
    busy = False
#end unlock_busy()

def start():
    global driver
    print("starting server...")
    driver.execute_script("start();")
#end start()

def stop():
    global driver
    print("stopping server...")
    driver.execute_script("stop();")
#end start()

def restart():
    global driver
    print("restarting server...")
    driver.execute_script("restart();")
#end start()

def get_status():
    global driver
    
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
    global driver
    print("checking login...")

    if("Server" in driver.title):
        print("already at server page")
        return
    #endif

    # attempt to open server page #
    driver.get("https://aternos.org/friends/")

    if(not ("Login" in driver.title)):
        print("already signed in! navigating to friend's page...")
        driver.execute_script(FRIEND_ACCESS_SCRIPT)
        return # already signed in
    #endif

    print("not signed in\nsigning in...")
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
    global driver
    driver.close()
#end stop_driver()

if __name__ == "__main__":
    login()
    app.run(host="0.0.0.0", port=8080, threaded=False)
