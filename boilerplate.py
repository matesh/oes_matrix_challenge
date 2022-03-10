import traceback
import random
import time
import sys
from renderer_common import Colour, Pixel, ROWS, COLUMNS, LED_COUNT, CLEAR_FRAME, dim, draw_rectangle, render_text, get_pixel_index

# Renderer selection according to argument. By default, it's the terminal renderer, other renderers will be used live.
if "pi" in sys.argv:
    from RaspberryPiRenderer import initialise_renderer
elif "nightdriver" in sys.argv:
    from NightDriverRenderer import initialise_renderer
else:
    from TerminalRenderer import initialise_renderer


def get_random_pixel():
    """
    returns a random pixel ID
    :return:
    """
    return random.randint(0, ROWS * COLUMNS - 1)


# Brightness 1 so it doesn't burn my retina
BRIGHTNESS = 1

# Framerate in FPS
FRAMERATE = 20
FRAME_TIME = (60/FRAMERATE)/60

# White colour just for the demonstration
COLOUR = Colour(0xFF, 0xFF, 0xFF)


if __name__ == "__main__":

    shutdown = False

    # Renderer initialisation
    renderer, render_pipe, terminate_renderer, renderer_terminated = initialise_renderer(render_delay=2)

    try:

        # Putting a single red pixel on the LED matrix using x, y coordinates
        # Defining the red colour
        colour = Colour(0xFF, 0x00, 0x00)

        # Defining the coordinates of the pixel. The top left pixel of the matrix is 0,0 and
        # currently it has 17 rows and 17 columns (rows 0-16 and columns 0-16)
        x = 3
        y = 13

        # Defining the actual pixel
        pixel = Pixel(get_pixel_index(x, y), colour)

        # Defining a frame, which is a list of  pixels.
        # A frame (list of pixels) is the unit that can be rendered.
        frame = [pixel]

        # Send the frame for rendering
        render_pipe.send(frame)

        # Draw two rectangles and wait 3s. Shows that putting a new frame in the render pipe doesn't
        # clear the empty pixels in the new frame
        render_pipe.send(draw_rectangle(3, 3, 5, 8, dim(COLOUR, BRIGHTNESS)))
        render_pipe.send(draw_rectangle(9, 9, 3, 6, dim(COLOUR, BRIGHTNESS), fill=True))
        time.sleep(3)

        # Clearing matrix by putting the pre-defined CLEAR_FRAME into the render pipe
        render_pipe.send(CLEAR_FRAME)

        # Render the text "Hello world" on the board
        render_text("Hello world", render_pipe, dim(COLOUR, BRIGHTNESS))
        time.sleep(1)

        # Clearing matrix by putting the pre-defined CLEAR_FRAME into the render pipe
        render_pipe.send(CLEAR_FRAME)

        # Continuously running random pixel pattern thing
        active_pixels = []
        MAX_ACTIVE_PIXELS = 50

        counter = 0
        while not shutdown:
            start = time.time()
            pixels_to_render = []
            pixel = get_random_pixel()
            while pixel in active_pixels:
                pixel = get_random_pixel()
            active_pixels.append(pixel)
            pixels_to_render.append(Pixel(pixel, dim(COLOUR, BRIGHTNESS)))
            if MAX_ACTIVE_PIXELS < len(active_pixels):
                turn_off_pixel = active_pixels.pop(0)
                pixels_to_render.append(Pixel(turn_off_pixel, Colour(0x00, 0x00, 0x00)))
            render_pipe.send(pixels_to_render)

            # Recommended wait between frame renders to maintain a stable FPS and allow overruns
            try:
                time.sleep(FRAME_TIME - (time.time() - start))
            except Exception:
                pass

        print("Terminating")
        render_pipe.send(CLEAR_FRAME)

    except KeyboardInterrupt:
        pass
    except Exception:
        print("Exception in main loop")
        traceback.print_exc()
    finally:
        print("Terminating renderer")
        terminate_renderer.set()
        while not renderer_terminated.is_set():
            time.sleep(0.1)
        print("All processes stopped")
