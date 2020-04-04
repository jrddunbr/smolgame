#!/usr/bin/python3

# Created by Jared Dunbar, April 4th, 2020
# Use this as an example for a basic game.

import pyxel, random
import os.path
from os import path

# Width and height of game, in tiles
WIDTH = 12
HEIGHT = 8

# Entities (should not) be able to walk through structures,
#   unless they have "allow" set to True
structures = []

# Entities can move all over the place and stand in the same cube, but not walk
#   into structures unless the structure has "allow" set to True
entities = []

# This is the texture map. We're cool and only register things once.
textures = {}

# This sets up all the rendering code for ya. Give it a image,
#   and it will remember the thing for you. WARNING! VERY BASIC
class Drawn():
    def __init__(self, name, texture="invalid.png"):
        # Only register if we're not in the texture map
        if (name not in textures):

            # This makes sure that your game doesn't crash if there's an invalid
            #   texture path.
            if not path.exists(texture):
                texture = "invalid.png"

            # There are 256 pixels wide so this class can store up to 16
            #   textures. Textures are always 16x16 for simplicity
            self.loc = len(textures)*16
            pyxel.image(0).load(0, self.loc, texture)
            textures[name] = self

    def draw(self, x, y):
        pyxel.blt(x * 16, y * 16, 0, 0, self.loc, 16, 16)

# This is the base class of any thing that renders to the screen and ticks.
class Entity():
    def __init__(self, name, texture="invalid.png", x=0, y=0):
        self.name = name
        self.x = x
        self.y = y
        self.allow = False
        self.texName = texture.rsplit(".",1)[0] # remove file extension
        Drawn(self.texName, texture)

    def update(self):
        pass

    def draw(self):
        textures[self.texName].draw(self.x, self.y)

# The player class extends Entity by listening for keyboard events.
class Player(Entity):
    def __init__(self, name, x=WIDTH/2, y=HEIGHT/2):
        super(Player, self).__init__(name, "player.png", x, y)
        self.cooldown = 0
        self.cooldownTime = 2

    def update(self):
        self.cooldown -= 1
        if (self.cooldown <= 0):
            if pyxel.btn(pyxel.KEY_UP):
                if canGo(self.x, self.y-1):
                    self.y -= 1
                self.cooldown = self.cooldownTime
            elif pyxel.btn(pyxel.KEY_DOWN):
                if canGo(self.x, self.y+1):
                    self.y += 1
                self.cooldown = self.cooldownTime
            elif pyxel.btn(pyxel.KEY_LEFT):
                if canGo(self.x-1,self.y):
                    self.x -= 1
                self.cooldown = self.cooldownTime
            elif pyxel.btn(pyxel.KEY_RIGHT):
                if canGo(self.x+1,self.y):
                    self.x += 1
                self.cooldown = self.cooldownTime

# This tells you if an entity is permitted to go somewhere.
def canGo(x, y):
    if (x < 0 or x >= WIDTH):
        pyxel.play(0, 0)
        return False
    if (y < 0 or y >= HEIGHT):
        pyxel.play(0, 0)
        return False

    for s in structures:
        if (s.x == x) and (s.y == y):
            if s.allow:
                return True
            pyxel.play(0, 0)
            return False
    return True

# This sets up the game
def setup():
    # Register with Pyxel
    pyxel.init(WIDTH * 16, HEIGHT * 16, caption="smolgame", scale=8, fps=20)

    # Register sounds
    pyxel.sound(0).set(
        note="c2c2", tone="s", volume="4", effect=("n" * 4 + "f"), speed=2
    )
    pyxel.sound(1).set(
        note="c3e3g3c4c4", tone="s", volume="4", effect=("n" * 4 + "f"), speed=7
    )

    # Register our player
    player = Player("player")
    entities.append(player)

    # Invalid texture test code
    #random = Entity("random", "random.png")
    #entities.append(random)

# Generate the world! You can use this to generate levels or whatever
def worldgen():
    for a in range(0, 10):
        x = random.randrange(0, WIDTH - 1)
        y = random.randrange(0, HEIGHT - 1)
        wall = Entity("wall", "wall.png", x, y)
        structures.append(wall)

# This is called by Pyxel every tick, and handles all game inputs
def update():
    # Clear the screen
    pyxel.cls(col=0)

    # Quit if Q
    if pyxel.btn(pyxel.KEY_Q):
        pyxel.quit()

    # Play a sound if Space
    if pyxel.btn(pyxel.KEY_SPACE):
        pyxel.play(0, 1)

    # Tick all entites and structures. The player movement is included randomly
    #   somewhere in this list but you can do a list comprehension to make it
    #   go first or last if you want (examples provided with no warranty)
    # for x in [x for x in entities if x is Player]
    # for x in [x for x in entities if x is not Player]
    for x in entities:
        x.update()
    for x in structures:
        x.update()

# This is called by Pyxel every time the screen needs a redraw, which can be
#   more than once per tick, but really depends on the FPS?
def draw():
    for x in entities:
        x.draw()
    for x in structures:
        x.draw()

# This is where the game setup logic is
def run():
    setup()
    worldgen()
    pyxel.run(update, draw)

# This is the entry point for our file.
run()
