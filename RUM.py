#RUM (bRainfUck iMproved) 0.2
#an "enhanced" BrainFuck interpreter in Python
#by Steve Johnson (http://www.steveasleep.com/)
#getchar() stolen from pybrain4 (http://gufffluff.blogspot.com/)

import sys, string

class SteveFucker(object):
    def __init__(self, tape_len=0, eof=""):
        super(SteveFucker, self).__init__()
        self.tape_len = tape_len
        self.eof = eof
    
    def eval(self, program_text):    
        self.program = program_text
        self.pgm_len = len(self.program)
        self.procedures = {}
        if self.tape_len > 0:
            self.tape = [0] * self.tape_len
        else:
            self.tape = [0] * 10
        self.ptr_pos = 0
        self.pgm_pos = 0
        self.reps = 0
        self.return_positions = []
        self.string = ""
        
        cmd_dict = {
            '.': self.put_char,
            ',': self.get_char,
            '(': self.put_proc,
            '"': self.put_string
        }
        while self.pgm_pos < self.pgm_len and self.pgm_pos >= 0:
            c = self.program[self.pgm_pos]
            if c in cmd_dict:
                cmd_dict[c]()
            elif c == '>':
                self.ptr_pos += self.get_reps()
                self.ptr_pos = self.check_tape(self.ptr_pos)
            elif c == '<':
                self.ptr_pos -= self.get_reps()
                self.ptr_pos = self.check_tape(self.ptr_pos)
            elif c == '+':
                self.tape[self.ptr_pos] += self.get_reps()
            elif c == '-':
                self.tape[self.ptr_pos] -= self.get_reps()
            elif c == ':':
                self.return_positions.append(self.pgm_pos)
                self.pgm_pos = self.procedures[self.tape[self.ptr_pos]]
            elif c == ')':
                self.pgm_pos = self.return_positions.pop()
            elif c == ']':
                if self.tape[self.ptr_pos] != 0:
                    self.go_to_matching_bracket()
            elif c == '[':
                if self.tape[self.ptr_pos] == 0:
                    self.go_to_matching_bracket()
            elif c in string.digits:
                if self.reps == 0:
                    self.reps = int(c)
                else:
                    self.reps *= 10
                    self.reps += int(c)
            elif c == "#":
                while self.program[self.pgm_pos] != "\n" \
                        and self.pgm_pos < self.pgm_len:
                    self.pgm_pos += 1
            self.pgm_pos += 1
        sys.stdout.write('\n')
    
    def check_tape(self, pos):
        if pos < len(self.tape):
            return pos
        if self.tape_len > 0:
            return pos % self.tape_len
        self.tape.extend([0] * len(self.tape))
        return pos
    
    def put_char(self):
        if self.tape[self.ptr_pos] in range(256):
            sys.stdout.write(chr(self.tape[self.ptr_pos]))
        else:
            sys.stdout.write(str(self.tape[self.ptr_pos]))
    
    def get_char(self):    
        if len(self.string) > 0:
            char_in = ord(self.string[0])
            self.string = self.string[1:]
        else:
            char_in = ord(getchar())
        if char_in == 3:
            self.pgm_pos = self.pgm_len
        if char_in == 4:
            if self.eof == "0":
                self.tape[self.ptr_pos] = 0
            elif self.eof == "-1":
                self.tape[self.ptr_pos] = -1
        else:
            self.tape[self.ptr_pos] = char_in
    
    def go_to_matching_bracket(self):
        depth = 1
        start = self.pgm_pos
        if self.program[self.pgm_pos] == "]":
            while depth > 0 and self.pgm_pos >= 0:
                self.pgm_pos -= 1
                if self.program[self.pgm_pos] == "]":
                    depth += 1
                elif self.program[self.pgm_pos] == "[":
                    depth -= 1
            if self.pgm_pos < 0:
                print "Missing left bracket to match right at", start
        elif self.program[self.pgm_pos] == "[":
            while depth > 0 and self.pgm_pos < self.pgm_len:
                self.pgm_pos += 1
                if self.program[self.pgm_pos] == "]":
                    depth -= 1
                elif self.program[self.pgm_pos] == "[":
                    depth += 1
            if self.pgm_pos >= self.pgm_len:
                print "Missing right bracket to match left at", start
        self.pgm_pos -= 1
    
    def put_string(self):
        start_pos = self.pgm_pos + 1
        ok = False
        while not ok and self.pgm_pos < self.pgm_len:
            self.pgm_pos += 1
            if self.program[self.pgm_pos] == "\\":
                self.pgm_pos += 1
            else:
                if self.program[self.pgm_pos] == '"':
                    ok = True
        if self.pgm_pos == self.pgm_len:
            print "String not terminated"
        new_str = self.program[start_pos:self.pgm_pos]
        new_str *= self.get_reps()
        if len(self.string) > 1:
            old_str = self.string[:-1]
        else:
            old_str = ""
        self.string = ''.join(
            [old_str, new_str, chr(0)]
        )
    
    def put_proc(self):
        val = self.tape[self.ptr_pos]
        start = self.pgm_pos
        while self.pgm_pos < self.pgm_len \
                and self.program[self.pgm_pos] != ')':
            self.pgm_pos += 1
        if self.pgm_pos >= self.pgm_len:
            print "Right paren not found for left at", start+1
        self.procedures[val] = start
    
    def get_reps(self):
        r = max(1, self.reps)
        self.reps = 0
        return r
    

class _Getch:
    """ Gets a single character from standard input.  
        Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
    
    def __call__(self): 
        return self.impl()
    

class _GetchUnix:
    def __init__(self):
        import tty, sys
    
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    

class _GetchWindows:
    def __init__(self):
        import msvcrt
    
    def __call__(self):
        import msvcrt
        return msvcrt.getch()
    

getchar = _Getch()

if __name__ == "__main__":
    fucker = SteveFucker()
    i = 1
    if sys.argv[i] == '-v':
        i+=1
    fucker.eval(open(sys.argv[i]).read())
    if i == 2: print fucker.tape
