import pyglet, RUM, sys
from pyglet.window import key

class RumBottle(pyglet.window.Window):
    def __init__(self, program):
        super(RumBottle, self).__init__()
        self.interp = RUM.RumSwigger()
        self.interp.init(program)
        
        self.label = pyglet.text.Label(
            text=repr(self.interp.tape), font_size=24,
            x=self.width/2, y=self.height/2,
            color=(0,0,0,255)
        )
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.RETURN:
            self.interp.step()
    
    def on_key_relese(self, symbol, modifiers):
        self.label.text = repr(self.interp.tape)
    
    def on_draw(self):
        pyglet.gl.glClearColor(1,1,1,1)
        self.clear()
        self.label.draw()
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        p = sys.argv[1]
    else:
        p = "examples/unlimited_tape.py"
    bottle = RumBottle(open(p).read())
    pyglet.app.run()