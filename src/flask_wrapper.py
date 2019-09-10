import flask
from aautomation import *

app = flask.Flask(__name__)

def do_main():
    login()
    app.run()
#end main()

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


if __name__ == "__main__": do_main() #don't run on import
