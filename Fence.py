class Fence:
    def __init__(self, _x, _y, _width, _height):
        self.x = _x
        self.y = _y
        self.width = _width
        self.height = _height
        
    def draw(self):
        fill(0)
        rectMode(CENTER)
        rect(self.x, self.y, self.width, self.height)