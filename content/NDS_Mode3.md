title: Bitmap Graphics on the Nintendo DS - Part 2: Mode 3
date: 2014-2-27

This is the second post in a two post series on drawing and animating bitmap graphics on the Nintendo DS.
The first part is [here](bitmap-graphics-on-the-nintendo-ds-part-1-framebuffer-mode.html).

The biggest problem with frame buffer mode is that it could only draw on the DS's primary display.
To solve that issue we'll need to dig deeper into graphics hardware.

The Nintendo DS has a graphics engine for each display, and each engine can be run in one of several modes.
These engines can be set to drive tile maps, 3d layers and the simplest option: bitmap backgrounds.
The engine mode that lets us draw bitmaps on both screens is Mode 3.

Writing for Mode 3 starts off about the same as writing for frame buffer mode.
First we set the display control registers appropriately:

    :::c
    REG_DISPCNT_MAIN = MODE3 | BG3_ENABLE;
    REG_DISPCNT_SUB = MODE3 | BG3_ENABLE;

The engines driving both screens are now in Mode 3, and we've enabled background 3 on each.
Background 3 is an arbitrary choice, we could have enabled other backgrounds too if we were interested in using some sort of layering techniques.

Now we have to configure the background on each display.
This step wasn't necessary in frame buffer mode.

    :::c
    REG_BG3CNT =  BG_256x256 | BG_15BITCOLOR | BG_CBB1;
    REG_BG3CNT_SUB = BG_256x256 | BG_15BITCOLOR | BG_CBB1;

Both backgrounds are now large enough to fill their screens, in fact they're larger than necessary!
It's possible to scroll these around (for example if the background is displaying  a map).
It's also worth noting that you could have a background that's smaller than the screen if for instance you wanted to display a small UI element like a health indicator.

Now things get tricky.
Backgrounds on the DS have associated affine transformation matrices which let you scale, stretch and skew the background.
If you want to learn more you can read all about affine transformations in [TONC](http://www.coranac.com/tonc/text/affine.htm), an excellent resource on Nintendo programming.

That's beyond this article though, we just want to draw plain, undistorted images to the screen.
This implies that we want our transformation matrix to be an identity matrix (that is when we apply the matrix to our graphics they come through unmodified).
Here's what a 2d identity matrix looks like:

![Identity matrix](/static/images/identity_matrix.png)

So how do we get that into the DS?

First we need to know about [fixed point numbers](https://instruct1.cit.cornell.edu/Courses/ee476/Math/index.html).
Fixed point numbers are a way to represent numbers with fractional parts.
In our case a fixed point number is stored as a 16 bit unsigned value where the first eight bits store the integer part of the number and the last eight store the fractional part.
This scheme of splitting a 16 bit number into two parts is called 8:8 fixed point.

So how do we store 1.0 in fixed point?
The integer part is 1, so we put a 1 in the left byte.
The fractional part is 0, so we don't have to do anything with the right byte.

Let's put some 1.0s and 0.0s into the affine matrices:

    :::C
    REG_BG3PA = 1 << 8;
    REG_BG3PD = 1 << 8;

    REG_BG3PA_SUB = 1 << 8;
    REG_BG3PD_SUB= 1 << 8;

The letters A and D in those register names refer to which spot in the matrix that register is for:

![Affine matrix](/static/images/affinematrix.png)

Our code puts 1.0s into A and D of the affine matrices of both backgrounds.
The other spots are set to 0.0 when the Game Boy turns on so we can leave them as is.

Phew, now that we've got that settled we can finally draw things to the screen.
Fortunately this works almost the same way as it was in frame buffer mode:

    :::c
    void setPixel3_main(int row, int col, u16 color) {
        VIDEO_BUFFER_MAIN[OFFSET(row, col, SCREENWIDTH)] = color | PIXEL_ENABLE;
    }


    void setPixel3_sub(int row, int col, u16 color) {
        VIDEO_BUFFER_SUB[OFFSET(row, col, SCREENWIDTH)] = color | PIXEL_ENABLE;
    }

If this is unfamiliar head back to [the previous article](bitmap-graphics-on-the-nintendo-ds-part-1-framebuffer-mode.html) which covered OFFSET and color representation.
The only new thing here is PIXEL\_ENABLE.

Last time we learned that colors are represented by 16 bit numbers with 5 bits for each component, red, green and blue.
In frame buffer mode that remaining bit was simply ignored.
Here in Mode 3 it isn't ignored, if that bit isn't set the pixel isn't drawn.
This can be used for transparency if you're layering backgrounds.

setPixel() can be used as the basis for all sort of drawing functions:

    :::c
    void drawRect3_main(int row, int col, int width, int height, u16 color) {
        int r, c;
        for (c=col; c<col+width; c++) {
            for (r=row; r<row+height; r++) {
                setPixel3_main(r, c, color);
            }
        }
    }

A corresponding function can be written for the secondary display.

Here's a screen shot of all this in action:

![Mode 3 demo](/static/images/mode3.png)

We've got the same bouncing ball from last time on the main display, and a rectangle and line hanging out on the secondary display.

If you'd like to browse the source of this demo or download the code head on over to [GitHub](https://github.com/pmallory/nds_mode3_bitmaps).
You can also [download the ROM](/static/bin/nds_mode3_bitmaps.nds) to run in an emulator.

Further Reading
---------------
There really aren't many good written resources on programming the Nintendo DS.

A very thorough [spec sheet](http://nocash.emubase.de/gbatek.htm) exists which explains the memory layout, control registers and other low level details.

There's also [libNDS](http://libnds.devkitpro.org/), a community developed API for programming the DS.
An API reference exists and there's lots of example code.

For a conceptual overview of Game Boy Advanced programming you can check out [TONC](http://www.coranac.com/tonc).
While it isn't directly applicable to the DS is it very very close.
Many topics (buttons, affine transformations, DMA, etc ) are identical or nearly identical on the GBA and DS.
