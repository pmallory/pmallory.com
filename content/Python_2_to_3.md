title: Updating a Program from Python 2 to Python 3
date: 2017-3-9
category: Tech

I've been working with Python 2 and Python 3 codebases for a couple years now.
I write new code in Python 3 and maintain past work written in Python 2, but I've never ported a codebase from two to three.

This topic is interesting to me because the 2/3 split is a big deal in every Python-related thread on Hacker News, but despite Python being my go-to language of seven years the split hasn't ever bothered me much.

To explore the problem I decided to port a small program I wrote five years ago.
[PyLife](https://github.com/pmallory/pylife) is an implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) that uses the terminal as its display.
I wrote the program to practice a few things:

* Writing Python in a functional style. The program generates each generation as a function of the last.
* Using the [itertools](https://docs.python.org/3/library/itertools.html) library to practice using iterators.
* Using the [curses library](https://en.wikipedia.org/wiki/Curses_%28programming_library%29) to make text based interfaces.

You can view the most recent, Python 2/3 compatible, [code at GitHub](https://github.com/pmallory/pylife/blob/master/life.py)

The Porting Process
-------------------

I started porting by running the program with the python3 interpreter to see what errors I got.
The first one was an `ImportError` involving itertools.
I wasn't familiar with how the library had been changed and reorganized in Python 3 so I Googled for [an overview](http://www.diveintopython3.net/porting-code-to-python-3-with-2to3.html#itertools).
I found that Python 3's `filter` function and related functions use iterators under the hood, making itertool's `filter` function redundant.
I removed the bad import and replaced all calls to `itertools.ifilter` with calls to `filter`.

The next error was similar.
Python 2 provides the `range` and `xrange` functions to create sequences of integers.
`range` returns a list while `xrange` returns a faster and more memory-efficient generator.
In Python 3 `range` behaves like `xrange` does in Python 2 and in the inefficient version of the function is removed.
Updating my program required a minute of find-and-replacing.

And with that my program is Python 2/3 compatible!
The program no longer uses generator backed ranges when run as Python 2.
I could work around this, but the program performs fine so I don't think it's worth the trouble.

Conclusions
-----------

Small programs are trivial to port.
Larger programs that depend on libraries beyond the standard library could be harder.
Programs that explicitly handle text encoding are almost certainly harder to port.
