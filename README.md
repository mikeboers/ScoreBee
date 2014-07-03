ScoreBee
========

*ScoreBee* is a GUI tool to assist biologists in behavioral scoring.


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
fc-cache -v

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
