import socket, tools, custom, time, sys, select
from json import dumps as package, loads as unpackage
MAX_MESSAGE_SIZE = 60000
def serve_forever(handler, port, heart_queue='default', external=False):
    if heart_queue=='default':
        import Queue
        heart_queue=Queue.Queue()
    if external:
        host='0.0.0.0'
    else:
        host = 'localhost'
    backlog = 5
    time.sleep(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind((host,port))
    except:
        tools.kill_processes_using_ports([str(port)])
        tools.kill_processes_using_ports([str(port)])
        time.sleep(2)
        return serve_forever(handler, port, heart_queue)
    s.listen(backlog)
    while True:
        try:
            a=serve_once(s, MAX_MESSAGE_SIZE, handler)
            if a=='stop':
                s.close()
                tools.log('shutting off server: ' +str(port))
                return
        except Exception as exc:
            tools.log('networking error: ' +str(port))
            tools.log(exc)