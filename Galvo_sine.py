
import PyDAQmx
import time
import numpy as np

f = 1
omega = 2*np.pi*f
A = 8
B = 0

task = PyDAQmx.Task()

task.CreateAOVoltageChan("/Dev1/ao0","",
                           -10.0,10.0,PyDAQmx.DAQmx_Val_Volts,None)

# a0 for y mirror, a1 for x mirror.

task.StartTask()

rt = 10

st = time.clock()

while time.clock() - st <= rt:
    t = time.clock() - st
    value = A*np.sin(omega*t) + B
    task.WriteAnalogScalarF64(1,10.0,value,None)
    
task.StopTask()