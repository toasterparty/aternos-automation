import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    if(len(sys.argv) != 2):
        print("ERROR: Invalid Arguments")
        return
    #endif

    if(sys.argv[1] == "start"):
        start()
    elif(sys.argv[1] == "stop"):
        stop()
    elif(sys.argv[1] == "restart"):
        restart()
    else:
        print("ERROR: Invalid Arguments")
    #endif
#end main()

def start():
    global driver

    print("starting server...")
    connect()
    disconnect()
#end start()

def stop():
    print("stopping server...")

#end start()

def restart():
    print("restarting server...")
    
#end start()

def connect():
    global driver
    driver = webdriver.Chrome()
    driver.get("https://aternos.org/server/")

    if("Login" in driver.title):
        print("signing in...")

    #endif

#end connect()

def disconnect():
    driver.close()
#end disconnect()

if __name__ == "__main__": main() #don't run on import