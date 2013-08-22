Title: Fix for gray overlay on touch with iOS and Sencha Touch
Date: 2011-10-01
Tags: ios

I've been working on a Javascript based app for the iPhone. I was originally using [Phonegap](http://www.phonegap.com/) which basically renders an HTML5/Javascript app in a UIWebView. I was running in to an issue where when you click on about a 20 point area on any edge of the screen, a gray overlay would appear. Most answers to this problem suggest [using a transparent `-webkit-tap-highlight-color`](http://stackoverflow.com/search?q=webkit-tap-highlight-color) or setting `-webkit-user-select: none`. I'm using [Sencha Touch](http://www.sencha.com/products/touch/) which already does this to all elements by default. In order to isolate the issue, I spent hours narrowing down all the CSS, HTML, and Javascript to the bare minimum I could manage to reproduce it. 

I created a basic Phonegap app with [this gist](http://gist.github.com/1233975). Note that the issue only shows up if you have the status bar hidden (in this case with `UIStatusBarHidden` set to `YES`). Below is a screenshot of what it looks like. On the left is the regular view. On the right is what it looks like when you touch the edge of the screen. The effect is subtle, but enough to be annoying if your app requires clicking on the edge of the screen a lot. It ends up looking like the screen is flickering.

![Side by side image of iPhone](|filename|/images/2011/09/iphone-screen-overlay.jpg "Strange overlay on touch")

Once I was able to distill the issue down to [the basic code](http://gist.github.com/1233975) it was much easier to track down. Apparently the issue only appears when you add any one of the mouse events &ndash; `mouseup`, `mousedown`, `mousemove`, or `click` &ndash; to the document.

This bit is the main offender:

    ::::js
    document.addEventListener('click', function(){}, true);


Oddly enough this doesn't happen with any of the touch events &ndash; `touchup`, `touchdown`, or `touchmove`.

After digging around in Sencha code for a while (which seems to be the only way to understand Sencha Touch) I figured out that this is the offending code:

    ::::js
    Ext.gesture.Manager = new Ext.AbstractManager({

        // ...
        
        defaultPreventedMouseEvents: ['click'],

        // ...

        attachListeners: function() {
            Ext.iterate(this.eventNames, function(key, name) {
                document.addEventListener(name, this.listenerWrappers[key], false);
            }, this);

            if (Ext.supports.Touch) {
                // Right here the click event gets attached on a touch device.
                this.defaultPreventedMouseEvents.forEach(function(name) {
                    document.addEventListener(name, this.listenerWrappers['mouse'], true);
                }, this);
            }
        },
        
        // ...
    });


The `click` event ends up being attached to `document` when it's a touch device. I'm not sure what case prompted Sencha to do this, but I can't see any reason for it being here especially since it's the cause of this issue.

So the fix is simple. Instead of modifying Sencha's code, I just put this at the top of my Javascript after loading Sencha's Javascript:

    ::::js
    // Prevent sencha from attaching to the 'click' event which
    // will make a gray overlay appear when you touch the each of the screen.
    Ext.gesture.Manager.defaultPreventedMouseEvents = [];

Note that these issues were reproduced with Sencha Touch 1.1.0 and iOS 4.3 but may not be limited to these versions.

I tried googling other solutions of course, but could only find other reports such as [Flicker when tapping edge of viewport](http://www.sencha.com/forum/showthread.php?146243-Flicker-when-tapping-edge-of-viewport).