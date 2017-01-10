title: Bitmap Graphics on the Nintendo DS - Part 1: Framebuffer mode
date: 2014-2-1
category: Tech

This is the first post in a two part series on drawing and animating bitmap graphics on the Nintendo DS.
The second part is [here](bitmap-graphics-on-the-nintendo-ds-part-2-mode-3.html).

The simplest way to draw graphics on the DS is frame buffer mode.
Frame buffer most is the closest analogue to the Game Boy Advance's bitmap modes.
In frame buffer mode one of the video memory blocks is designated as the frame buffer.
Each short in that block represents one pixel and the format of that short is XBBBBBGGGGGRRRRR.
The least significant five bits are the pixel's red intensity, the next five are green and the last are blue.
This means that each color component can take a value from 0 to 31.
The most significant bit, denoted by an 'X', is ignored.

Putting the DS in frame buffer mode is a two step process.
First the main screen's display control register is set to frame buffer mode:

    :::c
    REG_DISPCNT_MAIN = MODE_FB0;

Then we enable the video memory bank that corresponds to the specific frame buffer mode we're in:

    :::c
    VRAM_A_CR = VRAM_ENABLE;

In this case we enable VRAM bank A since we're in frame buffer mode 0, if we'd chosen MODE\_FB1 we would enable VRAM\_B.
MODE\_FB2 and FB3 likewise correspond with VRAM banks C and D.

With frame buffer mode enabled we can draw to the main screen by writing to the video bank.

    :::c
    void setPixel(int row, int col, u16 color) {
        VRAM_A[OFFSET(row, col, SCREENWIDTH)] = color;
    }

It's pretty simple, the only complication is calculating the index of a particular pixel.
The video memory is just a contiguous chunk of memory, it doesn't know anything about rows or columns.
Directly after row one (pixels 0 through 255) comes row two (pixels 256 through 511), and so on all the way down the screen.
This index can be calculated with a quick macro:

    :::c
    #define OFFSET(r,c,w) ((r)*(w)+(c))

That's everything you need to draw an image, but there's one more piece need to enable animation.
In order to move an object on the screen you need to draw an image, wait a bit, then redraw it in a new position.
We know how to do the drawing parts, but what about waiting?

The best approach is to wait until the display is in vertical blank to redraw the screen.
Vertical blank is the time in which the display isn't updating.
After the last row of pixels is drawn the video hardware waits a bit before returning to the top of the screen to begin redrawing.
This vertical blank period occurs about 60 times a second.
If we only update the framebuffer during these vertical blanks our game will animate at a reasonable 60 fps.
Another benefit of drawing during vblank is that the video memory isn't being modified as it's being drawn to the screen which would lead to glitchy graphical tearing.

So how do we use this vblank time?
The DS provides a register that keeps track of which scanline is currently being drawn.
If we wait until the value in the scanline register ticks past the last row of the display we know we're in vblank.

    :::c
    #define SCANLINECOUNTER   *(vu16 *)0x4000006
    #define SCREENHEIGHT (192)
    void waitForVblank() {
        while (SCANLINECOUNTER > SCREENHEIGHT);
        while (SCANLINECOUNTER < SCREENHEIGHT);
    }

So that's frame buffer mode.
I've made a demo that puts it all together:
<video width="480" height="476" controls>
    <source src="/static/bin/ndsfb.mp4" type="video/mp4">
    Your browser does not support HTML5 video.
</video>

You can browse the source of this demo on [GitHub](https://github.com/pmallory/nds_framebuffer_bitmaps).
If you'd like to run the demo in an emulator you can [download the ROM](/static/bin/nds_framebuffer_bitmaps.nds).

So what are the downsides of frame buffer mode?
The most obvious limitation is that it only lets you draw to one of the DS's screens.
Frame buffer mode is also less featureful than the other modes and doesn't really demonstrate how configurable the DS's graphics hardware is.

These problems are addressed by Mode 3, which is covered in [the next post in this series](bitmap-graphics-on-the-nintendo-ds-part-2-mode-3.html).
