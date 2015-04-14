import pygame
import GameObjects
from pygame.locals import *


def main():
    pygame.init()
    pygame.mixer.music.load("sound/Background.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    t_game = GameObjects.GameApp()
    clock = pygame.time.Clock()
    pygame.key.set_repeat(200, 50)
    tri_img = pygame.image.load("img/triangle.png")
    bg_img = pygame.image.load("img/Background.png")
    font = pygame.font.Font(None,36)
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    t_game.curCharacter.move_left(t_game)
                elif event.key == K_RIGHT:
                    t_game.curCharacter.move_right(t_game)
                if event.key == K_UP:
                    t_game.curCharacter.jump(t_game)
                if event.key == K_SPACE:
                    t_game.nextChar()
                if event.key == K_r:
                    t_game.reset(t_game.level)
            elif event.type == QUIT:
                exit()
            else:
                t_game.curCharacter.velocity[0] = 0
        for character in t_game.allChars:
            character.move(t_game)
        t_game.curCharacter.move(t_game)
        x = 0
        y = 0
        while x <= t_game.width:
            y = 0
            while y <= t_game.height:
                t_game.screen.blit(bg_img, (x, y))
                y += 32
            x += 32

        #DRAW OBSTACLES
        for wall in t_game.walls:
            t_game.screen.blit(wall.image, wall.rect)
        for floor in t_game.floors:
            t_game.screen.blit(floor.image, floor.rect)
        for door in t_game.doors:
            t_game.screen.blit(door.image, (door.rect.left, door.rect.top))
        for lava in t_game.lavas:
            t_game.screen.blit(lava.image, (lava.rect.left, lava.rect.top))
        # DRAW CURRENT CHARACTER
        for character in t_game.allChars:
            t_game.screen.blit(character.image, (character.rect.left, character.rect.top))
        t_game.screen.blit(t_game.curCharacter.image, (t_game.curCharacter.rect.left, t_game.curCharacter.rect.top))
        tri_rect = tri_img.get_rect()
        tri_left = t_game.curCharacter.rect.left #+ (tri_rect.top - tri_rect.bottom)
        tri_top = t_game.curCharacter.rect.top - (tri_rect.bottom - tri_rect.top)
        t_game.screen.blit(tri_img, (tri_left, tri_top))
        #DEATHS
        text = font.render("Deaths: " + str(t_game.deaths), 1, (0, 0, 0))
        textpos = text.get_rect()
        textpos.left += 16
        t_game.screen.blit(text, textpos)
        pygame.display.flip()
        # print t_game.curCharacter.velocity
        # print str(t_game.curCharacter.x) + " , " +  str(t_game.curCharacter.y)
        clock.tick(60)



if __name__ == "__main__":
    main()
