import networking, sys, tools, custom, os, multiprocessing, threads, api, blockchain

def daemonize(f):
    if sys.platform == 'win32':
        pypath = list(os.path.split(sys.executable))
        pypath[-1] = 'pythonw.exe'
        os.system('start '+os.path.join(*pypath)+' threads.py '+p)
        sys.exit(0)
    pid=os.fork()
    if pid==0: f()
    else: sys.exit(0)