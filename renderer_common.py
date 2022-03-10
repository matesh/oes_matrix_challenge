from collections import namedtuple
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time

# Use this special pixel index to trigger a fast and efficient clear (turn off) of all pixels on the board
CLEAR_FRAME_INDEX = 0XBEEF

# This is used to define a colour. Colours are integers between 0x00-0xFF (0-255), as per the hex
# colour coding definition. Purple for instance is 0xff00ff -> Colour(0xFF, 0x00, 0xFF)
Colour = namedtuple("Colour", ["red", "green", "blue"])

# This is used to define a pixel that is to be inserted into the render queue.
# Index is its position on the matrix (more precisely it's index in the led strip)
# Colour is the colour tuple that contains the hex of the 3 base colours
Pixel = namedtuple("Pixel", ["index", "colour"])

# Render this pixel to trigger a fast and efficient clear (turn off) of all pixels on the board
CLEAR_FRAME_PIXEL = Pixel(CLEAR_FRAME_INDEX, None)

# Render this frame to trigger a fast and efficient clear (turn off) of all pixels on the board
CLEAR_FRAME = [CLEAR_FRAME_PIXEL]

# Turned off pixel colour
DARK = Colour(0x00, 0x00, 0x00)

# An example pixel that can be inserted into the render pipe for rendering
EXAMPLE_PIXEL = Pixel(2, Colour(0x00, 0x01, 0x00))

# Current LED board size definition
ROWS = 17
COLUMNS = 17
LED_COUNT = ROWS * COLUMNS


def dim_individual_colour(colour, brightness):
    """
    Dims an individual colour
    :param colour: int 0-255
    :param brightness: brightness 0-255
    :return: dimmed colour
    """
    new_colour = (float(brightness) / 255) * float(colour)
    if new_colour < 0:
        return 1
    if 255 < new_colour:
        return 255
    return int(new_colour)


def dim(colour, brightness):
    """
    Dims a colour
    """
    try:
        return Colour(dim_individual_colour(colour.red, brightness),
                      dim_individual_colour(colour.green, brightness),
                      dim_individual_colour(colour.blue, brightness))
    except Exception:
        try:
            return dim_individual_colour(colour, brightness)
        except Exception:
            return colour


def render_text(text, render_pipe_input, text_colour):
    """
    Method to render text on the matrix
    :param text: The text to be rendered
    :param render_pipe_input: The render pipe in which the rendered frames are to be inserted
    :param text_colour: The colour to be used when rendering, Colour named tuple
    :return:
    """
    font = ImageFont.truetype('UbuntuMono-B.ttf', 17)  # load the font
    size = font.getsize(text)  # calc the size of text in pixels
    image = Image.new('1', size, 1)  # create a b/w image
    draw = ImageDraw.Draw(image)
    draw.text((0, -1), text, font=font)  # render the text to the bitmap
    column = 0
    while column + 17 < size[0]:
        start = time.time()
        render_pixels = []
        for index, column_to_render in enumerate(range(column, column + 17)):
            for row_to_render in range(2, size[1]):
                if image.getpixel((column_to_render, row_to_render)):
                    render_pixels.append(Pixel(get_pixel_index(index, row_to_render-1), DARK))
                else:
                    render_pixels.append(Pixel(get_pixel_index(index, row_to_render-1), text_colour))
        render_pipe_input.send(render_pixels)
        if column == 0:
            time.sleep(.5)
        else:
            try:
                time.sleep(0.05 - (time.time() - start))
            except Exception:
                pass
        column += 1


def draw_rectangle(x, y, a, b, colour, fill=False):
    """
    Draws a rectangle
    :param x: top left corner x coordinate
    :param y: top left corner y coordinate
    :param a: horizontal side length
    :param b: vertical side length
    :param colour: the colour of the rectangle
    :param fill: fill, true or false
    :return: rectangle frame
    """
    to_return = []
    if fill:
        for i in range(0, a):
            for j in range(0, b):
                to_return.append(Pixel(get_pixel_index(x+i, y+j), colour))
    else:
        for i in range(0, a):
            to_return.append(Pixel(get_pixel_index(x+i, y), colour))
            to_return.append(Pixel(get_pixel_index(x+i, y+b-1), colour))
        for j in range(1, b-1):
            to_return.append(Pixel(get_pixel_index(x, y+j), colour))
            to_return.append(Pixel(get_pixel_index(x + a-1, y + j), colour))
    return to_return


def left_to_right_top_to_bottom(x, y):
    """
    Transformation from x/y coordinate to an index of the pixel on the LED strip
    :param x: x coordinate
    :param y: y coordinate
    :return: the index on the LED strip
    """
    if y < 0 or x < 0 or ROWS <= y or COLUMNS <= x:
        raise ValueError("Invalid coordinate)")
    return y * COLUMNS + x


# Transformation appropriate for this LED setup
get_pixel_index = left_to_right_top_to_bottom
