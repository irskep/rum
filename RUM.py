#RUM (bRainfUck iMproved) 0.2
#an "enhanced" BrainFuck interpreter in Python
#by Steve Johnson (http://www.steveasleep.com/)
#getchar() stolen from pybrain4 (http://gufffluff.blogspot.com/)

import sys, string
from getch import getchar

class RumSwigger(object):
    def __init__(self, tape_len=0, eof="", cell_size=0):
        super(RumSwigger, self).__init__()
        self.tape_len = tape_len
        self.eof = eof
        self.cell_size = cell_size
    
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
            '>': self.inc_ptr,
            '<': self.dec_ptr,
            '+': self.inc_tape,
            '-': self.dec_tape,
            '.': self.put_char,
            ',': self.get_char,
            '[': self.check_bracket,
            ']': self.check_bracket,
            '(': self.put_proc,
            ')': self.end_proc,
            ':': self.call_proc,
            '"': self.put_string,
            '#': self.skip_comment
        }
        while self.pgm_pos < self.pgm_len and self.pgm_pos >= 0:
            c = self.program[self.pgm_pos]
            if c in cmd_dict:
                cmd_dict[c]()
            elif c in string.digits:
                if self.reps == 0:
                    self.reps = int(c)
                else:
                    self.reps *= 10
                    self.reps += int(c)
            self.pgm_pos += 1
        sys.stdout.write('\n')
    
    def check_tape(self, pos):
        if pos < len(self.tape):
            return pos
        if self.tape_len > 0:
            return pos % self.tape_len
        self.tape.extend([0] * len(self.tape))
        return pos
    
    def inc_ptr(self):
        self.ptr_pos += self.get_reps()
        self.ptr_pos = self.check_tape(self.ptr_pos)
    
    def dec_ptr(self):
        self.ptr_pos -= self.get_reps()
        self.ptr_pos = self.check_tape(self.ptr_pos)
    
    def inc_tape(self):
        v = self.tape[self.ptr_pos] + self.get_reps()
        if self.cell_size > 0:
            v = v % self.cell_size
        self.tape[self.ptr_pos] = v
    
    def dec_tape(self):
        v = self.tape[self.ptr_pos] - self.get_reps()
        if self.cell_size > 0:
            v = v % self.cell_size
        self.tape[self.ptr_pos] = v
    
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
    
    def check_bracket(self):
        depth = 1
        start = self.pgm_pos
        if self.program[self.pgm_pos] == "]":
            if self.tape[self.ptr_pos] == 0:
                return
            while depth > 0 and self.pgm_pos >= 0:
                self.pgm_pos -= 1
                if self.program[self.pgm_pos] == "]":
                    depth += 1
                elif self.program[self.pgm_pos] == "[":
                    depth -= 1
            if self.pgm_pos < 0:
                print "Missing left bracket to match right at", start
        elif self.program[self.pgm_pos] == "[":
            if self.tape[self.ptr_pos] != 0:
                return
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
    
    def call_proc(self):
        self.return_positions.append(self.pgm_pos)
        proc_pos = self.procedures[self.tape[self.ptr_pos]]
        while self.reps > 1:
            self.return_positions.append(proc_pos)
            self.reps -= 1
        self.reps = 0
        self.pgm_pos = proc_pos
    
    def end_proc(self):
        self.pgm_pos = self.return_positions.pop()
    
    def skip_comment(self):
        while self.pgm_pos < self.pgm_len \
                and self.program[self.pgm_pos] != "\n":
            self.pgm_pos += 1
    
    def get_reps(self):
        r = max(1, self.reps)
        self.reps = 0
        return r
    

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option(
        '-l', '--length', dest='tape_len', default=0, type='int', 
        help='Tape length.'
    )
    parser.add_option(
        '-e', '--eof', dest='eof', default="", type='string', 
        help='Set to 0, -1, or leave blank for desired EOF behavior.'
    )
    parser.add_option(
        '-s', '--size', dest='size', default=0, type='int', 
        help='Individual cell size. Set to 0 for unbounded.'
    )
    parser.add_option(
        "-v", "--verbose", dest="verbose", default=False, action="store_true",
        help="Print tape to console when finished."
    )
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Incorrect number of arguments.")
        quit()
    fucker = RumSwigger(opts.tape_len, opts.eof, opts.size)
    fucker.eval(open(args[0]).read())
    if opts.verbose: print fucker.tape
