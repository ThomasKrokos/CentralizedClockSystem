import Pyro5.api
import Pyro5.server
import random
from datetime import datetime, timedelta


@Pyro5.server.expose
@Pyro5.server.behavior(instance_mode="single")
class TimeServer(object):
    def getTimeServerTime(self):
        now = datetime.now()
        self.clock = now
        self.current_time = self.clock.time()
        return self.current_time


@Pyro5.server.expose
@Pyro5.server.behavior(instance_mode="single")
class Process(object):
    def __init__(self, pid):
        self.microsecond_offset = random.randint(0, 200) - 100
        self.local_clock = datetime.combine(datetime.now().date(), datetime.now().time())        
        print("WE GOT HEREINIT")
        
        self.local_clock = self.local_clock + timedelta(microseconds=self.microsecond_offset) 
        self.local_time = self.local_clock.time()
        self.pid = pid

        print(f"Process {pid} has been created with clock offset of {self.microsecond_offset} microseconds")

    def setTimeServer(self, time_server):
        self.time_server = time_server

    
    def getLocalTime(self):
        self.local_clock = datetime.combine(datetime.now().date(), datetime.now().time())
        self.local_clock = self.local_clock + timedelta(microseconds=self.microsecond_offset) 
        self.local_time = self.local_clock.time()
        return self.local_time
    
    def synchronize(self):
        print(f"Local time for process {self.pid} is at {self.getLocalTime()}")
        true_time = datetime.strptime(self.time_server.getTimeServerTime(), "%H:%M:%S.%f").time()
        print(f"Time from time server is {true_time}")
        offset = self.calculateOffset(self.local_time, true_time)
        print(f"Time offset: {offset}")
        if offset.total_seconds()<0:
            print(f"Slowing down process {self.pid}'s clock to align with time server")
        elif offset.total_seconds()>0:
            print(f"Jumping forward {self.pid}'s clock to align with time server")
        else:
            print(f"Process {self.pid}'s clock is already synchronized with the time server")

            
    def calculateOffset(self, local_time, server_time):
        now = datetime.now()
        local_datetime = datetime.combine(now.date(), local_time)
        server_datetime = datetime.combine(now.date(), server_time)
        offset = local_datetime - server_datetime
        return offset
    

@Pyro5.server.expose
class Process0(Process):
    def __init__(self):
        super().__init__(0)

@Pyro5.server.expose
class Process1(Process):
    def __init__(self):
        super().__init__(1)

@Pyro5.server.expose
class Process2(Process):
    def __init__(self):
        super().__init__(2)



if __name__ == "__main__":
    print("please run nameserver.py first")
    time_server = TimeServer()

    print("Registering timeserver and processes with pyro...")
    daemon = Pyro5.server.Daemon()         
    ns = Pyro5.api.locate_ns()             
    uri = daemon.register(TimeServer)   # register the Time Server as a Pyro object
    ns.register(f"timeserver", uri) 
    print(f"registered timeserver")
    
    urip0 = daemon.register(Process0())   # register the process as a Pyro object
    ns.register(f"process.0", urip0) 
    print(f"registered process0")

    urip1 = daemon.register(Process1())   # register the process as a Pyro object
    ns.register(f"process.1", urip1) 
    print(f"registered process1")
    
    urip2 = daemon.register(Process2())   # register the process as a Pyro object
    ns.register(f"process.2", urip2) 
    print(f"registered process2")
    
    print("Server is ready.")
    daemon.requestLoop()