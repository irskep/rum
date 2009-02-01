import pyglet, RUM, sys
from pyglet.window import key

class RumBottle(pyglet.window.Window):
    def __init__(self, program):
        super(RumBottle, self).__init__()
        self.interp = RUM.RumSwigger()
        self.interp.init(program)
        
        self.tape_label = pyglet.text.Label(
            text="", font_name='Monaco',
            x=5, y=10, font_size=10,
            color=(0,0,0,255)
        )
        self.message_label = pyglet.text.Label(
            text="", font_name='Monaco',
            font_size=10, color=(0,0,0,255), anchor_x='left',
            x=5, y=35
        )
        self.code_label_1 = pyglet.text.Label(
            text="", font_name='Monaco',
            font_size=10, color=(0,0,0,255), anchor_x='right',
            x=self.width/2-10, y=self.height/2
        )
        self.code_label_2 = pyglet.text.Label(
            text="*", font_name='Monaco',
            font_size=10, color=(0,0,0,255), anchor_x='center',
            x=self.width/2, y=self.height/2
        )
        self.code_label_3 = pyglet.text.Label(
            text="", font_name='Monaco',
            font_size=10, color=(0,0,0,255), anchor_x='left',
            x=self.width/2+10, y=self.height/2
        )
        self.on_key_release(0, 0)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.RETURN:
            self.interp.step()
            if modifiers & key.MOD_SHIFT:
                for i in range(4):
                    self.interp.step()
        if symbol == key.A:
            self.tape_label.x += 30
        if symbol == key.D:
            self.tape_label.x -= 30
    
    def on_key_release(self, symbol, modifiers):
        self.tape_label.text = repr(self.interp.tape)
        start = max(0, self.interp.pgm_pos-50)
        end = min(self.interp.pgm_len, self.interp.pgm_pos+50)
        self.code_label_1.text = self.interp.program[start:self.interp.pgm_pos]
        self.code_label_3.text = self.interp.program[self.interp.pgm_pos:end]
        self.message_label.text = self.interp.message
    
    def on_draw(self):
        pyglet.gl.glClearColor(1,1,1,1)
        self.clear()
        self.tape_label.draw()
        self.code_label_1.draw()
        self.code_label_2.draw()
        self.code_label_3.draw()
        self.message_label.draw()
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        p = sys.argv[1]
    else:
        p = "examples/hello2.b"
    bottle = RumBottle(open(p).read())
    pyglet.app.run()