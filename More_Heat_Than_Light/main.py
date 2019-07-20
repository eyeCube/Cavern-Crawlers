
import pygame
import copy
import math
#import time
#import random
#import sys
#import os

    # CONST ######
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
    ##############

    # Load Assets #
SPR_pc = pygame.image.load('assets/player/mc.png')
SPR_enemy = pygame.image.load('assets/player/enemy.png')
SPR_enviro_car = pygame.image.load('assets/enviromentals/car.png')
SPR_weapon_pistol = pygame.image.load('assets/weapons/socom.png')
SPR_weapon_pistol_pickup = pygame.image.load('assets/weapons/socom_pickup.png')
SPR_projectile_9mm = pygame.image.load('assets/ammo/9mm.png')
SPR_projectile_50cal = pygame.image.load('assets/ammo/50cal.png')
    ###############

    # Init Pygame #
pygame.init()
pygame.display.set_caption('Game Title')










################################################################

                # Persistent Classes #

################################################################


class Observer: # "data": Global Datalists for runtime
    '''
    This object keeps track of lists of objects for reference
        by other objects.
    Each object with a step event, for example, must be placed
        on this list using the self.add() function,
        and removed when deleted using self.remove().

        Event names:
        
        ev_step             Performed every game frame
        ev_draw             Final event performed
        ev_collision        Event not performed automatically.
            Function ev_collision() must be explicitly called.
            Collisions will only be checked against other
            items in the list 'ev_collision'. All objects that
            can collide have to have an object BoxCollider
            called bbox.
    '''
    
    lists = {
        "shape" : [],
        
        "step" : [],
        "draw" : [],
        "collision" : [],
            }

    def add(self, item, index):
        lis = self[index]
        if lis.count(item) == 0:
            lis.append(item)

    def remove(self, item, index):
        lis = self[index]
        if lis.count(item) > 0:
            lis.remove(item)

    def __getitem__(self,index):
        return self.lists[index]

    def __delattr__(self, name):
        pass
        
    ##
data = Observer()
    ##


class OrangIO: # "game": I/O Input and Output
    ''' NOTES
    This object takes input from Input class and handles
    events for all objects.
    
    perform_events() function:
    Iterate through list of events and also lists of objects
    Which have custom defined events like ev_step or ev_draw.
    To add a new event to an object, add the corresponding
    Event function (def ev_step, etc.) and put the following
    code in the __init__ and __del__ functions, respectively:
        data.add('ev_step', self)
        data.remove('ev_step', self)
    Replace ev_step with the event name if other than step.
    See Observer class for event names.
    '''
    
    events = None
    paused = False
    clock = pygame.time.Clock()
    suspended = False
    suspendAt_endOfTurn = False

    def __init__(self):
        data.add(self, 'step')
        self.init_keys()

    def __del__(self):
        data.remove(self, 'step')

    def turn(self, value):
        # Handle the IO stream
    # While suspended, does not take Input or give Output.
    # Call with 'step' as argument to advance one frame then suspend IO.
        val = False
        if   value == 'off':
            val = True
        elif value == 'on':
            val = False
        elif value == 'step':
            val = False
            self.suspendAt_endOfTurn = True
        self.suspended = val
    
    def perform_events(self):
        if self.suspended == False:
            
            #####    PYGAME EVENTS    #####
            for ev in self.events:
                if ev.type == pygame.QUIT:
                    self.end()
            
            #####    CUSTOM EVENTS    #####
                
                # STEP Event #
            for obj in data["step"]:
                obj.ev_step()
                        
                # DRAW Event #
            window.clear()
            window.queues_clear()
            
            for obj in data["draw"]:
                obj.ev_draw()
                
            window.queues_sortAll()
            window.draw()
            window.update()

            print("going")
            if self.suspendAt_endOfTurn == True:
                self.suspendAt_endOfTurn = False
                self.suspended = True
                print("worked")

    def init_keys(self):
        
        self.k_space = False
        
        self.k_left = False
        self.k_right = False
        self.k_up = False
        self.k_down = False

    def get_input(self):
        if self.suspended == False:
            
            self.init_keys()
            self.keys = pygame.key.get_pressed()
            
            if self.keys[pygame.K_SPACE] == 1:
                self.k_space = True
                
            if self.keys[pygame.K_a] == 1:
                self.k_left = True
            if self.keys[pygame.K_d] == 1:
                self.k_right = True
            if self.keys[pygame.K_w] == 1:
                self.k_up = True
            if self.keys[pygame.K_s] == 1:
                self.k_down = True

    def get_events(self):
        if self.suspended == False:
            self.events = pygame.event.get()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def pause_toggle(self):
        self.paused = not(self.paused)
    
    def end(self):
        pygame.quit()
        quit()
    
    def ev_step(self):
        pass

    ##
