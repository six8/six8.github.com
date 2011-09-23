--- 
layout: post
comments: true
title: "Install PIL in a virtualenv on Mac OSX Lion"
date: Tue Sep 20 02:19:15 -0500 2011
---

I work on a Mac but prefer to use Linux VMs (especially with [Vagrant](http://vagrantup.com)) for my development environment. Still, some things are small enough to not warrant a VM. Sometimes you just want to automate a process that's better done on OSX. In this case I wanted to automate some image manipulation with [PIL](http://www.pythonware.com/products/pil/).

There's several 'how to's around and [stackoverflow](http://stackoverflow.com/search?q=install+pil+mac) answers, but they all seem to want you to install extra dependancies or use [MacPorts](http://www.macports.org/) or [Brew](http://mxcl.github.com/homebrew/)'s Python. For this case I want to use the Python 2.7 that comes with Lion and install PIL inside a [virtualenv](http://pypi.python.org/pypi/virtualenv). I also want to use Brew at least for the things that aren't already installed with Lion.

[Installing PIL on mac osx with virtualenv, homebrew and pip](http://timetobefrank.blogspot.com/2011/05/installing-pil-on-mac-osx-with.html) gets you almost there but doesn't include freetype support. So I adapted it a bit. Here's what I ended up with:

1. Activate your virtual environment (I use [virtualenvwrapper](http://pypi.python.org/pypi/virtualenvwrapper)):

        workon default
    
2. Install jpeg libs with brew:

        brew install jpeg
    
3. Download the PIL source with pip, but don't install yet:

        pip install --upgrade --no-install PIL
    
4. Edit PIL's setup.py:

        vi $VIRTUAL_ENV/build/PIL/setup.py
    
5. Change `JPEG_ROOT` and `FREETYPE_ROOT`:

        JPEG_ROOT = '/usr/local/Cellar/jpeg/8c/'
        FREETYPE_ROOT = libinclude('/usr/X11')
    
6. Build:

        pip install --upgrade PIL
    
You should now have a complete install of PIL ready to go.