import os
import traceback
import sys
import time
import logging

from flask import Flask
from selenium import webdriver

logging.info('started')

app = Flask(__name__)

logging.info('flask started')

# Constants #

#CHROME_DRIVER_PATH = "./webdrivers/chromedriver"
FIREFOX_DRIVER_PATH = "./webdrivers/geckodriver"


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

@app.route('/')
def root():
    return "test"

@app.route('/start')
def do_start():
    login()
    start()
    return "success"
#end do_start()

@app.route('/stop')
def do_stop():
    login()
    stop()
    return "success"
#end do_stop()

@app.route('/restart')
def do_restart():
    login()
    restart()
    return "success"
#end do_restart()

@app.route('/status')
def do_status():
    login()
    return get_status()
#end do_status()

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
    global driver

    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    #driver = webdriver.Chrome(CHROME_DRIVER_PATH,options=chrome_options)
    driver = webdriver.Firefox(FIREFOX_DRIVER_PATH)

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
    global driver
    driver.close()
#end stop_driver()

if __name__ == "__main__":
    logging.info('starting flask app...')
    app.run(host="127.0.0.1", port=8080)
    logging.info('flask app started')