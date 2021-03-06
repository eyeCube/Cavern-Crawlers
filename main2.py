'''
    More Heat Than Light
    Jacob Wharton, Taylor Lundy, and John Beckman
'''


import pygame
import copy
import math
#import time
#import random
#import sys
#import os

    # CONST ######
MAXFPS = 60
WEAP_PISTOL=0
WEAP_UZI=1
WEAP_SHOTGUN=2
WEAP_CLUB=3

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
pygame.display.set_caption('More Heat Than Light')










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
        #"entities" : [],   # may be unnecessary...
        "dead" : [],    # entities to delete
        
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
##        if lis.count(item) > 0:   # should never remove non-existant item
        lis.remove(item)

    def __getitem__(self,index):
        return self.lists[index]

    def __delattr__(self, name):
        pass

    def removeDeadThings(self):
    '''
        call to delete all entities in "dead" list
    '''
    deadStuff=[]
    for ent in self['dead']:
        deadStuff.append(ent)
    for ent in deadStuff:
        if isinstance(ent, Player):
            gameOver()
        else:
            self.remove(ent, 'dead')
        ent.cleanup(self)

        
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
    code in the __init__ and cleanup functions, respectively:
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

    def cleanup(self):
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
                
            if self.keys[pygame.K_LEFT] == 1:
                self.k_left = True
            if self.keys[pygame.K_RIGHT] == 1:
                self.k_right = True
            if self.keys[pygame.K_UP] == 1:
                self.k_up = True
            if self.keys[pygame.K_DOWN] == 1:
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
        if len(args) == 0: # UNTESTED CODE !!!!
            self.coord = [0,0]
        else:
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

    def setPolar(self, theta, radius):  # UNTESTED CODE !!!!
        self[0] =  math.cos(theta) * radius
        self[1] = -math.sin(theta) * radius

    def tuple(self):
        return ( self.x, self.y )

    def list(self):
        return list( self.tuple() )

    @property 
    def radians(self):  # UNTESTED CODE !!!!
        return math.atan2(self[1], self[0]) + math.pi

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

    def cleanup(self):
        data.remove(self, 'shape')

    def addVtx(self, *args):     # Add Vertex(es)
        for a in args:
            self.vtx.append(list(a))


class Shadowcaster:

    def __init__(self):
        pass

    
class BoxCollider:
    
    def __init__(self, owner=None, width=0, height=0):
        data.add(self, 'collision')

        self.owner = owner
        self.follow(owner)
        self.set_bbox(width, height, 0, 0)
        self.solid = False

    def cleanup(self):
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
        # TODO: call follow function from within step event of objects with an instance of BoxCollider(?)
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
        if self.owner==None:
            return
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
##        data.add(self, 'step')
        
        super(Mobile, self).__init__()
        self.bbox = None # Bounding Box (Collider)
        self.x = 0
        self.y = 0
        self.speed = Vector([0,0])
        
    def cleanup(self):
        pass
##        data.remove(self, 'step')
            
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
        


'''class PlayerData: # "savedata": Save and Load Player / Quest Data

    def __init__(self):
    # When adding a new variable, add it to loadPC() too
            ## Player Vars
        self.x              = 150
        self.y              = 250
        self.accel          = 1
        self.maxSpd         = 8
        self.friction       = .5
        self.depth          = -10
        self.dash_speed     = 10
        self.sprite         = Sprite(self, SPR_pc)
        self.sprite.setDimensions(0,0,32,32)

    def loadPC(self, pc):
        pc.x             = self.x
        pc.y             = self.y
        pc.accel         = self.accel
        pc.maxSpd        = self.maxSpd
        pc.friction      = self.friction
        pc.sprite        = self.sprite
        pc.sprite.owner  = pc
        pc.depth         = self.depth
        pc.dash_speed    = self.dash_speed

    ##
save = PlayerData()
    ##
'''

class Player(Entity, Mobile):
    STATE_STANDING=0
    STATE_WALKING=1
    STATE_DASHING=2
    
    def __init__(self):
        data.add(self, 'step')
        data.add(self, 'draw')
