import flask
from aautomation import *

f_app = flask.Flask(__name__)

def app():
    print("started")
    login()
    f_app.run(host="0.0.0.0")
#end main()

@f_app.route('/start')
def do_start():
    login()
    start()
    return "success"
#end do_start()

@f_app.route('/stop')
def do_stop():
    login()
    stop()
    return "success"
#end do_stop()

@f_app.route('/restart')
def do_restart():
    login()
    restart()
    return "success"
#end do_restart()

@f_app.route('/status')
def do_status():
    login()
    return get_status()
#end do_status()


if __name__ == "__main__": app() #don't run on import
