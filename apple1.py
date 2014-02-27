from cpu import Cpu

if __name__ == "__main__":
    proc = Cpu()
    proc.memory = [
        6502, # Store the integer of 6502 in location 0x00
        42,   # Store the integer of 42 in location 0x01
        0xA5, 0x00,  # LDA 00 ; Store the value at 0x00 in the A register
        0xA6, 0x01,  # LDX 01 ; Store the value at 0x01 in the X register
        0x85, 0x01,  # STA 01 ; Store the value in the A register in location 0x01
        0x86, 0x00,  # STX 00 ; Store the value in the X register in location 0x00
        00           # BRK    ; End our glorious program
    ]

    # our first instruction is LDA, which is at location 0x02, let's start there
    proc.pc=0x02

    # Examine the memory before we start
    print("Before -- 0x00: %d 0x01: %d" % (proc.memory[0x0], proc.memory[0x1]))
    proc.run()

    # The results.  The values at 0x0 and 0x1 should be swapped
    print("After  -- 0x00: %d 0x01: %d" % (proc.memory[0x0], proc.memory[0x1]))

