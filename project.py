import turtle
import random
import time

CameraX = 0.0
CameraY = 0.0
SpriteQueue = []
Colliders = []
deltalogs = []
deltalogsum = 0.0
Screenshake = 0.0
Win = False

oldtime = time.monotonic()
delta = 1.0
carl = turtle.Turtle()
carl.hideturtle()
carl.penup()
carl.screen.clear()
carl.screen.screensize(960, 540)

LevelObjects = []

Input = {
    "Jump": False,
    "Left": False,
    "Right": False
}
    
def updateInput(): # Work with turtle keyboard listener to get inputs

    turtle.listen()

    turtle.onkeypress(UpPressed, "w")
    turtle.onkeypress(LeftPressed, "a")
    turtle.onkeypress(RightPressed, "d")

    turtle.onkeyrelease(UpReleased, "w")
    turtle.onkeyrelease(LeftReleased, "a")
    turtle.onkeyrelease(RightReleased, "d")

def UpPressed():
    Input["Jump"] = True

def UpReleased():
    Input["Jump"] = False

def LeftPressed():
    Input["Left"] = True

def LeftReleased():
    Input["Left"] = False

def RightPressed():
    Input["Right"] = True

def RightReleased():
    Input["Right"] = False


class Sprite: # Base class for all sprites, rendered every frame
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.Direction = 0.0
        self.Visible = True
        self.Background = False
        SpriteQueue.append(self)
        
    
    def setpos(self, X, Y): # Set turtle's position in regard to camera coords and sprite coords
        carl.goto(X + self.X - CameraX, Y + self.Y - CameraY)
    
    def draw(self): # Override with turtle drawing instructions
        pass

class GrassSprite(Sprite): # A green square for grass tiles
    def draw(self):
        carl.pensize(1)
        self.setpos(-16,16)
        carl.color("green")
        carl.begin_fill()
        self.setpos(16,16)
        self.setpos(16,-16)
        self.setpos(-16,-16)
        carl.end_fill()

class WinSprite(Sprite): # A light green square for victory tiles
    def draw(self):
        carl.pensize(1)
        self.setpos(-16,16)
        carl.color("light green")
        carl.begin_fill()
        self.setpos(16,16)
        self.setpos(16,-16)
        self.setpos(-16,-16)
        carl.end_fill()

class PlayerSprite(Sprite): # A blue square for the player
    def draw(self):
        carl.pensize(1)
        self.setpos(-16,16)
        carl.color("blue")
        carl.begin_fill()
        self.setpos(16,16)
        self.setpos(16,-16)
        self.setpos(-16,-16)
        carl.end_fill()

class EnemySprite(Sprite): # A red square for enemies
    def draw(self):
        carl.pensize(1)
        self.setpos(-16,16)
        carl.color("red")
        carl.begin_fill()
        self.setpos(16,16)
        self.setpos(16,-16)
        self.setpos(-16,-16)
        carl.end_fill()

class SpikeSprite(Sprite): # A gray triangle for spikes
    def draw(self):
        self.setpos(-16, -16)
        carl.color("gray")
        carl.pensize(1)
        carl.begin_fill()
        self.setpos(16, -16)
        self.setpos(0, 16)
        self.setpos(-16, -16)
        carl.end_fill()

