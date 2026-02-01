from PIL import Image
import arcade
import io

SPEED = 4
dictionary = {
    "shape": [120, 100],
    "moving": [
        [67, 30, 20],
        [52, 50, 20],
        ["<50", 70, 20]
    ],
    "walls": [[75, 70, 50, 10]],
    "loot": [[67, 5]],
    "enemies": [[12, 5]],
    "exits": [1, 2, 3, 4]
}


def create_block(x, y, output_path='block.png'):
    corner = Image.open('biom1wall2.png').resize((15, 15), 0)
    wall = Image.open('biom1wall1.png').resize((15, 15), 0)
    empty = Image.open('biom1wall0.png').resize((15, 15), 0)

    result = Image.new('RGBA', (x * 15, y * 15), (0, 0, 0, 0))

    for tile_row in range(y):
        for tile_col in range(x):

            if tile_row == 0 and tile_col == 0:
                current_tile = corner.rotate(270)

            elif tile_row == 0 and tile_col == x - 1:
                current_tile = corner.rotate(180)

            elif tile_row == y - 1 and tile_col == 0:
                current_tile = corner

            elif tile_row == y - 1 and tile_col == x - 1:
                current_tile = corner.rotate(90)

            elif tile_row == 0:
                current_tile = wall.rotate(180)
            elif tile_row == y - 1:
                current_tile = wall
            elif tile_col == 0:
                current_tile = wall.rotate(270)
            elif tile_col == x - 1:
                current_tile = wall.rotate(90)

            else:
                current_tile = empty

            x_c = tile_col * 15
            y_c = tile_row * 15

            result.paste(current_tile, (x_c, y_c), current_tile)

    result.save(output_path)
    return result


def make_room_walls(size_x, size_y):
    corner = Image.open('biom1wall2.png').resize((15 * 5, 15 * 5), 0)
    wall = Image.open('biom1wall1.png').resize((15 * 5, 15 * 5), 0)
    exits = dictionary['exits']
    tile_size = 15 * 5

    wall_images = []

    for tile_row in range(size_y):
        for tile_col in range(size_x):
            current_tile = None

            # Логика определения, есть ли здесь стена
            if (tile_row == 0 and tile_col == 0) or (tile_row == size_y - 5 and tile_col == 0 and 3 in exits):
                current_tile = corner.rotate(90)
            elif (tile_row == 0 and tile_col == size_x - 1) or (tile_row == size_y - 5 and tile_col == size_x - 1 and 4 in exits):
                current_tile = corner
            elif (tile_row == size_y - 1 and tile_col == 0) or (tile_row == 4 and tile_col == 0 and 2 in exits):
                current_tile = corner.rotate(180)
            elif (tile_row == size_y - 1 and tile_col == size_x - 1) or (tile_row == 4 and tile_col == size_x - 1 and 1 in exits):
                current_tile = corner.rotate(270)
            elif tile_row == 0:
                if not (3 in exits and tile_row in [size_y - 2, size_y - 3, size_y - 4]):
                    current_tile = wall
            elif tile_row == size_y - 1:
                current_tile = wall.rotate(180)
            elif tile_col == 0:
                if not ((2 in exits and tile_row in [1, 2, 3]) or (3 in exits and tile_row in [size_y - 2, size_y - 3, size_y - 4])):
                    current_tile = wall.rotate(90)
            elif tile_col == size_x - 1:
                if not ((1 in exits and tile_row in [1, 2, 3]) or (4 in exits and tile_row in [size_y - 2, size_y - 3, size_y - 4])):
                    current_tile = wall.rotate(270)

            if current_tile is not None:
                x = tile_col * tile_size
                y = tile_row * tile_size
                wall_images.append((current_tile, x, y))

    return wall_images


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(1200, 675, "fimoz game")
        self.camera = arcade.camera.Camera2D()
        self.setup()

    def setup(self):
        size_x = dictionary['shape'][0] // 5  # 24
        size_y = dictionary['shape'][1] // 5  # 20
        wall_data = make_room_walls(size_x, size_y)

        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        for img, x, y in wall_data:
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            texture = arcade.load_texture(img_bytes)

            wall_sprite = arcade.Sprite(texture)
            wall_sprite.center_x = x + texture.width / 2
            wall_sprite.center_y = y + texture.height / 2
            self.wall_list.append(wall_sprite)

        self.player_sprite_list = arcade.SpriteList()
        self.player = arcade.Sprite(":resources:images/enemies/slimeBlue.png", scale=2)
        self.player.center_x = size_x * 75 // 2
        self.player.center_y = 200
        self.player_sprite_list.append(self.player)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.wall_list,
            gravity_constant=0.5,
            ladders=None,
            walls=None
        )

        self.camera.viewport = (0, 0, self.width, self.height)
        self.center_camera_to_player()

    def center_camera_to_player(self):
        self.camera.position = (self.player.center_x, self.player.center_y)

    def on_draw(self):
        self.clear(arcade.color.DARK_BLUE_GRAY)
        self.wall_list.draw()
        self.player_sprite_list.draw()


    def on_update(self, delta_time: float):
        self.physics_engine.update()
        self.center_camera_to_player()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = SPEED
        elif key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.change_y = 12
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0


if __name__ == "__main__":
    game = MyGame()
    arcade.run()
