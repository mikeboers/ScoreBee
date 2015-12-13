ScoreBee
========

*ScoreBee* is a GUI tool for scoring videos. It was designed to score behaviour for a biology research project.

ScoreBee is quite functional, but is not considered a polished product, and so comes with a number of caveats:

- It uses an external video player that it must continuously syncronize with. All data collection performs such a sync, and so the data is correct, but the interface is occasionally disconcerting as time seems to "jump" around slightly.

- Time is represented as a count of frames. This might be a problem with your research if you have a variable speed video source, and your frames are not the same length.

- There is no GUI for editing the tracks you are scoring, not the templates; one must edit the [template defitions](https://github.com/mikeboers/ScoreBee/blob/master/scorebee/templates.py).

There are plans to replace the external video player with an embedded one, to add missing critical features, and to stomp a few bugs, but there is no timeline in place.


Installation
------------

ScoreBee's requirements are:

- [Qt4][qt]
- [PyQt4][pyqt]
- [Mplayer][mplayer]

On OS X (with [HomeBrew][brew]), installation is roughly:

~~~

# Install QT4, PyQt4 and sip
brew install pyqt

# Install mplayer, and (re)build the font cache.
brew install mplayer

# Make sure mplayer works.
# Note: the first time MPlayer OSX plays a video, fontconfig will build it's
# font cache. This can take a while but only has to be done once.
mplayer /path/to/some/video.mov

# Grab ScoreBee itself (if you are reading this on GitHub).
git clone git@github.com:mikeboers/ScoreBee
cd ScoreBee

~~~

To run ScoreBee (on OS X):

~~~

# Pull PyQt4 and sip into the shell's environment
export PYTHONPATH="/usr/local/opt/pyqt/lib/python2.7/site-packages:/usr/local/opt/sip/lib/python2.7/site-packages"
export PATH="$PATH:/usr/local/opt/pyqt/bin"

# Run ScoreBee.
make run

~~~


[qt]: http://qt-project.org/
[pyqt]: http://www.riverbankcomputing.co.uk/software/pyqt/intro
[mplayer]: http://www.mplayerhq.hu/design7/news.html
[brew]: http://brew.sh/
