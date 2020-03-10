'''
A space based shooter based on the 
Asteroid smasher tutorial for PyArcade 

'''



import arcade
import math
import random
import os

from typing import cast

STARTING_ENEMY_COUNT = 5
SCALE = 0.5
OFFSCREEN_SPACE = 300
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Velocity of Escape"
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE

class TurningSprite(arcade.Sprite):
    ''' 
    Sprite that sets its angle to the direction it is facing,
    used to shoot projectiles
    '''
    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))

class ShipSprite(arcade.Sprite):
    '''
    sprite that represents space ship
    
    derives from arcade.Sprite
    '''
    def __init__(self, filename, scale):
        '''
        initializer
        '''
        # call the parent Sprite constructor
        super().__init__(filename, scale)

        # info on where we are going.
        # Angle comes in automatically from the parent class
        self.thrust = 0
        self.speed = 0
        self.max_speed = 4
        # self.drag = 0.05
        self.drag = 0
        self.respawning = 0

        # mark that we are respawning
        self.respawn()

    def respawn(self):
        '''
        called when the player dies and need to make a new ship.
        "respawning" is an invulnerability timer.
        TODO: change to respawning at last visited planet
        '''
        self.respawning = 1
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.angle = 0

    def update(self):
        '''
        update position and other variables, 
        "update()" required symantics to adjust parent method
        '''


        if self.respawning:
            self.respawning += 1
            # makes player ship opaque
            self.alpha = 255


        # slows player ship forward movement after key release
        if self.speed > 0:
            self.speed -= self.drag
            if self.speed < 0:
                self.speed = 0

        # slows player ship reverse movement after key release
        if self.speed < 0:
            self.speed += self.drag
            if self.speed > 0:
                self.speed = 0


        self.speed += self.thrust
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed:
            self.speed = -self.max_speed
        
        # moves sprite in the direction of the sprite angle
        # see 'velocity and vectors'
        self.change_x += -math.sin(math.radians(self.angle)) * self.speed
        self.change_y += math.cos(math.radians(self.angle)) * self.speed

        self.center_x += self.change_x
        self.center_y += self.change_y

        #if the ship goes off screen, move it to the other side of the window
        # TODO: change so that player is always centered but off screen logic still applies to the map
        if self.right < 0:
            self.left = SCREEN_WIDTH

        if self.left > SCREEN_WIDTH:
            self.right = 0

        if self.bottom < 0:
            self.top = SCREEN_HEIGHT

        if self.top > SCREEN_HEIGHT:
            self.bottom = 0

        ''' call parent class '''
        super().update()

class AsteroidSprite(arcade.Sprite):
    ''' 
    Sprite that represents an asteroid 
    TODO: change to planet
    '''

    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.size = 0

    def update(self):
        '''
        Moves asteroids around
        TODO: convert to landing/defence
        '''
        super().update()
        if self.center_x < LEFT_LIMIT:
            self.center_x = RIGHT_LIMIT
        if self.center_x > RIGHT_LIMIT:
            self.center_x = LEFT_LIMIT
        if self.center_y > TOP_LIMIT:
            self.center_y = BOTTOM_LIMIT
        if self.center_y < BOTTOM_LIMIT:
            self.center_y = TOP_LIMIT

