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
def recvall(client, data=''):
    try:
        data+=client.recv(MAX_MESSAGE_SIZE)
    except:
        time.sleep(0.0001)
        tools.log('not ready')
        recvall(client, data)        
    if not data:
        return 'broken connection'
    if len(data)<5: return recvall(client, data)
    try:
        length=int(data[0:5])
    except:
        return 'no length'
    tries=0
    data=data[5:]
    while len(data)<length:
        d=client.recv(MAX_MESSAGE_SIZE-len(data))
        if not d:
            return 'broken connection'
        data+=d
    try:
        data=unpackage(data)
    except:
        pass
    return data