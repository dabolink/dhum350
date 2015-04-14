import pygame
GRAVITY = 1
GRAVITY_MAX = 5
JUMP = -15
LEFT = -4
RIGHT = 4
MAX = 10

class GameApp():
    def __init__(self, level=1, deaths=0):
        self.doors = []
        self.lavas = []
        self.level = level
        self.allChars = []
        self.floors = []
        self.walls = []
        self.deaths = deaths
        maxx = 0
        maxy = 0
        try:
            with open("Levels/level"+str(self.level)+".txt","r") as floorPlan:
                y = 0
                for string in floorPlan:
                    x = 0
                    for c in string:
                        if not c == "\n":
                            if c == "L":
                                Lava(x, y, "Jim", self)
                            if c == "W":
                                Wall(x, y, self)
                            if c == "F":
                                Floor(x, y, self)
                            if c == "D":
                                Door(x, y, self)
                            if c == "J":
                                Character("Jim", x, y, self)
                            if c == "N":
                                Character("John",x, y, self)
                            x += 16
                            if x > maxx:
                                maxx = x
                    y += 16
                    if y > maxy:
                        maxy = y
        except IOError:
            return

        self.width = maxx
        self.height = maxy
        size = self.width, self.height
        self.screen = pygame.display.set_mode(size)
        print self.width
        print self.height
        # for i in range(0, WIDTH, 16):
        #     Floor("", i, HEIGHT-10, self)
        # for i in range(0, HEIGHT, 16):
        #     Wall("", 0, i, self)
        #     Wall("", WIDTH-10, i, self)
        self.curCharacter = self.allChars.pop()
        self.play_field = PlayingField(15, 15, self.width, self.height)

    def nextChar(self):
        self.allChars.append(self.curCharacter)
        self.curCharacter = self.allChars.pop(0)

    def reset(self, level):
        death = pygame.mixer.Sound("sound/death.wav")
        pygame.mixer.Sound.play(death)
        self.__init__(level, self.deaths+1)


