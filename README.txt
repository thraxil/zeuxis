This is a simple utility for artists.

The basic idea is to simulate a figure drawing class with timed
poses. Going to a real, live session with a real model is obviously
ideal, but not always practical. With this utility, you point it at a
directory of images or an Atom feed (eg, from Flickr) and tell it how
long "poses" should last and it displays random images from that
source for a while until you stop it. It also shows you a countdown
timer in the corner so you actually know how much time you have left
for that pose. 

Basic Example Usage:

 % sketch.py 300 ~/images/poses/*.jpg 

That will tell it to draw random images from your "~/images/poses/"
directory and do 5 minute (300 seconds) poses. Hit 'q' to exit. 

To pull images from an Atom feed:

 % sketch.py 300 -u 'http://api.flickr.com/services/feeds/photos_public.gne?tags=turtle&lang=en-us&format=atom'

That will do 5 minute poses of public photos on flickr with the
'turtle' flag. (Hey, I like drawing turtles). 

Some extra features are available:

  * grayscale: hit 'g' to toggle grayscale vs color display (if you
    just want to do value studies)
  * posterize: hit 'p' to cycle through several different levels of
    higher contrast. This is useful in the same way that squinting at
    a subject so you just get a sense of the big blocks of shapes. Try
    it in grayscale mode.
  * gridlines: hit 'l' to cycle through different numbers of gridlines
    drawn on the image. Having a few lines up can be helpful for
    tricky subjects.

You can also hit 's' to skip the current image and move on to the next
one. 

Installation requirements:

  * pygame      (ubuntu: sudo aptitude install python-pygame)
  * feedparser  (ubuntu: sudo aptitude install python-feedparser)

Current Issues (patches welcome):

  * only handles Atom feeds of a pretty narrow flavor, with fullsize
    images as enclosures on the entries. In particular, I don't yet
    have it working with Flickr's RSS feeds (you currently have to
    manually make sure there's a 'format=atom' in the url).
  * it's not very smart about image sizes on feeds. Eg, if you're
    running it on a 1024x768 display, it will still try to pull down
    the full-size images from a flickr feed and rescale them (which
    can be slow) itself, rather than notice that flickr makes
    available images that are already closer in size to how it will
    want to display.
  * when pulling images from feeds, it should probably do something
    intelligent about pre-fetching. Currently, it doesn't download the
    image until it's time to display it, so you have to wait for it to
    download and scale to the appropriate size. It would be better if
    it did that in the background while the previous image is
    displaying so it could just quickly swap over without a delay.
  * doesn't handle multiple monitors very well. It tries to fullscreen
    across all of them, but should probably limit itself to one
    monitor.
  * I guess a non-fullscreen mode might be useful to some people. 
  * I wish I knew how to disable screensavers and monitor power-saving
    mode while it's on.
  * Also, it really needs a better name than 'sketch.py'. Please.
