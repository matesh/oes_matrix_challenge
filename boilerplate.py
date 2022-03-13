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
        # Render the text "Odyssey" on the board
        render_text("Odyssey", render_pipe, dim(COLOUR, BRIGHTNESS))
        time.sleep(1)

        # Clearing matrix by putting the pre-defined CLEAR_FRAME into the render pipe
        render_pipe.send(CLEAR_FRAME)

        # Defining Odyssey orange
        oes_orange = Colour(0xE7, 0x59, 0x25)
        oes_red = Colour(0xBE, 0x3A, 0x26)

        oes_orange_xs = [0,0,0,0,0,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,7,7,7,7,7,7,7,8,8,8,8,8,8,9,9,9,9,10,10,10,10,11,11,11,11,11,11,12,12,12,12,12,12,13,13,13,13,14,14]
        oes_orange_ys = [6,7,8,9,10,4,5,6,7,8,9,10,11,12,3,4,5,6,7,8,9,10,11,12,13,2,3,4,7,8,9,12,13,14,1,2,3,7,8,9,13,14,15,0,1,2,7,8,9,14,15,16,0,1,7,8,9,15,16,0,1,7,8,9,15,16,0,1,8,9,15,16,0,1,15,16,0,1,15,16,0,1,2,14,15,16,1,2,3,13,14,15,2,3,13,14,3,13]

        oes_red_xs = [13,13,13,13,14,14,14,14,14,14,14,14,15,15,15,15,15,15,15,15,15,16,16,16,16,16]
        oes_red_ys = [4,5,11,12,4,5,6,7,9,10,11,12,4,5,6,7,8,9,10,11,12,6,7,8,9,10]

        frame = []

        for i in range(len(oes_orange_xs)):
            pixel = Pixel(get_pixel_index(oes_orange_xs[i], oes_orange_ys[i]), oes_orange)
            frame.append(pixel)

        for i in range(len(oes_red_xs)):
            pixel = Pixel(get_pixel_index(oes_red_xs[i], oes_red_ys[i]), oes_red)
            frame.append(pixel)
        
        # Send the frame for rendering
        render_pipe.send(frame)
        time.sleep(5)
        render_pipe.send(CLEAR_FRAME)

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