class PlayingField(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(left, top, width, height)


class Character(pygame.sprite.Sprite):
    def __init__(self, char_img, x_offset, y_offset, t_game):
        t_game.allChars.append(self)
        pygame.sprite.Sprite.__init__(self)
        self.type = char_img
        self.jumping = False
        self.image = pygame.image.load("img/" + char_img + ".png")
        self.rect = self.image.get_rect().move(x_offset, y_offset)
        print self.rect
        self.x = x_offset
        self.y = y_offset
        self.velocity = [0, GRAVITY]

    def move_left(self, t_game):
        if self.velocity[0] <= -MAX:
            self.velocity[0] = -MAX
        if self.check_for_collision(t_game.walls):
            self.velocity[0] = 0
        else:
            self.velocity[0] += LEFT

    def move_right(self, t_game):
        if self.velocity[0] >= MAX:
            self.velocity[0] = MAX
        if self.check_for_collision(t_game.walls):
            self.velocity[0] = 0
        else:
            self.velocity[0] += RIGHT
    def jump(self, t_game):
        self.jumping = True

    def move(self, t_game):
        lava = self.check_for_collision(t_game.lavas)
        if lava:
            if not lava.enemy == self.type:
                t_game.reset(t_game.level)
        self.gravity(t_game)
        self.rect = self.rect.move(self.velocity[0], 0)
        wall = self.check_for_collision(t_game.walls)
        if wall:
            if self.velocity[0] > 0:
                self.rect.right = wall.rect.left
            elif self.velocity[0] < 0:
                self.rect.left = wall.rect.right
            self.velocity[0] = 0
        if not self == t_game.curCharacter:
            if self.check_for_single_object_collision(t_game.curCharacter):
                self.velocity[0] = 0
        if self == t_game.curCharacter:
            other_char = self.check_for_collision(t_game.allChars)
            if other_char:
                if self.rect.bottom >= other_char.rect.bottom:
                    if self.velocity[0] > 0:
                        self.rect.right = other_char.rect.left
                        other_char.rect.left = self.rect.right
                        self.velocity[0] = 0
                        other_char.velocity[0] = 0

                    elif self.velocity[0] < 0:
                        self.rect.left = other_char.rect.right
                        other_char.rect.right = self.rect.left
                        other_char.velocity[0] = 0
                        self.velocity[0] = 0

        if self.check_for_collision(t_game.doors) and self == t_game.curCharacter:
            Win = True
            for char in t_game.allChars:
                if not char.check_for_collision(t_game.doors):
                    Win = False
            if Win:
                print "YOU WIN"
                t_game.level += 1
                t_game.reset(t_game.level)



    def gravity(self, t_game):
        self.velocity[1] += GRAVITY
        self.y += self.velocity[1]
        self.rect = self.rect.move(0, self.velocity[1])
        lava = self.check_for_collision(t_game.lavas)
        if lava:
            if not lava.enemy == self.type:
                print lava.enemy, self.type
                t_game.reset(t_game.level)
        floor = self.check_for_collision(t_game.floors)
        if floor and self.velocity[1] < 0:
            self.velocity[1] = 0
            self.rect.top = floor.rect.bottom
        elif floor and not self.jumping and self.rect.bottom >= self.rect.top:
            self.velocity[1] = 0
            self.jumping = False
            self.rect.bottom = floor.rect.top
            self.y = floor.rect.top - (self.rect.bottom - self.rect.top)

        elif floor and self.jumping:
            other_char = self.check_for_collision(t_game.allChars)
            if other_char:
                self.velocity[1] = 0
                other_char.velocity[1] = 0
            else:
                self.velocity[1] = JUMP
                jump = pygame.mixer.Sound("sound/jump.wav")
                jump.set_volume(0.1)
                print jump.get_volume()
                pygame.mixer.Sound.play(jump)
                self.jumping = False

        elif not floor and self.jumping:
            other_char = self.check_for_collision(t_game.allChars)
            if other_char and self == t_game.curCharacter:
                self.velocity[1] = JUMP
                self.jumping = False
                jump = pygame.mixer.Sound("sound/jump.wav")
                jump.set_volume(0.1)
                print jump.get_volume()
                pygame.mixer.Sound.play(jump)
        else:
            if self.velocity[1] < GRAVITY_MAX:
                self.velocity[1] += GRAVITY
            else:
                self.velocity[1] = GRAVITY_MAX

            if self == t_game.curCharacter:
                other_char = self.check_for_collision(t_game.allChars)
                if other_char:
                        if self.rect.top < other_char.rect.top:
                            self.rect.bottom = other_char.rect.top
                        self.velocity[1] = 0
                        other_char.velocity[1] = 0

            elif not self == t_game.curCharacter:
                if self.check_for_single_object_collision(t_game.curCharacter) and not t_game.curCharacter.jumping:
                    if self.rect.top < t_game.curCharacter.rect.bottom and t_game.curCharacter.velocity[1] >= 0:
                        self.rect.bottom = t_game.curCharacter.rect.top
                    self.velocity[1] = 0
            self.jumping = False

    def check_for_collision(self, collision_group):
        for object in collision_group:
            if self.rect.colliderect(object.rect):
                return object
        return None

    def check_for_single_object_collision(self, collision_object):
        if self.rect.colliderect(collision_object.rect):
            return True
        return False


class Door(pygame.sprite.Sprite):
    def __init__(self, x_offset, y_offset, t_game):
        t_game.doors.append(self)
        self.rect = pygame.Rect(x_offset,y_offset,32, 32)
        self.image = pygame.image.load("img/door.png")

class Floor(pygame.sprite.Sprite):
    def __init__(self, x_offset, y_offset, t_game):
        t_game.floors.append(self)
        self.rect = pygame.Rect(x_offset,y_offset,16,16)
        self.image = pygame.image.load("img/Wall.png")


class Wall(pygame.sprite.Sprite):
    def __init__(self, x_offset, y_offset, t_game):
        t_game.walls.append(self)
        self.image = pygame.image.load("img/Wall.png")
        self.rect = pygame.Rect(x_offset,y_offset,16,16)

class Lava(Floor):
    def __init__(self, x_offset, y_offset, character, t_game):
        t_game.lavas.append(self)
        t_game.floors.append(self)
        self.enemy = character
        self.image = pygame.image.load("img/Lava" + character + ".png")
        self.rect = pygame.Rect(x_offset, y_offset, 16, 16)