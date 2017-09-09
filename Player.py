class Player:
    # Static variables
    speed = 10
    grav = -0.5
    r = 60
    
    def __init__(self, _pos, _leftSide, _bot):
        # leftSide determines which side of the net the player is on
        # bot is the Bot instance that controls the player, or None if the player is a human
        self.pos, self.leftSide, self.bot = _pos, _leftSide, _bot
        self.vel = PVector(0, 0)
        # Button states - left, right, jump
        self.left = False
        self.right = False
        self.jump = False
        
        self.points = 0
        
    def update(self, keysDown, botInputs):
        # Get control input
        if self.bot is not None:
            self.getNeuralInput(botInputs)
        else:
            self.getHumanInput(keysDown)
        
        # Respond to input
        self.vel.x = 0
        
        if self.left:
            self.vel.x -= self.speed
        if self.right:
            self.vel.x += self.speed
        if self.jump and self.pos.y >= height:
            self.vel.y = -12
            
        
        # Apply movement
        self.vel.y -= self.grav
        self.pos += self.vel
        
        # Don't fall off the bottom of the screen
        if self.pos.y >= height:
            self.pos.y = height
            self.vel.y = 0
            
        # Don't go past side bounds
        playerLeft = self.pos.x - self.r
        playerRight = self.pos.x + self.r
        
        # Don't go past fence
        if self.leftSide:
            leftBound = 0
            rightBound = width / 2 - 5    # Fence width = 10 (hardcoded)
        else:
            leftBound = width / 2 + 5
            rightBound = width    
        if playerLeft < leftBound:
            self.pos.x = leftBound + self.r
        elif playerRight > rightBound:
            self.pos.x = rightBound - self.r
            
            
        # Draw neural net
        if self.bot is not None:
            perceptronsX = (3 * width / 8) if self.leftSide else (5 * width / 8)
            pLeftY = 100
            pRightY = 200
            pJumpY = 300
            
            # Draw inputs
            inputsX = (width / 8) if self.leftSide else (7 * width / 8)
            inputsLabelX = inputsX + (15 * (-1 if self.leftSide else 1))
            inputStart = 45
            inputSpacing = 45
            inputsY = [inputStart + (inputSpacing * i) for i in range(8)]
            # This array stores the y positions of the inputs to render in the order ballXPos, ballYPos, ballXVel, ballYVel, playerXPos, playerYPos, playerXVel, playerYVel
            fill(0)
            textSize(12)
            ellipseMode(CENTER)
            for yPos in inputsY:
                ellipse(inputsX, yPos, 10, 10)    # Input dot
            
            # Draw input labels
            textAlign(RIGHT if self.leftSide else LEFT, CENTER)
            labels = ["b.x", "b.y", "b.vx", "b.vy", "p.x", "p.y", "p.vx", "p.vy"]
            for i in range(len(labels)):
                text(labels[i] + "\n" + str(round(botInputs[i], 2)), inputsLabelX, inputsY[i])    # Input label
            
            # Draw lines between inputs and perceptrons
            for i in range(len(inputsY)):
                inputYPos = inputsY[i]
                stroke((botInputs[i] * 255/2) + 255/2)    # Scale inputs from (-1, 1) to (0, 255)
                for perceptronYPos in [100, 200, 300]:
                    line(inputsX, inputYPos, perceptronsX, perceptronYPos)
            noStroke()
            
            # Draw perceptron labels
            fill(0)
            textSize(24)
            textAlign(CENTER, CENTER)
            text("Left", perceptronsX, pLeftY - 50)
            text("Right", perceptronsX, pRightY - 50)
            text("Jump", perceptronsX, pJumpY - 50)
            
            ellipseMode(CENTER)
            
            # Draw left perceptron
            fill(50 if self.left else 200)
            ellipse(perceptronsX, pLeftY, 30, 30)
            
            # Draw right perceptron
            fill(50 if self.right else 200)
            ellipse(perceptronsX, pRightY, 30, 30)
            
            # Draw jump perceptron
            fill(50 if self.jump else 200)
            ellipse(perceptronsX, pJumpY, 30, 30)
        
    def draw(self):
        fill(0)
        ellipseMode(RADIUS)
        ellipse(self.pos.x, self.pos.y, self.r, self.r)
        fill(255)
        noStroke()
        rectMode(CENTER)
        rect(self.pos.x, self.pos.y + 1 + self.r / 2, 2 * self.r, self.r + 2)
        
            
    def pressLeft(self):
        self.left = True
    
    def releaseLeft(self):
        self.left = False
        
    def pressRight(self):
        self.right = True
        
    def releaseRight(self):
        self.right = False
        
    def pressJump(self):
        self.jump = True
    
    def releaseJump(self):
        self.jump = False
        
    # Allow player to be controlled by relative direction, so bots can play either side of the fence 
        
    def pressForward(self):
        if self.leftSide:
            self.pressRight()
        else:
            self.pressLeft()
        
    def releaseForward(self):
        if self.leftSide:
            self.releaseRight()
        else:
            self.releaseLeft()

    def pressBackward(self):
        if self.leftSide:
            self.pressLeft()
        else:
            self.pressRight()
        
    def releaseBackward(self):
        if self.leftSide:
            self.releaseLeft()
        else:
            self.releaseRight()
        
    def getHumanInput(self, keysDown):
        if self.leftSide:
            leftKey = "a"
            rightKey = "d"
            jumpKey = "w" 
        else:
            leftKey = "l"
            rightKey = "'"
            jumpKey = "p"
        
        if leftKey in keysDown and keysDown[leftKey]:
            self.pressLeft()
        else:
            self.releaseLeft()
            
        if rightKey in keysDown and keysDown[rightKey]:
            self.pressRight()
        else:
            self.releaseRight()
            
        if jumpKey in keysDown and keysDown[jumpKey]:
            self.pressJump()
        else:
            self.releaseJump()
            
        
    def getNeuralInput(self, inputs):
        if self.bot.pForward.feedForward(inputs) == 1:
            #print("+fw")
            self.pressForward()
        else:
            #print("-fw")
            self.releaseForward()
            
        if self.bot.pBackward.feedForward(inputs) == 1:
            #print("+bw")
            self.pressBackward()
        else:
            #print("-bw")
            self.releaseBackward()
            
        if self.bot.pJump.feedForward(inputs) == 1:
            #print("+jp")
            self.pressJump()
        else:
            #print("-jp")
            self.releaseJump()