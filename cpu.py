class Cpu:
    def __init__(self):

        # Our memory is an array that contains data and instructions,
        # this will be populated by whatever code calls this class
        self.memory=[]

        # a,x,y are general purpose registers
        self.a = 0
        self.x = 0
        self.y = 0

        # The stack pointer 
        self.sp = 0

        # The program counter
        self.pc = 0

        # These flags let us know if the previous operation
        # resulted in a negative value, overflow, and other various states,
        # we'll expand on this later
        self.flag_negative = 0
        self.flag_overflow = 0
        self.flag_break = 0
        self.flag_decimal = 0
        self.flag_interrupt = 0
        self.flag_zero = 0
        self.flag_carry = 0

        self.debug = False

        # Each CPU instruction has a hexidecimal code,  our instructions
        # dictionary lets as associate this code with a function that performs
        # the correct operation
        self.instructions={
            "0xa5":self.ins_a5,
            "0xa6":self.ins_a6,
            "0x85":self.ins_85,
            "0x86":self.ins_86,
            "0x0":self.ins_00,
        }

    def show_registers(self):
        print("A\tX\tY\tSP\tPC")
        print("%s\t%s\t%s\t%s\t%s" % (self.a, self.x, self.y, self.sp, self.pc))
       
        
    def run(self):
        """
        run will go through memory and run instructions until it
        detects a break or hits the end of memory
        """
        while not self.flag_break and self.pc<len(self.memory):
            self.step()
            # Every instruction will increment our program counter by at least 1.
            # Most will do at least 2, and some 3.  If they need to do this, we'll handle
            # that inside that insutrctions function
            self.pc+=1

    def step(self):
        # Get the instruction from the memory location indicated with our program counter
        ins = self.memory[self.pc]
        # Run the method that matches the value we just fetched
        if self.debug:
            print("Running %s found at %s" % (hex(ins),hex(self.pc)))
            self.show_registers()
        self.instructions[hex(ins)]()
 
    def ins_a5(self):
        self.a=self.memory[self.memory[self.pc+1]]
        self.pc+=1
        
    def ins_a6(self):
        self.x=self.memory[self.memory[self.pc+1]]
        self.pc+=1
       
    def ins_85(self):
        self.memory[self.memory[self.pc+1]]=self.a
        self.pc+=1
       
    def ins_86(self):
        self.memory[self.memory[self.pc+1]]=self.x
        self.pc+=1
  
    def ins_00(self):
        self.flag_break=1
        