game = OrangIO()
    ##


class Window: # "window": GUI

        # Queue of objects to be drawn to the screen
    q = {
        'sprites' : []
        }

    def __init__(self, w, h):
        self.init_display(w, h)

    def init_display(self, w, h):
        self.DISP_W = w
        self.DISP_H = h
        self.disp = pygame.display.set_mode( (self.DISP_W,self.DISP_H) )

    def sprite(self, spr, x, y, z  ):
        # transform sprite object into list of data
        self.q['sprites'].append(
            [spr, round(x), round(y), z] )

    def queues_clear(self):         #<--''' ALTERED: TEST THIS CODE !!!!'''
        self.q['sprites'] = []

    def queue_sort(self, q):        #<--''' ALTERED: TEST THIS CODE !!!!'''
        # sort by depth (4th item in 'sprite' data created by Window.sprite())
        q = sorted(
             q, key=lambda item: item[3], reverse=True)

    def queues_sortAll(self):
        self.queue_sort(self.q["sprites"])
    
    def draw(self):     # Draw Screen
            # Sprites #
        for spr in self.q['sprites']:
            if (  spr[0] != None
            and   spr[0].visible == True  ):
                self.disp.blit(spr[0].sprite,
                              (spr[1], spr[2]) )
            # Shapes #
        for obj in data['shape']:
            if (  len(obj.vtx) > 2
            and   obj.visible == True  ):
                self.draw_poly( obj)

    def draw_poly(self, poly):
        ptList = copy.deepcopy(poly.vtx)
        i = 0
        while i < len(ptList):
            ptList[i][0] += poly.x
            ptList[i][1] += poly.y
            i +=1
        pygame.draw.polygon(self.disp, poly.color, ptList)
        
    def clear(self):    # Clear Screen
        self.disp.fill(WHITE)

    def update(self):   # Refresh Screen
        pygame.display.update()
        
    ##
window = Window(256, 256)
    ##





################################################################

                        # Other Classes #

################################################################



class Vector:
    D = 2   # Number of Dimensions
    
    def __init__(self, *args):
        self.coord = flatten(args)

    def __getitem__(self,index):
        return self.coord[index]

    def __setitem__(self,index,value):
        self.coord[index] = value

    def __add__(self, val):     # Vector Addition
        ans = []
        for i in range(self.D): # val must have __getitem__
            ans.append(self[i] + val[i])
        return Vector(ans)

    def __iadd__(self, val):
        for i in range(self.D):
            self[i] += val[i]
        return self

    def __sub__(self, val):     # Vector Subtraction
        ans = []
        for i in range(self.D):
            ans.append(self[i] - val[i])
        return Vector(ans)

    def __isub__(self, val):
        for i in range(self.D):
            self[i] -= val[i]
        return self

    def __mul__(self, val):     # Scalar Multiplication
        ans = []
        for i in range(self.D):
            ans.append(self[i] * val)
        return Vector(ans)

    def __imul__(self, val):
        for i in range(self.D):
            self[i] *= val
        return self

    def __truediv__(self, val): # Scalar Division
        ans = []
        for i in range(self.D):
            ans.append(self[i] / val)
        return Vector(ans)

    def __itruediv__(self, val):
        for i in range(self.D):
            self[i] /= val
        return self
    
    def set(self, *args):       # Set Magnitude or set Coordinates
        if len(args) == 1:      # Pass in exactly one or D arguments respectively
            sz = self.mag
            if sz != 0:
                for i in range(self.D):
                    self[i] = ( self[i] / sz ) * args[0]
        else:
            i = 0
            for arg in args:
                self[i] = args[i]
                i +=1

    def setPolar(self, radius, theta):  # UNTESTED CODE !!!!
        self[0] =  math.cos(radius) * theta
        self[1] = -math.sin(radius) * theta

    def tuple(self):
        return ( self.x, self.y )

    def list(self):
        return list( self.tuple() )

    @property 
    def x(self):
        return self[0]

    @property 
    def y(self):
        return self[1]

    @property 
    def mag(self):              # Get Magnitude
        return ( self.x**2 + self.y**2 ) **0.5


