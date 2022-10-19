
import os
print(" Program to demonstrate wait() method:")
print("\n")
print("Creating child process:")
pr = os.fork()
if pr is 0:    
    print("Child process will print the numbers from the range 0 to 5")
    for i in range(0, 5):
        print("Child process printing the number %d"%(i))      
    print("Child process with number %d existing" %os.getpid())
    print("The child process is",(os.getpid()))
else:    
    print("The parent process is now waiting")
    cpe = os.wait()
    print("Child process with number %d exited" % (cpe[0]))
    print("Parent process with number %d exiting after child has executed its process" % (os.getpid()))
    print("The parent process is", (os.getpid()))