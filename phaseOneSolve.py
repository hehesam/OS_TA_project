from sqlalchemy import null


class process():
    def __init__(self, ID, file_name):
        self.ID = ID
        self.state = "ready"
        self.temp = null
        self.IR = ""
        self.ACC = null
        self.PC = 0
        self.INST = open(file_name).readlines()

    def run(self):
        if self.state == "block":
            print("this process is blocked")
            return
        self.state = "running"
        self.IR = self.INST[self.PC]
        instructions = self.IR.split(" ")
        # print(instructions)
        instruction = instructions[0]
        value = float(instructions[1])
        self.temp = value 

        if instruction == "load":
            self.ACC = self.temp
        elif instruction == "add":
            self.ACC += self.temp
        elif instruction == "sub":
            self.ACC -= self.temp
        elif instruction == "mul":
            self.ACC *= self.temp

        self.PC += 1
        if self.PC >= len(self.INST):
            self.PC = 0

        self.state = "ready"
        

    def block(self):
        if self.state == "block":
            print("this process is blocked")
            return
        self.state = "block"

    def unblock(self):
        if self.state == "block":
                self.state = "ready"
        else :
            print("the process is already ready")
    def show_context(self):
        print(f"Process ID : {self.ID}\nInstruction Register : {self.IR}\nAccumulator : {self.ACC}\t\tTemp : {self.temp}")
        print(f"Program Counter : {self.PC}\t\tState : {self.state}")

index = 0

process_list = {}
running_process = -1
while True : 

    print("loop : ", index)
    index += 1

    signal_line = input()
    parameters = signal_line.split()
    signal = parameters[0]
    process_id = parameters[1]

    if signal == "create_process":
        process_id = parameters[1]
        instruction_file = parameters[2]
        pr = process(process_id,instruction_file)
        process_list[process_id] = pr
    else :
        if process_id not in process_list:
            print("process doesn't exist")
             
        elif signal == "run_process":
            process_id = parameters[1]
            pr = process_list[process_id] #!
            pr.run() 
        elif signal == "block_process":
            process_id = parameters[1]
            pr = process_list[process_id]
            pr.block()

        elif signal == "unblock_process":
            process_id = parameters[1]
            pr = process_list[process_id]
            pr.unblock()
        
        elif signal == "kill_process":
            process_id = parameters[1]
            process_list.pop(process_id)
        
        elif signal == "show_context":
            process_id = parameters[1]
            pr = process_list[process_id]
            pr.show_context()

        else :
            print("wrong input")