class Sprite:
    
    def __init__(self, owner, spr):
        self.owner = owner
        self.sprite = spr
        self.setDimensions(0,0,0,0)
        self.visible = True

    def setDimensions(self, xOff, yOff, w, h):
        self.x_offset = xOff
        self.y_offset = yOff
        self.width = w
        self.height = h

    def draw(self, *args):
        depth = self.owner.depth
        x = self.owner.x
        y = self.owner.y
        if len(args) > 0:
            x               = args[0]
            y               = args[1]
            self.depth      = args[2]
        window.sprite( self, x, y, depth )


class Shape:
    
    def __init__(self, xs, ys, *args):
        data.add(self, 'shape')
        
        self.color = BLACK
        self.x = xs
        self.y = ys
        self.vtx = []   # List of Vertices [x,y]
        for a in args:
            self.addVtx(a)
        self.visible = True

    def __del__(self):
        data.remove(self, 'shape')

    def addVtx(self, *args):     # Add Vertex(es)
        for a in args:
            self.vtx.append(list(a))


class Shadowcaster:

    def __init__(self):
        pass

    
class BoxCollider:
    
    def __init__(self, owner, width, height):
        data.add(self, 'collision')
        
        self.owner = owner
        self.follow(owner)
        self.set_bbox(width, height, 0, 0)
        self.solid = False

    def __del__(self):
        data.remove(self, 'collision')

    def set_bbox(self, width, height, xOff, yOff):
        self.w = width
        self.h = height
        self.xOffset = xOff
        self.yOffset = yOff

    '''def overlaps(self, other): ##  Move to Owner then check a collision
        self.follow(self.owner)
        return ev_collision(self,other)'''

    def place_free(self, xto, yto):
        self.x = xto
        self.y = yto
        
        isFree = True
        for obj in data['collision']:
            if (  obj != self
            and   obj.solid == True
            and   self.ev_collision(obj) == True  ):
                isFree = False
                break
        return isFree
        
    def follow(self, obj):
        self.x = obj.x
        self.y = obj.y

    def ev_collision(self,other): # Check at Current Position.
    #   other is BoxCollider
        if  (   self.x  <= other.x  + other.w
        and     self.x   + self.w  >= other.x
        and     self.y  <= other.y  + other.h
        and     self.y   + self.h  >= other.y   ):
            return True
        else:
            return False



        



#####################################
########   GAME CLASSES     ###########
#####################################



class Mobile:

    def __init__(self):
        data.add(self, 'step')
        
        super(Mobile, self).__init__()
        self.bbox = None # Bounding Box (Collider)
        self.x = 0
        self.y = 0
        self.speed = Vector([0,0])
        
    def __del__(self):
        data.remove(self, 'step')
            
    def move(self): # Move X and Y based on speed Vector
        if self.speed.mag != 0:
            xSpd = self.speed.x
            ySpd = self.speed.y
            
            if self.bbox != None:
                if self.bbox.place_free(
                    self.x + xSpd, self.y ) == True:
                    self.x += xSpd
                if self.bbox.place_free(
                    self.x, self.y + ySpd ) == True:
                    self.y += ySpd
            else:
                self.x += xSpd
                self.y += ySpd

    def jumpTo(self, xto, yto):
        self.x = xto
        self.y = yto

    def ev_step(self):
        if game.paused == False:
            self.move()


class Entity:
    
    def __init__(self):
        super(Entity, self).__init__()
        self.x = 0
        self.y = 0
        self.hp = 0
        self.hpMax = 0
        