class BulletSprite(TurningSprite):
        '''
        class for bullets

        derives from arcade.TurningSprite 
        which is just a Sprite that aligns to its direction
        '''
        def update(self):
            super().update()
            if self.center_x < -100 or self.center_x > 1500 of \
                    self.center_y > 1100 or self.center_y < -100:
                self.remove_from_sprite_lists()
                

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.frame_count = 0

        self.game_over = False

        # sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = None
        self.lives = 3

        # sounds
        self.laser_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound1 = arcade.load_sound(":resources:sounds/explosion1.wav")
        self.hit_sound2 = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.hit_sound3 = arcade.load_sound(":resources:sounds/hit1.wav")
        self.hit_sound4 = arcade.load_sound(":resources:sounds/hit2.wav")

    def start_new_game(self):
        '''
        sets up game and initalizes the variables
        '''
        self.frame_count = 0
        self.game_over = False

        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ship_life_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = ShipSprite(":resources:images/space_shooter/playerShip1_orange.png", SCALE)
        self.all_sprites_list.append(self.player_sprite)
        self.lives = 3

        # Make asteroids
        image_list = (":resources:images/space_shooter/meteorGrey_big1.png",
                      ":resources:images/space_shooter/meteorGrey_big2.png",
                      ":resources:images/space_shooter/meteorGrey_big3.png",
                      ":resources:images/space_shooter/meteorGrey_big4.png")
        
        for i in range(STARTING_ENEMY_COUNT):
            image_no = random.randrange(4)
            enemy_sprite = AsteroidSprite(image_list[image_no], SCALE)
            enemy_sprite.guid = "Asteroid"

            # spawn asteroid
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)
            enemy_sprite.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)

            # randomizes asteroid speed
            enemy_sprite.change_x = random.random() * 2 - 1
            enemy_sprite.change_y = random.random() * 2 - 1

            # sets asteroid off in random direction
            enemy_sprite.change_angle = (random.random() - 0.5) * 2
            enemy_sprite.size = 4
            self.all_sprites_list.append(enemy_sprite)
            self.asteroid_list.append(enemy_sprite)

    def on_draw(self):
        '''
        render the screen
        '''

        # required before we start drawing
        arcade.start_render()

        # draw all the sprites
        self.all_sprites_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 70, arcade.color.WHITE, 13)

        output = f"Asteroid Count: {len(self.asteroid_list)}"
        arcade.draw_text(output, 10, 50, arcade.color.WHITE, 13)

    def on_key_press(self, symbol, modifiers):
        '''
        called on key press
        controls
        '''
        # shoot if the player presses key and not respawning
        # TODO: fire two projectiles at a time (spawn offset)
        if not self.player_sprite.respawning and symbol == arcade.key.SPACE:
            bullet_sprite = BulletSprite(":resources:images/space_shooter/laserBlue01.png", SCALE)
            bullet_sprite.guid = "Bullet"

            # sets bullet in direction player is facing (player angle)
            # sets bullet speed
            # TODO: create seperate class for different weapons with different speeds / range
            bullet_speed = 13
            bullet_sprite.change_x = \
                -math.sin(math.radians(self.player_sprite.angle)) * bullet_speed
            bullet_sprite.change_y = \
                math.cos(math.radians(self.player_sprite.angle)) * bullet_speed

            # spawns bullet at player center
            # TODO: offset projectile spawn from weapon locations on player
            bullet_sprite.center_x = self.player_sprite.center_x
            bullet_sprite.center_y = self.player_sprite.center_y
            bullet_sprite.update()

            # adds new bullet to all/list and bullet list
            self.all_sprites_list.append(bullet_sprite)
            self.bullet_list.append(bullet_sprite)

            # TODO: derive sound from new weapon class
            arcade.play_sound(self.laser_sound)

        if symbol == arcade.key.A:
            self.player_sprite.change_angle = 3
        elif symbol == arcade.key.D:
            self.player_sprite.change_angle = -3
        # TODO: Pull thrust from ship class
        elif symbol == arcade.key.W:
            self.player_sprite.thrust = 0.15
        # TODO: Pull reverse thrust from ship class
        elif symbol == arcade.key.S:
            self.player_sprite.thrust = -0.1

    def on_key_release(self, symbol, modifiers):
        '''
        called when key is released
        '''
        if symbol == arcade.key.A:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.D:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.W:
            self.player_sprite.thrust = 0
        elif symbol == arcade.key.S:
            self.player_sprite.thrust = 0

    def split_asteroid(self, asteroid: AsteroidSprite):
        '''
        Split an asteroid into chunks
        Deletion of original asteroid is handled elsewhere
        '''
        # sets spawn coords and increments score
        x = asteroid.center_x
        y = asteroid.center_y
        self.score += 1

        if asteroid.size == 4:
            # splits into range(3) (so three) smaller asteroids
            # TODO: pull pieces from class 
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_med1.png",
                              ":resources:images/space_shooter/meteorGrey_med2.png"]
                
                enemy_sprite = AsteroidSprite(image_list[image_no], SCALE * 1.5)

                # spawn coords
                enemy_sprite.center_x = x
                enemy_sprite.center_y = y

                # randomizes velocity
                enemy_sprite.change_x = random.random() * 2.5 - 1.25
                enemy_sprite.change_y = random.random() * 2.5 - 1.25

                # sets vector for new asteroids
                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 3

                # adds new asteroid "pieces" to related lists
                self.all_sprites_list.append(enemy_sprite)
                self.asteroid_list.append(enemy_sprite)
                self.hit_sound1.play()


        elif asteroid.size == 3:
            # splits into range(3) (so three) smaller asteroids
            # TODO: pull pieces from class 
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_small1.png",
                              ":resources:images/space_shooter/meteorGrey_small2.png"]
                
                enemy_sprite = AsteroidSprite(image_list[image_no], SCALE * 1.5)

                # spawn coords
                enemy_sprite.center_x = x
                enemy_sprite.center_y = y

                # randomizes velocity
                enemy_sprite.change_x = random.random() * 3 - 1.5
                enemy_sprite.change_y = random.random() * 3 - 1.5

                # sets vector for new asteroids
                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 2

                # adds new asteroid "pieces" to related lists
                self.all_sprites_list.append(enemy_sprite)
                self.asteroid_list.append(enemy_sprite)
                self.hit_sound2.play()


        elif asteroid.size == 3:
            # splits into range(3) (so three) smaller asteroids
            # TODO: pull pieces from class 
            for i in range(3):
                image_no = random.randrange(2)
                image_list = [":resources:images/space_shooter/meteorGrey_tiny1.png",
                              ":resources:images/space_shooter/meteorGrey_tiny2.png"]
                
                enemy_sprite = AsteroidSprite(image_list[image_no], SCALE * 1.5)

                # spawn coords
                enemy_sprite.center_x = x
                enemy_sprite.center_y = y

                # randomizes velocity
                enemy_sprite.change_x = random.random() * 3.5 - 1.75
                enemy_sprite.change_y = random.random() * 3.5 - 1.75

                # sets vector for new asteroids
                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 1

                # adds new asteroid "pieces" to related lists
                self.all_sprites_list.append(enemy_sprite)
                self.asteroid_list.append(enemy_sprite)
                self.hit_sound3.play()


        elif asteroid.size == 1:
            self.hit_sound4.play()

    def on_update(self, x):
        '''
        move all the things
        '''
        self.frame_count += 1

        if not self.game_over:
            # here is why the ShipSprite class needs update()
            # so that it can be called while nested within the list
            self.all_sprites_list.update()       

            # checks for collisions between bullets and asteroids
            for bullet in self.bullet_list:
                asteroids_plain = arcade.check_for_collision_with_list(bullet, self.asteroid_list)
                asteroids_spatial = arcade.check_for_collision_with_list(bullet, self.asteroid_list)
                if len(asteroids_plain) != len(asteroids_spatial):
                    print('error')

                asteroids = asteroids_spatial

                for asteroid in asteroids:
                    # creates new smaller asteroids
                    self.split_asteroid(cast(AsteroidSprite, asteroid))
                    # deletes original asteroid and bullet (collide with bullet)
                    asteroid.remove_from_sprite_lists()
                    bullet.remove_from_sprite_lists()

            if not self.player_sprite.respawning:
                # same as for bullets but with player instead
                asteroids = arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list)
                # if there is an asteroid collision then asteroids is at least 1
                if len(asteroids) > 0:
                    # number of lives check
                    if self.lives > 0:
                        self.lives -= 1
                        self.player_sprite.respawn()
                        # asteroids[0] refers to the first asteroid in case several collide at once
                        self.split_asteroid(cast(AsteroidSprite, asteroids[0]))
                        asteroids[0].remove_from_sprite_lists()
                        self.ship_life_list.pop().remove_from_sprite_lists()
                        print("Crash")
                    else:
                        self.game_over = True
                        print("Game over")






'''
Game Open
'''

def main():
    window = MyGame()
    window.start_new_game()
    arcade.run()


if __name__ == "__main__":
    main()