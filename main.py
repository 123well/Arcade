from PIL import Image
import arcade
import io

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
    corner = Image.open('biom1wall2.png').resize((15, 15), 0)
    wall = Image.open('biom1wall1.png').resize((15, 15), 0)
    empty111 = Image.open('biom1wall0.png').resize((15, 15), 0)
    exits = dictionary['exits']

    result = Image.new('RGBA', (size_x * 15, size_y * 15), (0, 0, 0, 0))

    for tile_row in range(size_y):
        for tile_col in range(size_x):

            if (tile_row == 0 and tile_col == 0) or (tile_row == size_y - 5 and tile_col == 0 and 3 in exits):
                current_tile = corner.rotate(90)

            elif (tile_row == 0 and tile_col == size_x - 1) or (tile_row == size_y - 5 and tile_col == size_x - 1 and 4 in exits):
                current_tile = corner

            elif (tile_row == size_y - 1 and tile_col == 0) or (tile_row == 4 and tile_col == 0 and 2 in exits):
                current_tile = corner.rotate(180)

            elif (tile_row == size_y - 1 and tile_col == size_x - 1) or (tile_row == 4 and tile_col == size_x - 1 and 1 in exits):
                current_tile = corner.rotate(270)

            elif tile_row == 0:
                if 3 in exits and tile_row in [size_y - 2, size_y - 3, size_y - 4]:
                    continue
                current_tile = wall
            elif tile_row == size_y - 1:
                current_tile = wall.rotate(180)
            elif tile_col == 0:
                if 2 in exits and tile_row in [1, 2, 3]:
                    continue
                elif 3 in exits and tile_row in [size_y - 2, size_y - 3, size_y - 4]:
                    continue
                current_tile = wall.rotate(90)
            elif tile_col == size_x - 1:
                if 1 in exits and tile_row in [1, 2, 3]:
                    continue
                elif 4 in exits and tile_row in [size_y - 2, size_y - 3, size_y - 4]:
                    continue
                current_tile = wall.rotate(270)

            else:
                continue

            x_c = tile_col * 15
            y_c = tile_row * 15

            result.paste(current_tile, (x_c, y_c), current_tile)
    return result


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(16 * 75, 9 * 75, "fimoz game")

        room_img = make_room_walls(dictionary['shape'][0] // 5, dictionary['shape'][1] // 5)

        img_bytes = io.BytesIO()
        room_img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        texture = arcade.load_texture(img_bytes)

        self.room_sprite = arcade.Sprite()
        self.room_sprite.texture = texture
        self.room_sprite.center_x = self.width // 2
        self.room_sprite.center_y = self.height // 2

        self.room_sprite_list = arcade.SpriteList()
        self.room_sprite_list.append(self.room_sprite)

    def on_draw(self):
        self.clear()
        self.room_sprite_list.draw()


if __name__ == "__main__":
    game = MyGame()
    arcade.run()