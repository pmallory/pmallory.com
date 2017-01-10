title: Color Cycling
date: 2014-3-28
category: Tech

<iframe width="420" height="315" src="//www.youtube.com/embed/8YNk2UNqWzo" frameborder="0" allowfullscreen></iframe>

Color cycling is a nifty technique from the days of yore for creating animations.
The key idea of color cycling is to modify the color palette an image uses rather than the image itself.
Since each pixel on the screen is refers to some color in the palette, it's possible to change many pixels at once by modifying the palette.
This takes much less time than redrawing the screen because the palette is significantly smaller than the video buffer itself.

In this demo the palette is rotated every screen refresh:

    palette[1] <- palette[2] ... <- palette[255]
        \_______________________________^

The source of this demo is on [GitHub](https://github.com/pmallory/gba_ColorCycling/).
The repo includes both the Game Boy code and a small Python program for generating palettes that cycle well.

More complicated color cycling is possible too.
Sim City 2000 used color cycling to drive almost all of its animations (road traffic, water flowing through pipes, even the screen on the drive in movie theaters).
More intricate examples can be found [here](http://www.effectgames.com/demos/canvascycle/?sound=0).
