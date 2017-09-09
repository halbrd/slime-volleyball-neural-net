from Fence import Fence
from Ball import Ball
from Player import Player
from NeuralNet import Bot

class Game:
    def __init__(self, bot1, bot2):
        fenceTop = 50
        self.fence = Fence(width / 2, height - fenceTop / 2, 10, fenceTop)
        self.ball = Ball(PVector(width / 2, 100), 25)
        self.player1 = Player(PVector(width / 4, height), True, bot1)
        self.player2 = Player(PVector(3 * width / 4, height), False, bot2)
        self.justReset = False
        
    def update(self, keysDown):
        if self.justReset:
            self.justReset = False
            
            # Reset inputs to prevent jumps from being preserved across rounds
            if keysDown is not None:
                for key in keysDown:
                    keysDown[key] = False
                                
            delay(1000)
            
        self.player1.update(keysDown, self.getBotInputs(True))
        self.player2.update(keysDown, self.getBotInputs(False))
        self.ball.update()
        self.updateCollisions()
        
    def draw(self):
        self.player1.draw()
        self.player2.draw()
        self.fence.draw()
        self.ball.draw()
        self.printScores()
        
    def printScores(self):
        textSize(16)
        textAlign(LEFT, TOP)
        fill(0)
        text("Player 1: " + str(self.player1.points) + "\nPlayer 2: " + str(self.player2.points), 10, 10)
        
    def updateCollisions(self):
        # Set shorthand values
        fenceTop = height - self.fence.height    # Y value of top of fence
        fenceLeft = (width / 2) - (self.fence.width / 2)    # X value of left side of fence
        fenceRight = (width / 2) + (self.fence.width / 2)    # X value of right side of fence
        ballTop = self.ball.pos.y - self.ball.r    # Y value of top of ball
        ballBottom = self.ball.pos.y + self.ball.r    # Y value of bottom of ball
        ballLeft = self.ball.pos.x - self.ball.r    # X value of left side of ball
        ballRight = self.ball.pos.x + self.ball.r    # X value of right side of ball
        r = self.ball.r    # Radius of ball
        ballMidX = self.ball.pos.x    # X value of ball centre
        ballMidY = self.ball.pos.y    # Y value of ball centre
        
        # Ball - Floor
        if ballBottom >= height:
            self.ball.vel.y *= -1
            self.ball.pos.y = height - r
            
            # Reset and give points
            self.reset(self.ball.pos.x < width / 2)
            
        # Ball - Ceiling
        if ballTop <= 0:
            self.ball.vel.y *= -1
            self.ball.pos.y = r
            
        # Ball - Left wall
        if ballLeft <= 0:
            self.ball.vel.x *= -1
            self.ball.pos.x = r
            
        # Ball - Right wall
        if ballRight >= width:
            self.ball.vel.x *= -1
            self.ball.pos.x = width - r        
            
        # Ball - Fence top
        if fenceLeft < ballMidX < fenceRight and fenceTop - r < ballMidY < fenceTop:
            self.ball.pos.y = fenceTop - r
            self.ball.vel.y *= -1
        
        # Ball - Fence top left
        if fenceLeft - r < ballMidX < fenceLeft and fenceTop - r < ballMidY < fenceTop:
            localX = ballMidX - fenceLeft - r
            localY = ballMidY - fenceTop - r
            
            if localX <= localY:
                self.ball.vel.x *= -1
                self.ball.pos.x = fenceLeft - r
            if localX >= localY:
                self.ball.pos.y = fenceTop - r
                self.ball.vel.y *= -1                
            
        # Ball - Fence top right
        if fenceRight < ballMidX < fenceRight + r and fenceTop - r < ballMidY < fenceTop:
            localX = abs(ballMidX - fenceRight - r)
            localY = ballMidY - fenceTop - r
            
            if localX <= localY:
                self.ball.vel.x *= -1
                self.ball.pos.x = fenceRight + r
            if localX >= localY:
                self.ball.pos.y = fenceTop - r
                self.ball.vel.y *= -1   
            
        # Ball - Fence left
        if fenceLeft - r < ballMidX < width / 2 and fenceTop < ballMidY:
            self.ball.pos.x = fenceLeft - r
            self.ball.vel.x *= -1
            
        # Ball - Fence right
        if width / 2 < ballMidX < fenceRight + r and fenceTop < ballMidY:
            self.ball.pos.x = fenceRight + r
            self.ball.vel.x *= -1
        
        # Sphere-on-sphere bounce code adapted from https://processing.org/examples/bouncybubbles.html
        
        SPRING = 1
        
        # Ball - player 1
        dx = self.ball.pos.x - self.player1.pos.x
        dy = self.ball.pos.y - self.player1.pos.y
        distance = sqrt(dx * dx + dy * dy)
        minDist = self.ball.r + self.player1.r    # The distance at or below which they would be touching
        if distance < minDist:
            angle = atan2(dy, dx)
            targetX = self.player1.pos.x + cos(angle) * minDist
            targetY = self.player1.pos.y + sin(angle) * minDist
            ax = (targetX - self.ball.pos.x) * SPRING
            ay = (targetY - self.ball.pos.y) * SPRING
            self.ball.vel.x += ax
            self.ball.vel.y += ay
        
        # Ball - player 2
        dx = self.ball.pos.x - self.player2.pos.x
        dy = self.ball.pos.y - self.player2.pos.y
        distance = sqrt(dx * dx + dy * dy)
        minDist = self.ball.r + self.player2.r
        if distance < minDist:
            angle = atan2(dy, dx)
            targetX = self.player2.pos.x + cos(angle) * minDist
            targetY = self.player2.pos.y + sin(angle) * minDist
            ax = (targetX - self.ball.pos.x) * SPRING
            ay = (targetY - self.ball.pos.y) * SPRING
            self.ball.vel.x += ax
            self.ball.vel.y += ay

        
    def reset(self, left):
        self.justReset = True
        
        if left:
            self.player2.points += 1
        else:
            self.player1.points += 1
            
        textSize(16)
        textAlign(CENTER, CENTER)
        fill(0)
        text("Player " + ("2" if left else "1") + " scores!", width / 2, height / 2)
    
        
        self.player1.pos = PVector(width / 4, height)
        self.player2.pos = PVector(3 * width / 4, height)
        #self.ball = Ball(PVector((width / 4) if left else (3 * width / 4), 100), 25)    # This would place the ball above the losing player; disabled for simpler bot evolution
        self.ball = Ball(PVector(width / 2, 100), 25)

        
    def getBotInputs(self, left):
        inputs = []
        inputs += [self.ball.pos.x, self.ball.pos.y, self.ball.vel.x, self.ball.vel.y]
        if left:
            theBot = self.player1
        else:
            theBot = self.player2
        inputs += [theBot.pos.x, theBot.pos.y, theBot.vel.x, theBot.vel.y]
        
        # At this point the bot inputs will have the absolute values of the relevant positions;
        # we want positions relative to the fence, so that the bot will get the same inputs regardless
        # of what side of the net it's on. 
        
        # First we subtract the difference between x = 0 and the fence, so that if the ball is
        # on the fence, its x position = 0, on our side it's negative, and on their side its positive.
        
        for i in [0, 4]:    # Change the ball's x pos and the player's x pos (NOTE: loops on i=0 and 4, not 0 to 4, which would be `for i in range(0, 4)`)
            inputs[i] -= width / 2
            
        # Now we do a similar thing with the y values (so halfway down the screen is y = 0, done for scaling of input from roughly -1 to 1)
        for i in [1, 5]:
            inputs[i] -= height / 2
        
        # Next we need to reflect the x values about the y axis at x = fence if the bot player is
        # on the right
        if not left:
            for i in [0, 2, 4, 6]:
                inputs[i] *= -1
        
        VELOCITY_CAP = 8    # This needs to be the same as the VELOCITY_CAP in Ball.py
        # Now we want to scale everything to roughly the same range (around -1 to 1), otherwise our input 
        # magnitudes would be totally arbitrary (the difference between xPos = 0 vs 20 is completely 
        # different to xVel = 0 vs 20)
        inputsScaler = [width / 2, height / 2, VELOCITY_CAP, VELOCITY_CAP, width / 2, height / 2, VELOCITY_CAP, VELOCITY_CAP]
        for i in range(len(inputs)):
            inputs[i] /= inputsScaler[i]
        
        #print("BallX:" + str(inputs[0]))
        #print("BallY:" + str(inputs[1]))
        
        return inputs

        
        