import io
import code

class Parser:
    def __init__(self, source_path):
        self.f = open(source_path, 'r')
        self.has_more = True        

    def has_more_lignes(self):
        return self.has_more

    def advance(self):
        assert self.has_more == True
        self.f.readline()
        if peek_line(self.f) == "":
            self.has_more = False

    def _current(self):
        if peek_line(self.f).startswith("//"):
            self.advance()
            self._current()
        if ("//") in peek_line(self.f):
            line = peek_line(self.f).split("//", 1)[0].strip()
            return line
        first_line = peek_line(self.f)
        return first_line
    
    def symbol(self):
        assert self.instruction_type in ["A_INSTRUCTION" , "C_INSTRUCTION"]
        if self.instruction_type == "A_INSTRUCTION":
            res = self._current()
            return res[1:]
        else: 
            return self._current()[1:-1]
    
    def dest(self):
        assert self.instruction_type == "C_INSTRUCTION"
        if '=' in self._current():
            return self._current().split("=")[0]
        else:
            return None

    def jump(self):
        assert self.instruction_type == "C_INSTRUCTION"
        if ';' in self._current():
            return self._current().split(";")[-1]
        else:
            return None
    
    def comp(self):
        assert self.instruction_type == "C_INSTRUCTION"
        sub = self._current()
        if '=' in self._current():
            sub = sub.split("=")[-1].strip()
        if ';' in self._current():
            sub = sub.split(";")[0]
        return sub

    @property
    def instruction_type(self):
        current = self._current()
        if any([sign_c in current  for sign_c in ["=", ";"]]):
            return "C_INSTRUCTION"
        elif current.startswith("@"):
            return "A_INSTRUCTION"
        elif current.startswith("("):
            return "L_INSTRUCTION"
    
def peek_line(file_obj: io.TextIOBase) -> str:
    pos = file_obj.tell()          
    line = file_obj.readline()     
    file_obj.seek(pos)            
    return line