class SquareCollider: # Base class for hitboxes
    def __init__(self, W, H, S):
        self.Width = W
        self.Height = H
        self.X = 0.0
        self.Y = 0.0
        self.Solid = S
        Colliders.append(self)
    
    def overlap(self, upper1, lower1, upper2, lower2): # Check if 2 ranges overlap
        if lower1 < upper2 and upper1 > lower2:
            return True
        else:
            return False
    
    def collideX(self, motion): # Get the collisions along the X axis, return a tuple with the solid collision and a list of nonsolid collisions
        solidCollision = (None, motion)
        nonsolids = []

        for collider in Colliders:
            if (not collider == self) and self.overlap(
                (self.Height * 0.5) + self.Y,
                (self.Height * -0.5) + self.Y,
                (collider.Height * 0.5) + collider.Y,
                (collider.Height * -0.5) + collider.Y
                ):
                if collider.Solid:
                    if motion > 0.0:
                        moveover = ((collider.Width * -0.5) + collider.X) - ((self.Width * 0.5) + self.X)
                        if self.overlap(
                            (self.Width * 0.5) + self.X + motion,
                            (self.Width * -0.5) + self.X,
                            (collider.Width * 0.5) + collider.X,
                            (collider.Width * -0.5) + collider.X
                        ) and solidCollision[1] > moveover:
                            solidCollision = (collider, moveover)
                    else:
                        moveover = ((collider.Width * 0.5) + collider.X) - ((self.Width * -0.5) + self.X)
                        if self.overlap(
                            (self.Width * 0.5) + self.X,
                            (self.Width * -0.5) + self.X + motion,
                            (collider.Width * 0.5) + collider.X,
                            (collider.Width * -0.5) + collider.X
                        ) and solidCollision[1] < moveover:
                            solidCollision = (collider, moveover)
                else:
                    nonsolids.append(collider)

        temp = nonsolids
        count = 0
        for i in range(len(temp)):
            moveover = solidCollision[1]
            print(len(temp))
            print(temp)
            print(temp[1])
            if not((moveover > 0.0 and self.overlap(
                (self.Width * 0.5) + self.X + moveover,
                (self.Width * -0.5) + self.X,
                (temp[count].Width * 0.5) + temp[count].X,
                (temp[count].Width * -0.5) + temp[count].X
            )) or (moveover <= 0 and self.overlap(
                (self.Width * 0.5) + self.X,
                (self.Width * -0.5) + self.X + moveover,
                (temp[count].Width * 0.5) + temp[count].X,
                (temp[count].Width * -0.5) + temp[count].X
            ))):
                temp2 = temp[count]
                nonsolids.remove(temp2)
            count += 1
        return (solidCollision, nonsolids)
                

    def collideY(self, motion): # Get the collisions along the Y axis, return a tuple with the solid collision and a list of nonsolid collisions
        solidCollision = (None, motion)
        nonsolids = []

        for collider in Colliders:
            if (not collider == self) and self.overlap(
                (self.Width * 0.5) + self.X,
                (self.Width * -0.5) + self.X,
                (collider.Width * 0.5) + collider.X,
                (collider.Width * -0.5) + collider.X
                ):
                if collider.Solid:
                    if motion > 0.0:
                        moveover = ((collider.Height * -0.5) + collider.Y) - ((self.Height * 0.5) + self.Y)
                        if solidCollision[1] > moveover and moveover > 0 - self.Height:
                            solidCollision = (collider, moveover)
                    else:
                        moveover = ((collider.Height * 0.5) + collider.Y) - ((self.Height * -0.5) + self.Y)
                        if solidCollision[1] < moveover and moveover < self.Height:
                            solidCollision = (collider, moveover)
                else:
                    nonsolids.append(collider)
        
        for nonsolid in nonsolids:
            moveover = solidCollision[1]
            if not((moveover > 0.0 and self.overlap(
                (self.Height * 0.5) + self.Y + moveover,
                (self.Height * -0.5) + self.Y,
                (nonsolid.Height * 0.5) + nonsolid.Y,
                (nonsolid.Height * -0.5) + nonsolid.Y
            )) or (moveover <= 0 and self.overlap(
                (self.Height * 0.5) + self.Y,
                (self.Height * -0.5) + self.Y + moveover,
                (nonsolid.Height * 0.5) + nonsolid.Y,
                (nonsolid.Height * -0.5) + nonsolid.Y
            ))):
                nonsolids.remove(nonsolid)
        return (solidCollision, nonsolids)
    
    def oncollision(self, collider): # Override with events that should happen after colliding with the hitbox
        pass
    
    def move(self, x, y, tagAlong): # Collide along both axes, drag tagAlong objects with, and return collisions on each axis
        bonk = [False, False]
        ymovement = self.collideY(y)
        if ymovement[0][0] != None:
            ymovement[0][0].oncollision(self)
            bonk[1] = True
        self.Y += ymovement[0][1]
        for node in tagAlong:
            node.Y += ymovement[0][1]
        for collider in ymovement[1]:
            collider.oncollision(self)
        
        xmovement = self.collideX(x)
        if xmovement[0][0] != None:
            xmovement[0][0].oncollision(self)
            bonk[0] = True
        self.X += xmovement[0][1]
        for node in tagAlong:
            node.X += xmovement[0][1]
        for collider in xmovement[1]:
            if not(collider in ymovement[1]):
                collider.oncollision(self)
        
        return bonk

