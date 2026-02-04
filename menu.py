import arcade
import math
import json
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
TITLE = "CYBER NEXUS"
SETTINGS_FILE = "settings.json"

CYBER_GREEN = (0, 255, 128)
CYBER_BLUE = (0, 191, 255)
DARK_BG = (12, 18, 35)
ACCENT = (80, 220, 255)
TEXT_COLOR = (240, 255, 250)


class Slider:
    def __init__(self, x, y, w, h, min_v, max_v, val, color):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.min_v, self.max_v, self.val = min_v, max_v, val
        self.color, self.drag = color, False

    def draw(self):
        arcade.draw_rectangle_filled(self.x + self.w / 2, self.y, self.w, self.h, (30, 40, 70))
        fill_w = (self.val - self.min_v) / (self.max_v - self.min_v) * self.w
        arcade.draw_rectangle_filled(self.x + fill_w / 2, self.y, fill_w, self.h, self.color)
        arcade.draw_rectangle_outline(self.x + self.w / 2, self.y, self.w, self.h, (100, 150, 200), 2)
        handle_x = self.x + (self.val - self.min_v) / (self.max_v - self.min_v) * self.w
        arcade.draw_circle_filled(handle_x, self.y, self.h / 2 + 3, self.color)

    def update(self, x):
        rel = max(0.0, min(1.0, (x - self.x) / self.w))
        self.val = self.min_v + rel * (self.max_v - self.min_v)


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.load_settings()
        self.state = "main"
        self.selected = 0
        self.pulse = 0.0
        self.setup_sliders()

    def setup_sliders(self):
        cx = SCREEN_WIDTH / 2
        self.brightness_slider = Slider(cx - 180, SCREEN_HEIGHT / 2 + 40, 360, 18, 0.5, 2.0, self.brightness,
                                        CYBER_GREEN)
        self.sensitivity_slider = Slider(cx - 180, SCREEN_HEIGHT / 2 - 20, 360, 18, 0.2, 3.0, self.sensitivity,
                                         CYBER_BLUE)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE) as f:
                    s = json.load(f)
                    self.brightness = s.get("brightness", 1.0)
                    self.sensitivity = s.get("sensitivity", 1.0)
                return
            except:
                pass
        self.brightness, self.sensitivity = 1.0, 1.0
        self.save_settings()

    def save_settings(self):
        with open(SETTINGS_FILE, 'w') as f:
            json.dump({"brightness": round(self.brightness, 2), "sensitivity": round(self.sensitivity, 2)}, f)

    def on_show_view(self):
        arcade.set_background_color(DARK_BG)

    def on_update(self, dt):
        self.pulse = (self.pulse + dt * 3) % (math.pi * 2)

    def on_draw(self):
        self.clear()
        self.draw_grid()
        if self.state == "main":
            self.draw_main()
        else:
            self.draw_settings()
        arcade.draw_text("v1.0", SCREEN_WIDTH - 50, 20, (80, 100, 130), 14)

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, 50):
            arcade.draw_line(x, 0, x, SCREEN_HEIGHT, (25, 40, 70, 120), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            arcade.draw_line(0, y, SCREEN_WIDTH, y, (25, 40, 70, 120), 1)

    def draw_main(self):
        size = 58 + math.sin(self.pulse) * 5
        arcade.draw_text(TITLE, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 90, CYBER_GREEN, size, anchor_x="center",
                         font_name="Arial", bold=True)
        arcade.draw_text("CYBER REALMS", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 130, CYBER_BLUE, 24, anchor_x="center",
                         font_name="Arial")
        items = ["НОВАЯ ИГРА", "НАСТРОЙКИ", "ВЫХОД"]
        for i, item in enumerate(items):
            y = SCREEN_HEIGHT / 2 + 30 - i * 80
            hover = i == self.selected
            glow = HOVER_GREEN if i != 1 else HOVER_BLUE
            if hover:
                arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, y, 280 + math.sin(self.pulse * 4) * 15, 55, (*glow, 40))
            color = HOVER_GREEN if hover and i != 1 else (
                HOVER_BLUE if hover and i == 1 else (CYBER_GREEN if i != 1 else CYBER_BLUE))
            arcade.draw_rectangle_rounded(SCREEN_WIDTH / 2, y, 270, 48, 12, color)
            arcade.draw_text(item, SCREEN_WIDTH / 2, y - 8, TEXT_COLOR, 25, anchor_x="center", font_name="Arial",
                             bold=True)
        arcade.draw_text("↑ ↓ ВЫБОР | ENTER ПОДТВЕРДИТЬ", SCREEN_WIDTH / 2, 60, (150, 200, 255), 16, anchor_x="center")

    def draw_settings(self):
        arcade.draw_text("СИСТЕМНЫЕ НАСТРОЙКИ", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 90, CYBER_BLUE, 38, anchor_x="center",
                         font_name="Arial", bold=True)
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 480, 260, (25, 35, 60, 230))
        arcade.draw_rectangle_outline(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 480, 260, CYBER_BLUE, 3)
        arcade.draw_text("ЯРКОСТЬ", SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT / 2 + 75, CYBER_GREEN, 22, anchor_x="left",
                         font_name="Arial", bold=True)
        self.brightness_slider.draw()
        arcade.draw_text(f"{self.brightness_slider.val:.2f}", SCREEN_WIDTH / 2 + 200, SCREEN_HEIGHT / 2 + 70,
                         TEXT_COLOR, 18, anchor_x="left")
        arcade.draw_text("ЧУВСТВИТЕЛЬНОСТЬ", SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT / 2 + 15, CYBER_BLUE, 22,
                         anchor_x="left", font_name="Arial", bold=True)
        self.sensitivity_slider.draw()
        arcade.draw_text(f"{self.sensitivity_slider.val:.2f}", SCREEN_WIDTH / 2 + 200, SCREEN_HEIGHT / 2 + 10,
                         TEXT_COLOR, 18, anchor_x="left")
        arcade.draw_rectangle_rounded(SCREEN_WIDTH / 2, 90, 180, 42, 10, (45, 60, 90))
        arcade.draw_text("НАЗАД (ESC)", SCREEN_WIDTH / 2, 82, CYBER_BLUE, 21, anchor_x="center", font_name="Arial",
                         bold=True)

    def on_key_press(self, key, _):
        if self.state == "main":
            if key == arcade.key.UP:
                self.selected = (self.selected - 1) % 3
            elif key == arcade.key.DOWN:
                self.selected = (self.selected + 1) % 3
            elif key == arcade.key.ENTER:
                if self.selected == 0:
                    print(f"Запуск: яркость={self.brightness:.2f}, чувств={self.sensitivity:.2f}")
                elif self.selected == 1:
                    self.state = "settings"
                elif self.selected == 2:
                    self.save_settings(); arcade.close_window()
        elif self.state == "settings" and key == arcade.key.ESCAPE:
            self.brightness = self.brightness_slider.val
            self.sensitivity = self.sensitivity_slider.val
            self.save_settings()
            self.state = "main"

    def on_mouse_motion(self, x, y, dx, dy):
        if self.state == "main":
            for i in range(3):
                btn_y = SCREEN_HEIGHT / 2 + 30 - i * 80
                if abs(x - SCREEN_WIDTH / 2) < 135 and abs(y - btn_y) < 24:
                    self.selected = i

    def on_mouse_press(self, x, y, button, _):
        if self.state == "main":
            for i in range(3):
                btn_y = SCREEN_HEIGHT / 2 + 30 - i * 80
                if abs(x - SCREEN_WIDTH / 2) < 135 and abs(y - btn_y) < 24:
                    if i == 0:
                        print(f"Запуск: яркость={self.brightness:.2f}, чувств={self.sensitivity:.2f}")
                    elif i == 1:
                        self.state = "settings"
                    elif i == 2:
                        self.save_settings(); arcade.close_window()
        elif self.state == "settings":
            self.brightness_slider.drag = abs(
                y - self.brightness_slider.y) < 25 and self.brightness_slider.x < x < self.brightness_slider.x + self.brightness_slider.w
            self.sensitivity_slider.drag = abs(
                y - self.sensitivity_slider.y) < 25 and self.sensitivity_slider.x < x < self.sensitivity_slider.x + self.sensitivity_slider.w

    def on_mouse_drag(self, x, y, dx, dy, buttons, _):
        if self.brightness_slider.drag: self.brightness_slider.update(x)
        if self.sensitivity_slider.drag: self.sensitivity_slider.update(x)

    def on_mouse_release(self, x, y, button, _):
        self.brightness_slider.drag = False
        self.sensitivity_slider.drag = False
        self.brightness = self.brightness_slider.val
        self.sensitivity = self.sensitivity_slider.val
        self.save_settings()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, resizable=False)
    window.show_view(MainMenu())
    arcade.run()


if __name__ == "__main__":
    main()