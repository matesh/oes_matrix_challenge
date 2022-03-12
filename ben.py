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

# red, green, or blue (based on https://stackoverflow.com/a/28999469/6837300)
def get_random_color():
  rgbl=[0xFF,0x00,0x00]
  random.shuffle(rgbl)
  return tuple(rgbl)

# Brightness 1 so it doesn't burn my retina
BRIGHTNESS = 1

# Framerate in FPS
FRAMERATE = 20
FRAME_TIME = (60/FRAMERATE)/60

if __name__ == "__main__":

    shutdown = False

    # Renderer initialisation
    renderer, render_pipe, terminate_renderer, renderer_terminated = initialise_renderer(render_delay=2)

    try:
        while not shutdown:

            colour_rgb = get_random_color()
            colour = Colour(colour_rgb[0], colour_rgb[1], colour_rgb[2])

            # Render the text
            render_text("Ben is cool!!", render_pipe, dim(colour, BRIGHTNESS))
            time.sleep(1)
             # Clearing matrix by putting the pre-defined CLEAR_FRAME into the render pipe
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