class TileBox(SquareCollider): # Tile base class
    def __init__(self, x, y):
        self.Width = 32
        self.Height = 32
        self.X = x
        self.Y = y
        self.Solid = True
        Colliders.append(self)

class WinBox(SquareCollider): # Victory tile that ends the game
    def __init__(self, x, y):
        self.Width = 32
        self.Height = 32
        self.X = x
        self.Y = y
        self.Solid = True
        Colliders.append(self)
        self.Sprite = WinSprite(x, y)
    
    def oncollision(self, collider): # End the game after colliding with the player
        global Win
        if collider == Player:
            Win = True

class SpikeBox(TileBox): # Spike tile hitbox
    def oncollision(self, collider): # Restart the level after colliding with the player
        if collider == Player:
            LoadLevel(True)

class GroundTile:
    def __init__(self, x, y):
        self.Hitbox = TileBox(x, y)
        self.Sprite = GrassSprite(x, y)

class PlayerClass(SquareCollider):
    def __init__(self):
        self.Width = 32
        self.Height = 32
        self.X = 0.0
        self.Y = 0.0
        self.Solid = True
        Colliders.append(self)
        self.Sprite = PlayerSprite(0.0, 0.0)
        self.velocityX = 0.0
        self.velocityY = 0.0
        self.jumpTime = 0.0

    def update(self): # Strafe and jump on player inputs, collide with walls, and fall
        self.velocityX = 0.0
        if Input["Left"]: self.velocityX -= 400
        if Input["Right"]: self.velocityX += 400
        if Input["Jump"] and self.jumpTime > 0.0:
            self.jumpTime -= 1 * delta
        else:
            self.velocityY -= 4000.0 * delta
            self.jumpTime = 0.0

        bonk = self.move(self.velocityX * delta, self.velocityY * delta, [self.Sprite])
        
        if bonk[0]:
            self.velocityX = 0.0

        if bonk[1]:
            if self.velocityY <= 0 and Input["Jump"]:
                self.jumpTime = 0.2
                self.velocityY = 500.0
            else:
                self.velocityY = 0.0
                self.jumpTime = 0.0
        
        self.Sprite.X = self.X
        self.Sprite.Y = self.Y
    
    def oncollision(self, collider): # Restart the level after touching an enemy
        if isinstance(collider, Enemy):
            LoadLevel(True)

class Enemy(SquareCollider): # Enemy class
    def __init__(self, x, y):
        self.Width = 32
        self.Height = 32
        self.X = x
        self.Y = y
        self.velocityX = 0.0
        self.velocityY = 0.0
        self.Solid = True
        Colliders.append(self)
        self.Sprite = EnemySprite(0.0, 0.0)
    
    def update(self): # Move toward the player, collide with walls, and fall
        self.velocityX = 0.0
        self.velocityY -= 4000.0 * delta
        if Player.X < self.X: self.velocityX -= 200
        if Player.X > self.X: self.velocityX += 200

        bonk = self.move(self.velocityX * delta, self.velocityY * delta, [self.Sprite])

        if bonk[0]:
            self.velocityX = 0.0

        if bonk[1]:
            self.velocityY = 0.0
        
        self.Sprite.X = self.X
        self.Sprite.Y = self.Y

    def oncollision(self, collider): # Restart the level on touching the player
        if collider == Player:
            LoadLevel(True)


