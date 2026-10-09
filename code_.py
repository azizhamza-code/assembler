class code:
    def __init__(self):
        pass


    def dest(self, dest: str):
        """
        Returns the binary code of the dest mnemonic.
        """
        if dest is None:
            return "000"
        elif dest == "M":
            return "001"
        elif dest == "D":
            return "010"
        elif dest == "MD" or dest == "DM":
            return "011"
        elif dest == "A":
            return "100"
        elif dest == "AM" or dest == "MA":
            return "101"
        elif dest == "AD" or dest == "DA":
            return "110"
        elif dest == "AMD" or dest == "ADM" or dest == "MAD" or dest == "MDA" or dest == "DAM" or dest == "DMA":
            return "111"
        else:
            raise ValueError(f"Invalid dest mnemonic: {dest}")

    def jump(self, jump: str):
        """
        Returns the binary code of the jump mnemonic.
        """
        if jump is None:
            return "000"
        elif jump == "JGT":
            return "001"
        elif jump == "JEQ":
            return "010"
        elif jump == "JGE":
            return "011"
        elif jump == "JLT":
            return "100"
        elif jump == "JNE":
            return "101"
        elif jump == "JLE":
            return "110"
        elif jump == "JMP":
            return "111"
        else:
            raise ValueError(f"Invalid jump mnemonic: {jump}")

    def comp(self, comp: str):
        """
        Returns the binary code of the comp mnemonic.
        Assumes a=0 unless M is used (where a=1).
        Only the 6 bits (ignoring 'a') encoding are implemented here for simplicity.
        """
        # a=0 computations
        comp_table = {
            "0"  : "101010",
            "1"  : "111111",
            "-1" : "111010",
            "D"  : "001100",
            "A"  : "110000",
            "!D" : "001101",
            "!A" : "110001",
            "-D" : "001111",
            "-A" : "110011",
            "D+1": "011111",
            "A+1": "110111",
            "D-1": "001110",
            "A-1": "110010",
            "D+A": "000010",
            "D-A": "010011",
            "A-D": "000111",
            "D&A": "000000",
            "D|A": "010101",
            # a=1 computations (replace A with M)
            "M"  : "110000",
            "!M" : "110001",
            "-M" : "110011",
            "M+1": "110111",
            "M-1": "110010",
            "D+M": "000010",
            "D-M": "010011",
            "M-D": "000111",
            "D&M": "000000",
            "D|M": "010101",
        }

        if comp in comp_table:
            return comp_table[comp]
        else:
            raise ValueError(f"Invalid comp mnemonic: {comp}")

   
        
            