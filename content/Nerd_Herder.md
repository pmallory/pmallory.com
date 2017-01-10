title: Nerd Herder
date: 2011-10-10
category: Tech

Nerd Herder is an arcade style game for the Gameboy Advance.

![splash screen](/images/NerdSplash.png)

Your goal as head TA is to guide your students to their academic destinies. You
do this by chasing the best and brightest students to the dorm to study, while
driving the less capable to the M-Train¹. At your disposal are your passion
for quality education and two power ups. A readme is included with the ROM with
a more complete description of gameplay.

![action shot](/images/NerdGameplay.png)

The game is written in C. The nifty technical features include:

* Direct Memory Access (DMA) to load the tiles/tile map, sprites, color palette, and to keep the sound buffer full
* Animated sprites with transparency
* Scrolling background
* Music (pcm encoded, not beeps and boops)
* Inline assembly to access BIOS functionality

Download ROM and Readme: [NerdHerder](/static/bin/NerdHerder.zip)

Browse Source: [GitHub repo](https://github.com/pmallory/NerdHerder)

***

¹At Georgia Tech, to “board the M-Train” is to transfer from a science or engineering major to management. Refer to [Urban Dictionary](http://www.urbandictionary.com/define.php?term=m-train) or this [informational music video](http://www.youtube.com/watch?v=0NzNKKrYHqY).