class Spike(TileBox): # Class for spike tiles
    def __init__(self, x, y):
        self.Hitbox = SpikeBox(x, y)
        self.Sprite = SpikeSprite(x, y)

Player = PlayerClass()

Mapdata = [ # The level data
    "  p         ",
    "fffff   ffffff",
    "fffff   ffffff",
    "        f                      s",
    "        fe                 s   ff",
    "        fffffffff          ff",
    "        fffffffff   sss    se",
    "        fffffffffsssfffff  fssssssssssffs  se      sse     s  s  s",
    "        fffffffffffffffff  ffffffffffffff  fffffffffffffffff  s  s",
    "                                                              fwwf "
    ]

def LoadLevel(Death): # Load the level from map data, shake the screen if the player dies

    global Screenshake

    if Death:
        Screenshake = 0.1

    LevelObjects.clear()
    SpriteQueue.clear()
    Colliders.clear()
    Player.__init__()

    Yidx = 0

    for row in Mapdata:
        Xidx = 0
        for tile in row:
            match tile:
                case " ":
                    pass
                case "p":
                    Player.X = Xidx * 32
                    Player.Y = Yidx * 32
                case "f":
                    LevelObjects.append(GroundTile(Xidx * 32, Yidx * 32))
                case "s":
                    LevelObjects.append(Spike(Xidx * 32, Yidx * 32))
                case "e":
                    LevelObjects.append(Enemy(Xidx * 32, Yidx * 32))
                case "w":
                    LevelObjects.append(WinBox(Xidx * 32, Yidx * 32))
            Xidx += 1
        Yidx -= 1
        

LoadLevel(False) # Start the game

while True:

    updateInput() # Refresh keyboard inputs

    Player.update() # Update the player

    # Update enemies

    for object in LevelObjects:
        if isinstance(object, Enemy):
            object.update()
    
    # Restart the level if the player falls in the void

    if Player.Y < -64 - (len(Mapdata) * 32):
        LoadLevel(True)

    # Center the camera at the player's position and shake the screen

    CameraX = Player.X
    CameraY = Player.Y

    if Screenshake > 0.0:
        CameraX += random.randint(-5, 5)
        CameraY += random.randint(-5, 5)
        Screenshake -= 1 * delta
    else:
        Screenshake = 0.0

    # Display sprites

    carl.clear()
    carl.screen.tracer(0,0)
    background = []
    for Sprite in SpriteQueue:
        if Sprite.Visible:
            if Sprite.Background:
                Sprite.draw()
            else:
                background.append(Sprite)
    for Sprite in background:
        Sprite.draw()
    carl.screen.update()

    # Print the frames per second average for every frame in the last second

    deltalogs.append(delta)
    deltalogsum += delta
    while deltalogsum > 1.0:
        deltalogsum -= deltalogs[0]
        deltalogs.pop(0)
    
    deltamean = 0.0
    for item in deltalogs:
        deltamean += item
    if len(deltalogs) != 0.0 and deltamean != 0.0:
        deltamean = deltamean/len(deltalogs)
    
    if deltamean != 0.0:
        pass
        print("FPS: " + str(round(1.0/deltamean)))

    # Get the delta time from the last frame

    delta = time.monotonic() - oldtime
    oldtime = time.monotonic()

    # When you beat the game, stop everything and show a message on the screen

    if Win:
        carl.goto(0, 40)
        carl.color("black")
        carl.write("You win", False, "center", ("Arial", 32, "bold"))
        print("Game finished, close window to restart")
        while True:
            carl.screen.tracer(0,0)
            carl.screen.update()
