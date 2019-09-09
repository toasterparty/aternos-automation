import sys

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
    print("starting server...")

#end start()

def stop():
    print("stopping server...")

#end start()

def restart():
    print("restarting server...")
    
#end start()

if __name__ == "__main__": main() #don't run on import