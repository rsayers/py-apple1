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
            0x69:{'fn':self.op_ADC, 'mode':'IMM', 'cycles':2},
            0x65:{'fn':self.op_ADC, 'mode':'ZPG', 'cycles':2},
            0x75:{'fn':self.op_ADC, 'mode':'ZPX', 'cycles':2},
            0x6D:{'fn':self.op_ADC, 'mode':'ABS', 'cycles':3},
            0x7D:{'fn':self.op_ADC, 'mode':'ABS', 'cycles':3},
            0x79:{'fn':self.op_ADC, 'mode':'ABS', 'cycles':3},
            0x61:{'fn':self.op_ADC, 'mode':'IDX', 'cycles':2},
            0x71:{'fn':self.op_ADC, 'mode':'IDY', 'cycles':2},
            0x29:{'fn':self.op_AND, 'mode':'IMM', 'cycles':2},
            0x25:{'fn':self.op_AND, 'mode':'ZPG', 'cycles':2},
            0x35:{'fn':self.op_AND, 'mode':'ZPX', 'cycles':2},
            0x2D:{'fn':self.op_AND, 'mode':'ABS', 'cycles':3},
            0x3D:{'fn':self.op_AND, 'mode':'ABS', 'cycles':3},
            0x39:{'fn':self.op_AND, 'mode':'ABS', 'cycles':3},
            0x21:{'fn':self.op_AND, 'mode':'IDX', 'cycles':2},
            0x31:{'fn':self.op_AND, 'mode':'IDY', 'cycles':2},
            0x0A:{'fn':self.op_ASL, 'mode':'IMP', 'cycles':1},
            0x06:{'fn':self.op_ASL, 'mode':'ZPG', 'cycles':2},
            0x16:{'fn':self.op_ASL, 'mode':'ZPX', 'cycles':2},
            0x0E:{'fn':self.op_ASL, 'mode':'ABS', 'cycles':3},
            0x1E:{'fn':self.op_ASL, 'mode':'ABS', 'cycles':3},
            0x24:{'fn':self.op_BIT, 'mode':'ZPG', 'cycles':2},
            0x2C:{'fn':self.op_BIT, 'mode':'ABS', 'cycles':3},
            0x00:{'fn':self.op_BRK, 'mode':'IMP', 'cycles':1},
            0x18:{'fn':self.op_CLC, 'mode':'IMP', 'cycles':1},
            0xD8:{'fn':self.op_CLD, 'mode':'IMP', 'cycles':1},
            0x58:{'fn':self.op_CLI, 'mode':'IMP', 'cycles':1},
            0xB8:{'fn':self.op_CLV, 'mode':'IMP', 'cycles':1},
            0xC9:{'fn':self.op_CMP, 'mode':'IMM', 'cycles':2},
            0xC5:{'fn':self.op_CMP, 'mode':'ZPG', 'cycles':2},
            0xD5:{'fn':self.op_CMP, 'mode':'ZPX', 'cycles':2},
            0xCD:{'fn':self.op_CMP, 'mode':'ABS', 'cycles':3},
            0xDD:{'fn':self.op_CMP, 'mode':'ABS', 'cycles':3},
            0xD9:{'fn':self.op_CMP, 'mode':'ABS', 'cycles':3},
            0xC1:{'fn':self.op_CMP, 'mode':'IDX', 'cycles':2},
            0xD1:{'fn':self.op_CMP, 'mode':'IDY', 'cycles':2},
            0xE0:{'fn':self.op_CPX, 'mode':'IMM', 'cycles':2},
            0xE4:{'fn':self.op_CPX, 'mode':'ZPG', 'cycles':2},
            0xEC:{'fn':self.op_CPX, 'mode':'ABS', 'cycles':3},
            0xC0:{'fn':self.op_CPY, 'mode':'IMM', 'cycles':2},
            0xC4:{'fn':self.op_CPY, 'mode':'ZPG', 'cycles':2},
            0xCC:{'fn':self.op_CPY, 'mode':'ABS', 'cycles':3},
            0xC6:{'fn':self.op_DEC, 'mode':'ZPG', 'cycles':2},
            0xD6:{'fn':self.op_DEC, 'mode':'ZPX', 'cycles':2},
            0xCE:{'fn':self.op_DEC, 'mode':'ABS', 'cycles':3},
            0xDE:{'fn':self.op_DEC, 'mode':'ABS', 'cycles':3},
            0xCA:{'fn':self.op_DEX, 'mode':'IMP', 'cycles':1},
            0x88:{'fn':self.op_DEY, 'mode':'IMP', 'cycles':1},
            0x49:{'fn':self.op_EOR, 'mode':'IMM', 'cycles':2},
            0x45:{'fn':self.op_EOR, 'mode':'ZPG', 'cycles':2},
            0x55:{'fn':self.op_EOR, 'mode':'ZPX', 'cycles':2},
            0x4D:{'fn':self.op_EOR, 'mode':'ABS', 'cycles':3},
            0x5D:{'fn':self.op_EOR, 'mode':'ABS', 'cycles':3},
            0x59:{'fn':self.op_EOR, 'mode':'ABS', 'cycles':3},
            0x41:{'fn':self.op_EOR, 'mode':'IDX', 'cycles':2},
            0x51:{'fn':self.op_EOR, 'mode':'IDY', 'cycles':2},
            0xE6:{'fn':self.op_INC, 'mode':'ZPG', 'cycles':2},
            0xF6:{'fn':self.op_INC, 'mode':'ZPX', 'cycles':2},
            0xEE:{'fn':self.op_INC, 'mode':'ABS', 'cycles':3},
            0xFE:{'fn':self.op_INC, 'mode':'ABS', 'cycles':3},
            0xE8:{'fn':self.op_INX, 'mode':'IMP', 'cycles':1},
            0xC8:{'fn':self.op_INY, 'mode':'IMP', 'cycles':1},
            0x4C:{'fn':self.op_JMP, 'mode':'ABS', 'cycles':3},
            0x20:{'fn':self.op_JSR, 'mode':'ABS', 'cycles':3},
            0xA9:{'fn':self.op_LDA, 'mode':'IMM', 'cycles':2},
            0xA5:{'fn':self.op_LDA, 'mode':'ZPG', 'cycles':2},
            0xB5:{'fn':self.op_LDA, 'mode':'ZPX', 'cycles':2},
            0xAD:{'fn':self.op_LDA, 'mode':'ABS', 'cycles':3},
            0xBD:{'fn':self.op_LDA, 'mode':'ABS', 'cycles':3},
            0xB9:{'fn':self.op_LDA, 'mode':'ABS', 'cycles':3},
            0xA1:{'fn':self.op_LDA, 'mode':'IDX', 'cycles':2},
            0xB1:{'fn':self.op_LDA, 'mode':'IDY', 'cycles':2},
            0xA2:{'fn':self.op_LDX, 'mode':'IMM', 'cycles':2},
            0xA6:{'fn':self.op_LDX, 'mode':'ZPG', 'cycles':2},
            0xB6:{'fn':self.op_LDX, 'mode':'ZPY', 'cycles':2},
            0xAE:{'fn':self.op_LDX, 'mode':'ABS', 'cycles':3},
            0xBE:{'fn':self.op_LDX, 'mode':'ABS', 'cycles':3},
            0xA0:{'fn':self.op_LDY, 'mode':'IMM', 'cycles':2},
            0xA4:{'fn':self.op_LDY, 'mode':'ZPG', 'cycles':2},
            0xB4:{'fn':self.op_LDY, 'mode':'ZPX', 'cycles':2},
            0xAC:{'fn':self.op_LDY, 'mode':'ABS', 'cycles':3},
            0xBC:{'fn':self.op_LDY, 'mode':'ABS', 'cycles':3},
            0x4A:{'fn':self.op_LSR, 'mode':'IMP', 'cycles':1},
            0x46:{'fn':self.op_LSR, 'mode':'ZPG', 'cycles':2},
            0x56:{'fn':self.op_LSR, 'mode':'ZPX', 'cycles':2},
            0x4E:{'fn':self.op_LSR, 'mode':'ABS', 'cycles':3},
            0x5E:{'fn':self.op_LSR, 'mode':'ABS', 'cycles':3},
            0xEA:{'fn':self.op_NOP, 'mode':'IMP', 'cycles':1},
            0x09:{'fn':self.op_ORA, 'mode':'IMM', 'cycles':2},
            0x05:{'fn':self.op_ORA, 'mode':'ZPG', 'cycles':2},
            0x15:{'fn':self.op_ORA, 'mode':'ZPX', 'cycles':2},
            0x0D:{'fn':self.op_ORA, 'mode':'ABS', 'cycles':3},
            0x1D:{'fn':self.op_ORA, 'mode':'ABS', 'cycles':3},
            0x19:{'fn':self.op_ORA, 'mode':'ABS', 'cycles':3},
            0x01:{'fn':self.op_ORA, 'mode':'IDX', 'cycles':2},
            0x11:{'fn':self.op_ORA, 'mode':'IDY', 'cycles':2},
            0x48:{'fn':self.op_PHA, 'mode':'IMP', 'cycles':1},
            0x08:{'fn':self.op_PHP, 'mode':'IMP', 'cycles':1},
            0x68:{'fn':self.op_PLA, 'mode':'IMP', 'cycles':1},
            0x28:{'fn':self.op_PLP, 'mode':'IMP', 'cycles':1},
            0x2A:{'fn':self.op_ROL, 'mode':'IMP', 'cycles':1},
            0x26:{'fn':self.op_ROL, 'mode':'ZPG', 'cycles':2},
            0x36:{'fn':self.op_ROL, 'mode':'ZPX', 'cycles':2},
            0x2E:{'fn':self.op_ROL, 'mode':'ABS', 'cycles':3},
            0x3E:{'fn':self.op_ROL, 'mode':'ABS', 'cycles':3},
            0x6A:{'fn':self.op_ROR, 'mode':'IMP', 'cycles':1},
            0x66:{'fn':self.op_ROR, 'mode':'ZPG', 'cycles':2},
            0x76:{'fn':self.op_ROR, 'mode':'ZPX', 'cycles':2},
            0x6E:{'fn':self.op_ROR, 'mode':'ABS', 'cycles':3},
            0x7E:{'fn':self.op_ROR, 'mode':'ABS', 'cycles':3},
            0x40:{'fn':self.op_RTI, 'mode':'IMP', 'cycles':1},
            0x60:{'fn':self.op_RTS, 'mode':'IMP', 'cycles':1},
            0xE9:{'fn':self.op_SBC, 'mode':'IMM', 'cycles':2},
            0xE5:{'fn':self.op_SBC, 'mode':'ZPG', 'cycles':2},
            0xF5:{'fn':self.op_SBC, 'mode':'ZPX', 'cycles':2},
            0xED:{'fn':self.op_SBC, 'mode':'ABS', 'cycles':3},
            0xFD:{'fn':self.op_SBC, 'mode':'ABS', 'cycles':3},
            0xF9:{'fn':self.op_SBC, 'mode':'ABS', 'cycles':3},
            0xE1:{'fn':self.op_SBC, 'mode':'IDX', 'cycles':2},
            0xF1:{'fn':self.op_SBC, 'mode':'IDY', 'cycles':2},
            0x38:{'fn':self.op_SEC, 'mode':'IMP', 'cycles':1},
            0xF8:{'fn':self.op_SED, 'mode':'IMP', 'cycles':1},
            0x78:{'fn':self.op_SEI, 'mode':'IMP', 'cycles':1},
            0x85:{'fn':self.op_STA, 'mode':'ZPG', 'cycles':2},
            0x95:{'fn':self.op_STA, 'mode':'ZPX', 'cycles':2},
            0x8D:{'fn':self.op_STA, 'mode':'ABS', 'cycles':3},
            0x9D:{'fn':self.op_STA, 'mode':'ABS', 'cycles':3},
            0x99:{'fn':self.op_STA, 'mode':'ABS', 'cycles':3},
            0x81:{'fn':self.op_STA, 'mode':'IDX', 'cycles':2},
            0x91:{'fn':self.op_STA, 'mode':'IDY', 'cycles':2},
            0x86:{'fn':self.op_STX, 'mode':'ZPG', 'cycles':2},
            0x96:{'fn':self.op_STX, 'mode':'ZPY', 'cycles':2},
            0x8E:{'fn':self.op_STX, 'mode':'ABS', 'cycles':3},
            0x84:{'fn':self.op_STY, 'mode':'ZPG', 'cycles':2},
            0x94:{'fn':self.op_STY, 'mode':'ZPX', 'cycles':2},
            0x8C:{'fn':self.op_STY, 'mode':'ABS', 'cycles':3},
            0xAA:{'fn':self.op_TAX, 'mode':'IMP', 'cycles':1},
            0xA8:{'fn':self.op_TAY, 'mode':'IMP', 'cycles':1},
            0xBA:{'fn':self.op_TSX, 'mode':'IMP', 'cycles':1},
            0x8A:{'fn':self.op_TXA, 'mode':'IMP', 'cycles':1},
            0x9A:{'fn':self.op_TXS, 'mode':'IMP', 'cycles':1},
            0x98:{'fn':self.op_TYA, 'mode':'IMP', 'cycles':1}
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


    def step(self):
        # Get the instruction from the memory location indicated with our program counter
        insptr = self.memory[self.pc]
        # Run the method that matches the value we just fetched
        if self.debug:
            print("Running %s found at %s" % (hex(ins),hex(self.pc)))
            self.show_registers()
        
        ins = self.instructions[insptr]
        operand = None
        if ins['mode']=='ZPG':
            operand = self.memory[self.memory[self.pc+1]]
        elif ins['mode']=='ZPY':
            operand = self.memory[self.memory[self.pc+1]+this.y]
        elif ins['mode']=='ABS':
            operand = self.memory[self.pc+1]
        

        ins['fn'](operand)
        self.pc+=ins['cycles']

   
    def op_BRK(self, operand=None):
        self.flag_break=1

    def op_LDA(self, operand):
        self.a=operand

    def op_LDX(self,operand):
        self.x=operand

    def op_STA(self,operand):
        self.memory[operand]=self.a

    def op_STX(self,operand):
        self.memory[operand]=self.x

    def op_ADC(self,operand):
        pass

    def op_AND(self,operand):
        pass

    def op_ASL(self,operand):
        pass

    def op_BIT(self,operand):
        pass

    def op_BRK(self,operand):
        pass

    def op_CLC(self,operand):
        pass

    def op_CLD(self,operand):
        pass

    def op_CLI(self,operand):
        pass

    def op_CLV(self,operand):
        pass

    def op_CMP(self,operand):
        pass

    def op_CPX(self,operand):
        pass

    def op_CPY(self,operand):
        pass

    def op_DEC(self,operand):
        pass

    def op_DEX(self,operand):
        pass

    def op_DEY(self,operand):
        pass

    def op_EOR(self,operand):
        pass

    def op_INC(self,operand):
        pass

    def op_INX(self,operand):
        pass

    def op_INY(self,operand):
        pass

    def op_JMP(self,operand):
        pass

    def op_JSR(self,operand):
        pass

    def op_LDY(self,operand):
        pass

    def op_LSR(self,operand):
        pass

    def op_NOP(self,operand):
        pass

    def op_ORA(self,operand):
        pass

    def op_PHA(self,operand):
        pass

    def op_PHP(self,operand):
        pass

    def op_PLA(self,operand):
        pass

    def op_PLP(self,operand):
        pass

    def op_ROL(self,operand):
        pass

    def op_ROR(self,operand):
        pass

    def op_RTI(self,operand):
        pass

    def op_RTS(self,operand):
        pass

    def op_SBC(self,operand):
        pass

    def op_SEC(self,operand):
        pass

    def op_SED(self,operand):
        pass

    def op_SEI(self,operand):
        pass

    def op_STY(self,operand):
        pass

    def op_TAX(self,operand):
        pass

    def op_TAY(self,operand):
        pass

    def op_TSX(self,operand):
        pass

    def op_TXA(self,operand):
        pass

    def op_TXS(self,operand):
        pass

    def op_TYA(self,operand):
        pass
