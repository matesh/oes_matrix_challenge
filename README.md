# Odyssey LED martix challenge introduction
Show us what you can throw together in an hour! You will write code to draw on my LED matrix.
It is a 17x17 matrix built out of WS812b LED pixels, which can be individually addressed and are
able to emit 16 million colours. Your work will be judged by (and only by) the non-coders in the
company, so impress them, not get stuck on your code style!

# Requirements
The code is written in python 3 and the required library (Pillow) that you need to install is in
the requirements.txt file. This is not necesary, but is used to render text in a helper method.
If you want to avoid installing it, just comment out the relevant code in `renderer_common.py`

# boilerplate.py
Your starting point, contains the example code. The code will be ran on a raspberry pi that 
controls the LED matrix. As you can see, the renderer runs in a separate process, so you will
have an entire raspberry pi 3 processor core to use for your image generation.

Put your code between the try: except sturcture, everything currently there can be removed.

## General recommendations:
- It is recommended to use the sleep routine in the boilerplate code for a stable and persistent
frame rate. 
- If the code runs poorly, the frame rate can be lowered
- The LED panel is pretty bright, I recommend dimming colours/pixels using the provided, it will come
though better on camera as well. A Brightness between 30 and 60 gives enough flexibility with colours
without being too aggressive. For the full 16 million colours, don't dim, but bear the consequences :)
- The thing runs on a £10 chinesium power supply, avoid turning on all LEDs at with all colours at
full brightness
- If you are animating, it is cheaper in terms of hardware resources, to turn of pixels that are not needed
in the next frame, instead of rendering an empty frame (clear screen) between frames. Sending the LED strip
data through i2c takes time and it may delay the rendering of the next frame causing frame drops.

# renderer_common.py
This contains constants and functions used by both the renderers and the code using the renderer.
Here you can find the definition of the LED panel, some constants for easier management (clearing)

`dim_individual_colour` allows the brightness to be applied to just a colour value (red or green for example)

`dim` will dim a colour tuple or an individual colour (interchangeable)

Pixels are custom named tuples as defined here Pxels are to be defined by the ID of the LED pixel on the strip 
and a colour, which is also a tuple. This provides flexibility for various effects, like the random
pixels in the example. The ID of a led pixel can be resolved from it's coordinates using the `get_pixel_index` function.

Colours are to be defined as a named tuple defined here.

# TerminalRenderer.py
This is a helper that allows the drawn picture to be rendered as ASCII characters in the terminal.
It's features are identical to the other renderers that I use live, so if your code runs in the terminal,
it should run on the matrix as well. I tested this renderer on multiple computers on macOS and Windows and
worked just fine, though it may not render perfectly smoothly in the terminal depending on the speed
of your computer.

# Submitting your code
- Any additional requirements/libraries your code needs, please include in the `requirement.txt`
- Create a pull request with your code
- Make the result pretty, not your code, this is not a coder dick weaving, you need to impress
the non-coders! :)
- Please submit your code an hour before the kickoff at latest, so I have time to deploy, test and
optimise if needed be!