##        data.add(self, "entities")
        
        super(Player, self).__init__()
        self.state = Player.STATE_STANDING
            # Load PC Variables
        self.x              = 150
        self.y              = 250
        self.accel          = 1
        self.maxSpd         = 8
        self.friction       = .5
        self.sprite         = Sprite(self, SPR_pc)
        self.depth          = -10
        self.dash_speed     = 10
        self.dash_time      = 5
        self.dash_cooldownMax = 15
        self.dash_cooldown  = 0
        self.dashing        = 0
        self.dash_iframes   = 4
        self.iframes        = 0
        self.bbox = BoxCollider( self, self.sprite.width,
                                       self.sprite.height )
        
    def cleanup(self):
        data.remove(self, 'step')
        data.remove(self, 'draw')
##        data.remove(self, 'entities')

    def input(self):
        # get a vector based on the move key inputs from the player
        mov = Vector( -game.k_left + game.k_right,
                      -game.k_up   + game.k_down   )
        # acceleration
        if mov.mag > 0:
            mov.set(self.accel)
            self.speed += mov
        # dashing
        if (game.k_space==True and self.dash_cooldown < 0):
            self.dash(mov)

    def ev_step(self):
        if game.paused == False:
            self.upkeep()
            self.input()
                # Max Speed
            if self.state != Player.STATE_DASHING:
                self.speed.set(
                    min(self.speed.mag, self.maxSpd) )
                # Friction
            if self.state != Player.STATE_DASHING:
                self.speed.set(
                    max(0, self.speed.mag - self.friction) )
                # Animation
            if self.state != Player.STATE_DASHING:
                if self.speed.mag >= 0.25:
                    self.state = Player.STATE_WALKING
                else:
                    self.state = Player.STATE_STANDING      
            
            super(Player, self).ev_step()
            

    def ev_draw(self):
        self.sprite.draw()

    def upkeep(self):
        self.dash_cooldown  -= 1
        self.dashing        -= 1
        self.iframes        -= 1
        if (self.state==Player.STATE_DASHING and self.dashing < 0):
            self.reset_state()
        if self.iframes < 0:
            self.invincible = False

    def resetState(self):
        self.state = Player.STATE_STANDING
        # reset sprite?
        
    def dash(self, mov):
        #self.sprite = SPR_PLAYER_DASHING
        self.invincible = True
        self.iframes = max(self.dash_iframes, self.iframes)
        self.state = Player.STATE_DASHING
        self.speed = mov * self.dash_speed
        self.dash_cooldown = self.dash_cooldownMax
        self.dashing = self.dash_time


class Enemy(Entity, Mobile):

    def __init__(self):
        self.sprite = Sprite(SPR_pc)





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


##def create_player(): # not needed anymore
##    pc = Player(data)
##    return pc



################################################################

                            # COMBAT #

################################################################

'''
    changes to existing codebase:
        - created MAXFPS const = 60, use it in main function
            - created weapon ID constants
        - added "dead" key to Observer class lists dict
        - added removeDeadThings func to Observer class
        - changed __del__ functions for all classes to the name "cleanup"
            * using __del__ was a mistake and would produce a bug.
        - updated Vector2 class
        - changed Mobile class:
            * no parent classes should add themselves to data
        **COMMENTED OUT** - added "entities" key to Observer class lists dict
        **COMMENTED OUT** - Player object adds itself to "entities" list on init, removes on del 

    TODO:
        - add IMAGE_BULLET
        - modify collision events so that:
            * each object has its own event function
            * each calls its bbox collision event in its collision event fxn
            * for bboxes, parameter other in the fxn is a bbox;
                * for entities, it is another entity.
                * for entities, can check type of other etc.
                    * for Bullet, in collision event:
##                        if isinstance(other,Entity):
##                            hurt(other, damage)
        
    
'''


class Bullet(Entity, Mobile):
    def __init__(self, data, x, y, _v, _dmg, _dType, _rng, _t, _bboxSize):
        data.add(self, "step")
        data.add(self, "draw")
        data.add(self, "entities")
        
        super(Bullet, self).__init__()
        self.x=x
        self.y=y
        self.velocity=_v
        self.damage=_dmg
        self.damageType=_dType
        self.maxRange=_rng
        self.maxTime=_t
        self.time=0
        self.startX=x
        self.startY=y
        self.sprite = Sprite(self, IMAGE_BULLET)
        self.bbox = BoxCollider(self, _bboxSize, _bboxSize)
        
    def cleanup(self, data):
        data.remove(self, 'step')
        data.remove(self, 'draw')
        data.remove(self, 'entities')
        
    def ev_step(self):
        super(Bullet,self).ev_step()
        #if game.paused==False:
        self.time = self.time + 1
        if (
            self.time > self.maxTime
            or distance(self.x,self.y,self.startX,self.startY)
            ):
            kill(self)
            return

    def ev_draw(self):
        self.sprite.draw()

    def ev_collision(self, other):
        pass


