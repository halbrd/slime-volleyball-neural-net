class Ball:
    speed = 2
    grav = -0.3
    
    def __init__(self, _pos, _r):
        self.pos, self.r = _pos, _r
        self.vel = PVector(0, 0)
        
    def update(self):
        self.vel.y -= self.grav
        
        VELOCITY_CAP = 8
        # Cap velocity in either axis at VELOCITY_CAP
        if self.vel.x > VELOCITY_CAP: self.vel.x = VELOCITY_CAP
        if self.vel.y > VELOCITY_CAP: self.vel.y = VELOCITY_CAP
        
        self.pos += self.vel * self.speed
        
    def draw(self):
        fill(50, 200, 100)
        ellipseMode(RADIUS)
        ellipse(self.pos.x, self.pos.y, self.r, self.r)