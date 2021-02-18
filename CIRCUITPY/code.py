import time
import board
import terminalio
import displayio
import busio
from adafruit_display_text import label
import adafruit_st7789
import digitalio
import adafruit_imageload

displayio.release_displays()

# buttons
A = digitalio.DigitalInOut(board.GP12)
A.switch_to_input(pull=digitalio.Pull.UP)
B = digitalio.DigitalInOut(board.GP13)
B.switch_to_input(pull=digitalio.Pull.UP)
X = digitalio.DigitalInOut(board.GP14)
X.switch_to_input(pull=digitalio.Pull.UP)
Y = digitalio.DigitalInOut(board.GP15)
Y.switch_to_input(pull=digitalio.Pull.UP)

# pins for the display
tft_cs = board.GP17
tft_dc = board.GP16
spi_mosi = board.GP19
spi_clk = board.GP18
spi = busio.SPI(spi_clk, MOSI=spi_mosi)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = adafruit_st7789.ST7789(
    display_bus, width=135, height=240, rowstart=40, colstart=53
)
display.rotation = 180

# create a display group
screen = displayio.Group(max_size=10)
display.show(screen)

# white border
color_bitmap = displayio.Bitmap(135, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF

bg_sprite = displayio.TileGrid(
    color_bitmap, pixel_shader=color_palette, x=0, y=0)
screen.append(bg_sprite)

# pink background
inner_bitmap = displayio.Bitmap(131, 236, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xF22A70
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=2, y=2)
screen.append(inner_sprite)

happy_birthday = displayio.Group(max_size=10, scale=1, x=24, y=40)
hb_label = label.Label(terminalio.FONT, text="happy birthday", color=0xFFFFFF)
happy_birthday.append(hb_label)

abe = displayio.Group(max_size=10, scale=3, x=39, y=62)
# LabeL lABEl
abe_label = label.Label(terminalio.FONT, text="ABE", color=0x6600CC)
abe.append(abe_label)  # Subgroup for text scaling

screen.append(happy_birthday)
screen.append(abe)

tomto = displayio.Group(max_size=10, scale=2, x=40, y=120)

tomto_sprite_sheet, tomto_palette = adafruit_imageload.load(
    "ABETOMTO.BMP",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette,
)

tomto_palette.make_transparent(0)
tomto_sprite = displayio.TileGrid(
    tomto_sprite_sheet,
    width=1,
    height=1,
    tile_width=26,
    tile_height=26,
    pixel_shader=tomto_palette,
)
# tomto_sprite[0] = 0
tomto.append(tomto_sprite)
screen.append(tomto)

while True:
    # the buttons are True unless they are pressed
    # feels the wrong way round, but hoo-hoo!
    if not B.value:
        inner_palette[0] = 0x00ff00
        hb_label.color = 0x000000
        abe_label.color = 0x660066
    if not Y.value:
        inner_palette[0] = 0x000000
        hb_label.color = 0xffffff
        abe_label.color = 0xf2257a
    if not A.value:
        if tomto_sprite[0] < 4:
            tomto_sprite[0] += 1
        time.sleep(0.2)
    if not X.value:
        if tomto_sprite[0] > 0:
            tomto_sprite[0] -= 1
        time.sleep(0.2)
