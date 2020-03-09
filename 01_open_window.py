"""
Platformer Game
"""
import arcade
import random
import math

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Space Man"


# constants for item scaling within the game
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# movement speed of the player, in pexels per frame
PLAYER_MOVEMENT_SPEED = 5
PLAYER_TURN_SPEED = 2


class MyGame(arcade.Window):
    """
    Main application class.
    """ 

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # lists to keep track of the sprites. each sprite should go into a list
        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        # separate var that holds the player sprite
        self.player_sprite = None

        # physics engine
        self.physics_engine = None

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # instantiate the lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        
        # set up the player, placing it at specific coords
        image_source = "images/SpaceShipSprites/spaceshooter/PNG/playerShip1_blue.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 120
        self.player_sprite.angle = 0
        self.player_list.append(self.player_sprite)

        # create random meteors
        meteor_source = "images/SpaceShipSprites/spaceshooter/PNG/Meteors/meteorBrown_med1.png"
        for x in range(1, 3, 1):
            meteor = arcade.Sprite(meteor_source, TILE_SCALING)
            meteor.position = [x*100, x*20]
            self.wall_list.append(meteor)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)



    def on_draw(self):
        """ Render the screen. """

        # clear screen to background color
        arcade.start_render()
        # Code to draw the screen goes here

        # draw the sprites
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        '''called whenever a key is pressed'''

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.down or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.left or key == arcade.key.A:
            self.player_sprite.turn_left(PLAYER_TURN_SPEED)
        elif key == arcade.key.right or key == arcade.key.D:
            self.player_sprite.turn_right(PLAYER_TURN_SPEED)

    def on_key_release(self, key, modifiers):
        ''' called when key is released'''
    
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.down or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.left or key == arcade.key.A:
            self.player_sprite.change_angle = 0
        elif key == arcade.key.right or key == arcade.key.D:
            self.player_sprite.change_angle = 0

    def on_update(self, delta_time):
        ''' movement and game logic '''
        # move the player with the physics engine
        self.physics_engine.update()


        


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
