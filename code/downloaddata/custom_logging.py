#importing the module 
import os
from config import BASE_DIR

class CustomLogging():
    def logOutput(log, gediL2AFlag):
        if gediL2AFlag:
            logfile = BASE_DIR+"/logs/std_l2a.log"
        else:
            logfile = BASE_DIR+"/logs/std_l2b.log"
        
        if os.path.exists(logfile):
            with open(logfile, "a") as f:
                f.write(log+"\n")
                print(log)
        else:
            with open(logfile, "w+") as f:
                f.write(log+"\n")
                print(log)
            
