openmm_engine v0.3.1
========

Might and Magic 6-7-8 engine attempt.

- Author   : Alessandro Rosetti alessandro.rosetti@gmail.com
- License  : GPLv2 License

![ScreenShot](/res/screen_road_to_castle_ironfist.png)

Requirements
========

- python3
- pillow
- pyopengl
- numpy


WARNING: lod classes tested on mm6,7,8 but a few files are still failing to be extracted.

WARNING2: this program is being developed on linux. It's not currently being ever tested on other systems

Testing
========
You can play with the class methods, extract all data or search specific files.
- run: ./lod_test.py
       ./map_test.py

MM6 Opengl Engine Demo
----------
This is a simple messy opengl example with python3. It loads resources from mm6 lod files
and uses as textures,map,sprites :D

(the original example code has been taken from http://openglsamples.sourceforge.net/ and adapted to my needs)

WARNING: use data from mm6! (tested on gentoo linux)
- run: ./openmm_engine_test.py <mapcode>

the codes are the coordinates of the position of the map in Enroth
first char is one of a b c d e
second char is one of 1 2 3
'e3' is new new sorpigal

as you can se the map is currently messed up. (now is more like the first screen)

![ScreenShot](/res/screen_megatex.png)

Todo 
========
- LodManager class: cache of game data, create new lod files, other helpful functions.
- LodArchive: Threadsafe Lod* class ?
- GUI class:  buttons, decorators, animations etc...
- SndArchive class: snd files.
- 3D engine.... this hurts.
- The game logic ... take me to the temple please.

Comments
========
This is one of my first python projects.

Don't be shocked if you find the code horrorific, I don't know the language very well. ( I know C/C++ )

Why am I doing this?
There are a lot of lod extractors but none in python and I wanted to learn a bit of this magnificent language.

I'm doing this work for fun contact me if you want to help ;)

The current work is very very raw and there is no actual engine but mostly tests of modules, random code.

As soon as I see that the work is possible I hope to be able to clean the code and use a better architecture!

I found very helpful the documentations and the code of other projects like mm_mapview, mm8leveleditor, mm7view, and the new mm7 reverse engineering.
also this link: http://rewiki.regengedanken.de/wiki/Might_and_Magic_6


Insane future works
========
(sure, dream on... :P)
- FULL python/c implementation of 3DO's Might and Magic engine for mm6-7-8 and mods.
- new adventures from scratch!
- redo all 2.5D sprites to 3D models.
- better buildings/objects models, bump mapping stuff like that...

Disclaimer
========
I own these games, if you want to use this script buy the games. look at gog.com
All trademarks, product names are the property of their respective owners!
