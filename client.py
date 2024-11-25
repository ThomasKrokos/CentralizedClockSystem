from Pyro5.api import Proxy

# RUN THIS FILE AFTER server.py

if __name__ == "__main__":
    print("Pulling objects from pyro server \n")
    process0 = Proxy("PYRONAME:process.0")
    print(process0)
    process1 = Proxy("PYRONAME:process.1")
    print(process1)
    process2 = Proxy("PYRONAME:process.2")
    print(process2)
    timeserver = Proxy("PYRONAME:timeserver")
    print(timeserver)

    try:
        print("testing centralized clock synch...")
        process0.setTimeServer(timeserver)
        process1.setTimeServer(timeserver)
        process2.setTimeServer(timeserver)


        process0.synchronize()
        
        process1.synchronize()
        
        process2.synchronize()
        
        print("ending test of centralized clock synch")
        
    except Exception as e:
        print(f"error: {e}")
    