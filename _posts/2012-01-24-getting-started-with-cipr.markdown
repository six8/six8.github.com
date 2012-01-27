--- 
layout: post
comments: true
title: "Getting Started with Cipr"
date: Tue Jan 24 15:25:47 -0600 2012
---

Now Just WTF is Cipr?
---------------------

[Cipr](http://github.com/six8/corona-cipr) (pronounced "sipper") is part package manager, part development framework for [Corona SDK](http://www.anscamobile.com/corona/). Much like Python's [pip](http://pypi.python.org/pypi/pip), Cipr makes it easier to share packages and integrate them into Corona apps. The Goal for Cipr is that there's a generous amount of third-party, best-of-breed packages available for use in Corona apps. This will help new developers get started developing apps sooner and reduce the re-inventing of the wheel for every app.

Installing Cipr
---------------

Cipr is developed with [Python](http://python.org/) and currently only supports Mac OSX. Installing is simple on Macs because it comes with Python installed. If you're familiar with Python you can install Cipr with [pip](http://pypi.python.org/pypi/pip) or [easy_install](http://pypi.python.org/pypi/setuptools) either globally or, as preferred, in a [virtualenv](http://pypi.python.org/pypi/virtualenv). 

For those new to Python, don't worry, you don't need to know it. You can simply install Cipr with this command on the terminal:

	sudo easy_install cipr

This installs the `cipr` command line utility. All your interaction with Cipr is through this command. You can get a list of available commands with:

    cipr -h
    
Your First Project
------------------

Cipr considers each app a Project. Cipr can be used on an existing project, but for this tutorial let's create an empty project:

    mkdir /tmp/hellocipr
    cd /tmp/hellocipr
    cipr init

`cipr init` initializes the current directory as a Cipr project. It will copy in the default Cipr skeleton files which includes a basic `build.settings`, `config.lua`, and `main.lua`. These are some of the files every Corona project has. `cipr init` also adds `cipr.lua`. This is the basic development package loader for Cipr. It should not be modified as Cipr will overwrite it with the production version during build.

This project will run at this point, but won't do anything useful. Cipr isn't entirely useful on it's own, so lets install a package:

    cipr install git://github.com/six8/cipr.logging.git
    
As you can see, most Cipr packages are git repositories starting with `git://`. You can install packages from a directory as well, but this is generally only needed for package developers.

See what packages are now installed:

    cipr packages -l

You should see something like this:
    
    - cipr.logging
      - directory: /tmp/hellocipr/.cipr/packages/cipr.logging
      - source: git://github.com/six8/cipr.logging.git
      
Now lets try out our new package. Open up `main.lua` in your favorite editor and make it look like this:

    -- Initialize cipr
    local cipr = require 'cipr'
    -- Use cipr to import the logging package
    local logging = cipr.import 'cipr.logging'
    -- Create a logger for this file (... is automatically replaced with this file name)
    local log = logging.getLogger(...)
    log:setLevel(log.DEBUG)

    local x = 1

    log:info('Started')
    log:debug('the value of `x` is %s', x)  
    
Now we're ready to run this with Corona:

    cipr run
    
You should now see something like the following in your terminal:

    20120124T16:46:10 [root] INFO    Started
    20120124T16:46:10 [root] DEBUG   the value of `x` is 1    
    
As you can see, this started Corona and ran our little app which pretty much only does logging at this point. You can now either exit Corona via the UI or hit `ctrl+C` in the terminal.

### Let's Do More

We can add other packages to our project. Furthermore, those packages can declare dependencies that will pull in other packages. We can install `cipr.ui`, a collection of UI helpers for Corona:

    cipr install git://github.com/six8/cipr.ui.git
    
This will produce a lot more output since it's also installing its dependencies. `cipr packages` should now look more like this:

    - cipr.ui
    - cipr.class
    - middleclass-extras
    - middleclass
    - cipr.logging

[cipr.class](http://github.com/six8/cipr.class) uses [middleclass](http://github.com/kikito/middleclass) for classes in lua. [cipr.ui](http://github.com/six8/cipr.ui) depends on `cipr.class` so it and all of its dependencies are installed.

Let's change `build.settings` so our app is in landscape mode:

    settings = {
        orientation = {
            default = "landscapeLeft",
            supported = {
                "landscapeLeft", "landscapeRight",
            },
        },
        iphone = {
            plist = {
                CFBundleIconFile = "Icon.png",
                CFBundleIconFiles = {
                    "Icon.png" ,
                    "Icon@2x.png" ,
                    "Icon-72.png" ,
                    "Icon-Small.png" ,
                    "Icon-Small@2x.png",
                    "Icon-Small-50.png"
                },
                -- When set to TRUE turns off the gloss,
                -- but leaves the rounded edges.
                UIPrerenderedIcon = true,
                UIStatusBarHidden = true,
                UIInterfaceOrientation = "UIInterfaceOrientationLandscapeLeft",
 
                UISupportedInterfaceOrientations = {
                    "UIInterfaceOrientationLandscapeLeft",
                    "UIInterfaceOrientationLandscapeRight"
                },                        
            },
        }
    }

Now let's modify `main.lua` so we can test out `cipr.ui`'s `DebugBar`:

    local cipr = require 'cipr'
    local log = cipr.import('cipr.logging').getLogger(...)
    log:setLevel(log.DEBUG)
    -- Use cipr to import the ui package
    local DebugBar = cipr.import 'cipr.ui.DebugBar'

    log:info('Started')

    display.setDefault('background', 100, 100, 100)
    display.setStatusBar( display.HiddenStatusBar )

    DebugBar:new()
    
Now `cipr run` the project to see the results. You should see a mostly gray screen. Slide the arrow at the top right to the left. This will drag out the DebugBar drawer that shows some useful debug info. You can use this to help with your app development. To disable it for production apps you simply remove or disable `DebugBar:new()`.

Exploring Some Existing Packages
--------------------------------

Since Cipr is in early development, only a few packages exist. [cipr.ui](http://github.com/six8/cipr.ui) is one of the most useful of the new packages. Let's take a look at some of it's features. 

### EffectChain

Transitions are a powerful feature of Corona. Often you need to run several transitions on a single object before finally destroying it. In this example,
we'll create a mini-particle engine that will use [EffectChain](http://github.com/six8/cipr.ui/blob/master/cipr/ui/EffectChain.lua) to power animations.

Add this to your `main.lua` and `cipr run` it:

    local EffectChain = cipr.import 'cipr.ui.EffectChain'
    local random = math.random

    local particleGroup = display.newGroup()

    -- EffectChains are re-usable
    local popBubble = EffectChain():
        fadeIn{time=500}:
        transition{y=10, time=400, transition=easing.inExpo}:
        scale{scale=4, alpha=0,time=200}:
        call(display.remove)
    
    --[[
    Create a randomly sized particle and make it float and pop
    ]]--
    local function addNewParticle()
        local x = random(20, display.contentWidth - 20)
        local y = random(100, display.contentHeight - 20)
        local particle = display.newCircle(particleGroup, x, y, random(5, 20))
        particle:setFillColor(255, 255, 255, 200)

        -- Clone the EffectChain for this particle and play it
        popBubble:on(particle):play()
    end 

    timer.performWithDelay(100, addNewParticle, -2)
    
You should now see what looks like a bubbly drink. Don't forget to try out the DebugBar to see how it performs.

### ParallaxView

Almost every 2D game has a Parallax background. [ParallaxView](http://github.com/six8/cipr.ui/blob/master/cipr/ui/widgets/ParallaxView.lua) makes it easy to create these types of backgrounds.

Add this to your `main.lua` and `cipr run` it:

    local ParallaxView = cipr.import 'cipr.ui.widgets.ParallaxView'

    local view = display.newGroup()
    local background = display.newGroup()
    view:insert(background)
    -- Put our particle group from earlier on top
    view:insert(particleGroup)

    local pview = ParallaxView(display.contentWidth, display.contentHeight)
    background:insert(pview)
    background.y = display.contentHeight

    -- This layer moves at 1/4 the speed
    local layer1 = pview:newLayer(0.25)

    local bgA = display.newRect(0, 0, 400, 220)
    bgA:setFillColor(120, 120, 120)

    local bgB = display.newRect(0, 0, 400, 280)
    bgB:setFillColor(140, 140, 140)

    local bgC = display.newRect(0, 0, 400, 200)
    bgC:setFillColor(160, 160, 160)

    layer1:addCol(bgA)
    layer1:addCol(bgB)
    layer1:addCol(bgC)  

    -- This layer moves at half the speed
    local layer2 = pview:newLayer(0.5)

    -- A layer must have at least 2 columns. The width of all 
    -- the cols combined must be at least the width of the view
    -- in order to loop properly
    local bg1 = display.newRect(0, 0, 300, 120)
    bg1:setFillColor(90, 90, 90)

    local bg2 = display.newRect(0, 0, 300, 80)
    bg2:setFillColor(50, 50, 50)

    local bg3 = display.newRect(0, 0, 300, 100)
    bg3:setFillColor(75, 75, 75)

    layer2:addCol(bg1)
    layer2:addCol(bg2)
    layer2:addCol(bg3)


    local x = 0
    local function enterFrame()
        x = x + 10
        pview:scrollTo(x, 0, 1)    
    end

    Runtime:addEventListener('enterFrame', enterFrame)

You should see a couple layers of backgrounds scrolling by at different rates.

Explore [cipr.ui](http://github.com/six8/cipr.ui) for many other useful utilities. 

Building
--------

To run your app for the Xcode simulator or submit it to the App store, you'll need to build it.

To build:

    cipr build
    
This will package up all the files for your project under your project's `build` directory. Unfortunately, Corona doesn't support command line parameters so you'll have to build it from the Corona UI. Select your project's `dist/Payload` directory as the place to output the built app. Once your project is built, you can easily package it as an IPA:

    cipr packageipa

What's Next?
------------

Cipr is currently in development. It's being used as the basis for several games actively in development. It has a ways to go before it's production ready so use at your own risk. Any contributions to get Cipr further along will be greatly appreciated. Take a look at [Cipr](http://github.com/six8/corona-cipr) and [cipr.ui](http://github.com/six8/cipr.ui) and see if it will ease your development with Corona.

### Source Control

One last note. All projects should of course be using source control. Cipr needs `.ciprcfg` which it creates at the root of your project. This file should be added to your source control. Cipr also creates a `.cipr` directory in your project. This is where it maintains installed packages. This directory should generally be excluded from source control as it may have many large packages. You should also exclude the `build` and `dist` directories.

Since `.cipr` isn't generally checked in, this poses a problem if you are sharing code with others. To install a project's required packages, run the following in the project's directory:

    cipr install
