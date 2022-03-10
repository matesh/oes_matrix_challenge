import multiprocessing
from renderer_common import LED_COUNT, CLEAR_FRAME_INDEX, ROWS, COLUMNS
from traceback import print_exc
import os


class TerminalRenderer(multiprocessing.Process):
    def __init__(self, render_pipe, stop_signal, stopped_signal, render_delay=None):
        super(TerminalRenderer, self).__init__()

        self.render_pipe = render_pipe
        self.stop_signal = stop_signal
        self.stopped_signal = stopped_signal
        self.brightness = 255

        self.unsuccessful_renders = 0
        self.led_strip = [0] * LED_COUNT

    def run(self):
        try:
            while not self.stop_signal.is_set():
                if self.render_pipe.poll(0.05):
                    frame = self.render_pipe.recv()
                    for pixel in frame:
                        if pixel.index == CLEAR_FRAME_INDEX:
                            self.led_strip = [0] * LED_COUNT
                        else:
                            if pixel.colour.green == 0x0 and pixel.colour.red == 0x0 and pixel.colour.blue == 0x0:
                                self.led_strip[pixel.index] = 0
                            else:
                                self.led_strip[pixel.index] = 1

                    self.print_matrix()

        except KeyboardInterrupt:
            pass
        except Exception:
            print("Exception in renderer")
            print_exc()
        finally:
            print("Terminating renderer")
            self.stopped_signal.set()

    def print_matrix(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        frame = ""
        for row in range(0, ROWS):
            line = "{:2}|".format(row)
            for pixel in range(row*COLUMNS, (row+1)*COLUMNS):
                line += '*|' if self.led_strip[pixel] == 1 else " |"
            frame += line + os.linesep
        print(frame)


def initialise_renderer(render_delay=None):
    render_pipe_out, render_pipe_in = multiprocessing.Pipe(False)
    terminate_renderer = multiprocessing.Event()
    renderer_terminated = multiprocessing.Event()
    renderer = TerminalRenderer(render_pipe_out, terminate_renderer, renderer_terminated, render_delay=None)
    renderer.daemon = True
    renderer.start()
    return renderer, render_pipe_in, terminate_renderer, renderer_terminated