# class for things that can shoot guns, swing bats, etc.
class Fighter:
    GUN=0
    MELEE=1
    STATE_NORMAL = 0
    STATE_RELOADING = 1
    STATE_SWINGING = 2      # swinging melee weapon
##    STATE_SWAPPING = 3      # swapping weapons
##    STATE_FIRING = 10
    
    def __init__(self, weap, wType):
        super(Shooter, self).__init__()
        
        print(self, "Inherited from Fighter")
        
        self.weap=weap      # equipped weapon
        self.weapType = wType
        self._autoReload = 0
        self._reloading = 0
        self._state = Fighter.STATE_NORMAL

    def cleanup(self):
        pass

    def ev_step(self):
        print(self, "called Shooter ev_step function")
        
        # reloading
        self._autoReload -= 1
        self._reloading -= 1
        if self._autoReload == 0:
            self.reload()
        if self._reloading == 0:
            self._reload()

    def fire(self, tvector):
        '''
            (attempt to) fire the gun with the trajectory Vector tvector
                initiate reloading sequence if out of ammo
        '''
        if self._state == Fighter.STATE_NORMAL:
            if self.weap.ammo > 0:
                self.weap.pressTrigger(tvector)
            else:
                self._click_reload()
        else:
            if self._state == Fighter.STATE_RELOADING:
                self._click()
    
    def reload(self):
        '''
            begin reloading sequence
        '''
        # animation
        # TODO: animations
        # timer
        self._reloading = self.weap.reloadTime
        # change state to reloading
        self._state = Fighter.STATE_RELOADING
       
    def _click(self): # try to fire with empty mag, just play a sound
        pass
    
    def _click_reload(self): # try to fire with empty mag, auto-reload
##        sounds.play(SND_GUN_CLICK)    # TODO: sounds. Could be imported in a file called sounds.py which contains functions for playing sounds etc.
        self._autoReload = 15   # wait a few frames to auto-reload
    
    def _reload(self):  # call gun's reload func to refill ammo
        self.weap.reload()
    
    def _interruptReload(self): # call to stop the reloading sequence
        self._reloading = 0
        self._autoReload = 0
        # cancel animation
        self._state = Fighter.STATE_NORMAL


def create_pistol(x, y):
    weap = Weap_Pickup(WEAP_PISTOL, x, y)
    return weap
def create_uzi(x, y):
    weap = Weap_Pickup(WEAP_UZI, x, y)
    return weap
def create_shotgun(x, y):
    weap = Weap_Pickup(WEAP_SHOTGUN, x, y)
    return weap
def create_club(x, y):
    weap = Weap_Pickup(WEAP_CLUB, x, y)
    return weap

def equip_weapon(ent, weap):
    ent.

class Weap_Pickup:
    def __init__(self, ID, x, y):
        data.add(self, "draw")
        
        self.ID=ID
        self.x=x
        self.y=y
        self.bbox = BoxCollider(16,16)
        
    def ev_draw(self):
        pass


class Gun:
    MODE_SEMI=0
    MODE_AUTO=1
    MODE_BURST=2
    AMMO_9MM=0
    AMMO_SHELLS=1
    AMMO_50CAL=2
    
    def __init__(self,
                 name, dSprite, bSprite, aType,
                 dmgm, dmg, dType, acc, rof, magSize, rTime,
                 bSpeed, bSpeedMax, bLife, bLifeMax,
                 kick=0, pierces=0, burstn=3, aoe=0, shots=1, spread=0, 
                 semi=True, auto=False, burst=False, safe=False
                 ):
        # new parameters: kick, safe
        
        super(Gun, self).__init__()
        
        self.name = name
