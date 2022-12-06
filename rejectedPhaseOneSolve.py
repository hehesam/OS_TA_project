

from sqlalchemy import null


class thread():
    def __init__(self, ID,function_ID):
        self.ID = ID
        self.FunctionID = function_ID
        self.state = True
        # self.PC = 0

    def start_thread(self, input_value_1,input_value_2):
        if self.state == False:
            print("thread is locked")
            return 

        if self.FunctionID == "add":
            return self.add(input_value_1,input_value_2)
        elif self.FunctionID == "sub":
            return self.subtract(input_value_1,input_value_2)
        elif self.FunctionID == "mul":
            return self.mult(input_value_1,input_value_2)
        else :
            print("wrong function ID")
            return 

    def lock_thread(self):
        if self.state == True:
            self.state = False
        else :
            print("The thread is already lock")
    
    def free_thread(self):
        if self.state == False:
            self.state = True
        else :
            print("The thread is already free")


    def add(self,input_value_1,input_value_2):
        print("add function")
        return input_value_1+input_value_2

    def subtract(self,input_value_1,input_value_2):
        print("subtract function")
        return input_value_1-input_value_2

    def mult(self,input_value_1,input_value_2):
        print("mult function")
        return input_value_1*input_value_2

class process():
    def __init__(self,ID):
        self.ID = ID
        self.state = True # suspended or running
        self.PC = 0
        self.REG = [null]*9
        self.Thread_list = {}


    def suspend(self):
        if self.state == False :
            print("it's already suspended")
        self.state = False

    def _continue(self):
        if self.state == True :
            print("it's already running")
        else:
            self.state = True 

    def program_counter(self):
        if self.state == True:
            self.PC += 1

    def print_register(self, register_id):
        if self.state == False :
            print("This process is suspended you can't do anything until it is free")
        else:
            print("Register\t", self.REG[register_id])
    
    def write_register(self, register_id, input_value):
        if self.state == False :
            print("This process is suspended you can't do anything until it is free")

    def print(self):
        if self.state == False :
            print("This process is suspended you can't do anything until it is free")
        else:
            print("Process ID\t", self.ID)
            print("Registers\n", self.REG)

    def clear_registers(self):
        if self.state == False :
            print("This process is suspended you can't do anything until it is free")
        else:
            self.REG = [null]*9
    
    def create_thread(self,thread_id, function_id):
        if self.state == False :
            print("This process is suspended you can't do anything until it is free")
        else:
            thr = thread(thread_id,function_id)
            self.Thread_list[thread_id] = thr
    
    def start_thread(self, thread_id, IN_register_id_1,IN_register_id_2, OUT_register_id):
        if self.state == False :
            print("This process is suspended you can't do anything until it is free")
        else:
            thr = self.Thread_list[thread_id]
            IN_reg_1 = self.REG[IN_register_id_1]
            IN_reg_2 = self.REG[IN_register_id_2]
            value = thr.start_thread(IN_reg_1,IN_reg_2)          # calculate the thread function 
            self.REG[OUT_register_id] = value       # set the value of thread function to a register

    def kill_thread(self, thread_id):
        if self.state == False :
            print("This process is suspended you can't do anything until it is free")
        else:
            self.Thread_list.pop(thread_id)     # remove the thread from process

    def lock_thread(self, thread_id):
        if self.state == False :
            print("This process is suspended you can't do anything until it is free")
        else:
            thr = self.Thread_list[thread_id]
            thr.lock_thread()                   # lock the thread so to calculation can be done

    def free_thread(self, thread_id):
        if self.state == False :
            print("This process is suspended you can't do anything until it is free")
        else:
            thr = self.Thread_list[thread_id]
            thr.free_thread()                   # free the thread so function can be called

REGISTERS = []



index = 0

process_list = {}
while True : 

    print("loop : ", index)
    index += 1

    signal_line = input()
    parameters = signal_line.split()
    signal =parameters[0]
    if signal == "start_process":
        pr = process(parameters[1])
        process_list[parameters[1]] = pr
        
    
    elif signal == "kill_prcess":
        process_id = parameters[1]
        if process_id not in process_list :
            print("process doesn't exist")
        else :     
            process_list.pop(process_id) # delete a process

    elif signal == "suspend_process":
        process_id = parameters[1]
        pr = process_list[process_id]
        pr.suspend()                #  suspend a process

    elif signal == "continue_process":
        process_id = parameters[1]
        pr = process_list[process_id]
        pr._continue()              #  process can continue its work

    elif signal == "read_process":
        process_id = parameters[1]
        pr = process_list[process_id]
        pr.print()                  # shows processID, threadIDs, regiters value, PC, state
 
    elif signal == "read_register":
        process_id = parameters[1]
        register_id = parameters[2]
        pr = process_list[process_id]   
        pr.print_register(register_id)        # shows the value of each register in one process

    elif signal == "write_register":
        process_id = parameters[1]
        input_registerID = parameters[2]
        input_value = parameters[3]
        pr = process_list[process_id]  
        pr.write_register(input_registerID,input_value)

    elif signal == "clear_register":
        process_id = parameters[1]
        pr = process_list[process_id] 
        pr.clear_registers()        # clean all the register from values

    elif signal == "create_thread":
        process_id = parameters[1]
        thread_id = parameters[2]
        function_id = parameters[3]
        pr = process_list[process_id]
        pr.create_thread(thread_id,function_id) # create and add a thread to a process and specifing its function type
        

    elif signal == "start_thread":
        process_id = parameters[1]
        thread_id = parameters[2]
        register_id = parameters[3]
        input_value = parameters[4]
        pr = process_list[process_id]
        pr.start_thread(thread_id,register_id,input_value)  # a thread calculates a function and set the value of a register to the output of that function

    elif signal == "kill_thread":
        process_id = parameters[1]
        thread_id = parameters[2]
        pr = process_list[process_id]
        pr.kill_thread(thread_id)               # pop the thread from process


    elif signal == "lock_thread":
        process_id = parameters[1]
        thread_id = parameters[2]
        pr = process_list[process_id]
        pr.lock_thread(thread_id)           # lock the thread and forbbids any calculation 

    elif signal == "free_thread":
        process_id = parameters[1]
        thread_id = parameters[2]
        pr = process_list[process_id]
        pr.free_thread(thread_id)       # 