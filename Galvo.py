
import PyDAQmx

value_x = 0
value_y = 0

task_x = PyDAQmx.Task()
task_y = PyDAQmx.Task()

task_x.CreateAOVoltageChan("/Dev1/ao1","",
                           -10.0,10.0,PyDAQmx.DAQmx_Val_Volts,None)

task_y.CreateAOVoltageChan("/Dev1/ao0","",
                           -10.0,10.0,PyDAQmx.DAQmx_Val_Volts,None)

task_x.StartTask()
task_y.StartTask()

task_x.WriteAnalogScalarF64(1,10.0,value_x,None)
task_y.WriteAnalogScalarF64(0,10.0,value_y,None)

#task_x.StopTask()
#task_y.StopTask()