##        self.sprite = sprite            # player's sprite when pickup weapon
        self.dispSprite = dSprite       # display sprite (for menus, HUD, etc.)
        self.bulletSprite = bSprite     # sprite of the bullet it fires
        self.ammoType = aType           # what kind of ammunition it uses
        self.damageMelee = dmgm         # health damage dealt with melee
        self.damage = dmg               # health damage dealt with bullet
        self.damageType = dType         # Damage type constant
        self.accuracy = acc             # Tendency to aim off the cursor
        self.areaOfEffect = aoe         # pixel radius
        self.rateOfFire = rof           # shots per second
        self.shotsFired = shots         # quantity of missiles fired per shot
        self.shotSpread = spread        # shot spread amount for multishots
        self.magSize = magSize          # ammo capacity
        self.reloadTime = rTime         # game ticks elapsed when reloading
        self.bulletSpeed = bSpeed       # minimum speed the bullet moves
        self.bulletSpeedMax = bSpeedMax # maximum "
        self.bulletLife = bLife         # game ticks elapsed before autodeath
        self.bulletLifeMax = bLifeMax   # maximum "
        self.kick = kick                # kickback amount
        self.pierces = pierces          # how many foes it can pierce
        self.burstQuantity = burstn     # how many shots fired in burstfire
        self.mode_semi=semi             # can it fire semiauto?
        self.mode_auto=auto             # " automatic?
        self.mode_burst=burst           # " burst fire?
        self.has_safety = safe          # does it have a wimpy safety mode?
        
        self.mode = Gun.MODE_SEMI       # current fire mode setting
        self.safety=False               # safety mode on?
        self.ammo=0                     # number of shots currently chambered
        self.can_fire=True
        
    def safety_toggle(self):    self.safety = not self.safety
    def mode_set_semi(self):    self.mode = Gun.MODE_SEMI
    def mode_set_auto(self):    self.mode = Gun.MODE_AUTO
    def mode_set_burst(self):   self.mode = Gun.MODE_BURST
    
    def reload(self):
        # TODO: implement limited ammo restraints
        self.ammo = self.magSize
    
    def pressTrigger(self, tvector):    # fire, aimed with trajectory tvector
        if self.wait > 0: return
        if self.safety: return
        if self.mode == Gun.MODE_SEMI:
            self._fireSemi(tvector)
        elif self.mode == Gun.MODE_BURST:
            self._fireBurst(tvector)
        elif self.mode == Gun.MODE_AUTO:
            self._fireAuto(tvector)
    
    def releaseTrigger(self):
        # release the "fire" button to allow another semi-auto shot
        self.can_fire = True
        
    def _calcShotDelay(self):
        ''' Calculate & return the number of steps before you can fire again.
            Delay time is based on framerate and rate of fire. '''
        return (MAXFPS / self.rateOfFire)
    
    def _fireSemi(self, tvector):   # semi-auto fire
        #   Note: can_fire must be reset before you can fire again
        #   ( you have to release the trigger before you can pull it again )
        self.wait = self._calcShotDelay()
        self.can_fire = False
        self._fire(tvector)
    
    def _fireAuto(self, tvector):   # full auto fire
        self.wait = self._calcShotDelay()
        self._fire(tvector)
    
    def _fireBurst(self, tvector):  # burst fire
        pass
    
    def _fire(self, tvector):       # release a shot
        life = self.bulletLife + int(
            random.random(self.bulletLifeMax - self.bulletLife)
            )
        newVector = vector
        newVector.setPolar(vector.radians, self.bulletSpeed + int(
            random.random(self.bulletSpeedMax - self.bulletSpeed)
            ))
        for ii in range(self.shotsFired):
            tempVector = Vector2()
            tempVector += newVector
            tempVector.setPolar(vector.radians, self.bulletSpeed + int(
                random.random(self.bulletSpeedMax - self.bulletSpeed)
                ))
            bullet = Bullet(
                newVector,
                self.bulletSprite,
                self.damage, self.damageType, life,
                self.areaOfEffect, self.pierces
                )
            
    

def distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def gameOver():
    #TODO: show "YOU DIED" sequence or some shit
    game.end()

def hurt(ent, damage):
    if ent.isDead: return
    ent.hp -= damage
    if ent.hp <= 0:
        kill(ent)

def kill(ent):
    data.add(ent, "dead") 
    ent.isDead = True


    








################################################################

                            # MAIN #

################################################################
        

def main(*args):
    
        # INIT GAME ##
    gameRunning = True
    window.init_display(700,700)
    
        ## Init Objects
    pc = Player(data)

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
        game.clock.tick(MAXFPS)

        game.get_input()
        game.get_events()
        game.perform_events()




                    # PROGRAM #

        

main()
game.end()


################################################################