class Player(Entity, Mobile):
    STATE_STANDING  = 0
    STATE_WALKING   = 1
    STATE_DASHING   = 2

    
    def __init__(self):
        data.add(self, 'step')
        data.add(self, 'draw')
        
        super(Player, self).__init__()
            # Load PC Variables
        self.x             = 150
        self.y             = 250
        self.accel         = 1
        self.maxSpd        = 6
        self.friction      = .5
        self.sprite        = Sprite(self, SPR_pc)
        self.depth         = -10
        self.dash_speed    = 20
        self.dash_time     = 6
        self.dash_cooldown = 0
        self.dash_cooldown_max = 30
        self.dashing = 0
        self.invincible = False
        self.iframes = 0
        self.dash_iframes = 4
        self.sprite.setDimensions(0,0,32,32)
        
       
        self.bbox = BoxCollider( self, self.sprite.width,
                                       self.sprite.height )
        self.state = Player.STATE_STANDING

    def upkeep(self):
        self.iframes -= 1
        self.dash_cooldown -= 1
        self.dashing -= 1
        if self.dashing < 0:
            self.reset_state()
        if self.iframes < 0:
            self.invincible = False
    
    def __del__(self):
        data.remove(self, 'step')
        data.remove(self, 'draw')

    def reset_state(self):
        self.state = Player.STATE_STANDING

    def input(self):
        mov = Vector( -game.k_left + game.k_right,
                      -game.k_up   + game.k_down   )
        if mov.mag > 0:
            mov.set(self.accel)
            self.speed += mov

        if game.k_space == True and self.dash_cooldown < 0:
            self.dash(mov)

    def dash(self, mov):
        self.invincible = True
        self.iframes = max(self.dash_iframes, self.iframes)
        self.state = Player.STATE_DASHING
        self.speed =mov * self.dash_speed
        self.dash_cooldown = self.dash_cooldown_max
        self.dashing = self.dash_time

    def ev_step(self):
        if game.paused == False:
            self.upkeep()
            self.input()
                # Max Speed
            if self.state != Player.STATE_DASHING:
                self.speed.set(
                    min(self.speed.mag, self.maxSpd) )
                # Friction
            self.speed.set(
                max(0, self.speed.mag - self.friction) )

                # Dashing
            if self.state != Player.STATE_DASHING:
                if self.speed.mag >= 0.25:
                    self.state = Player.STATE_WALKING
                else:
                    self.state = Player.STATE_STANDING
            
            super(Player, self).ev_step()
            

    def ev_draw(self):
        self.sprite.draw()


class Enemy(Entity, Mobile):

    def __init__(self):
        self.sprite = Sprite(SPR_enemy)





################################################################

                        # FUNCTIONS #

################################################################



def flatten(*args):
    ans = []
    for arg in args:
        if hasattr(arg, '__iter__'):
            ans.extend(flatten(*arg))
        else:
            ans.append(arg)
    return ans



################################################################

                            # MAIN #

################################################################
        

def main(*args):
    
        # INIT GAME ##
    gameRunning = True
    window.init_display(700, 700)
    
        ## Init Objects
    pc = Player()

        ##### TESTING PURPOSES ONLY
    Shape(200, 200, [0,0],     [120,50], [40,150] ).color = RED
    Shape(10, 50, (-50,20),  (40,190), (30,250) )
    Shape(500, 300, (-50,100), (190,0), (200,100), (400,250) )
    bill = Shape( 40, 40, (0, 0), (0, 120), (120, 120), (120, 0) )
    box1 = BoxCollider(bill, 120, 120)
    box1.solid = True
    bob = Shape( 400, 40, (0, 0), (0, 120), (120, 120), (120, 0) )
    box2 = BoxCollider(bob, 120, 120)
    box2.solid = True
    Shape(40, 20)
    del bob

    u = -1
        #####

    
# MAIN GAME LOOP #
    while gameRunning:
        game.clock.tick(60)

        game.get_input()
        game.get_events()
        game.perform_events()




                    # PROGRAM #

        

main()
game.end()


################################################################



