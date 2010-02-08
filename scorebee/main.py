
import logging
import sys

from .application import Application
from .document import Document, Track, Event

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    app = Application(sys.argv)
    
    # Load a document.
    # We absolutely MUST have the document constructed fully BEFORE
    # setting it here. There are side effects to setting it.
    # HACK: This is just a hack for now.
    doc = Document('/Users/mikeboers/Desktop/example.MOV')
    # self.doc = Document('/Users/mikeboers/Desktop/C00000S00A20091231112932302.avi')
    doc.add_track(Track(
        name='A behaviour',
        key='q',
        group='top two',
        events=[
            Event(10, 15), Event(50, 65), Event(500, 600)
        ]
    ))
    doc.add_track(Track(
        name='Nothin here',
        key='w',
        group='top two',
        events=[]
    ))
    doc.add_track(Track(
        name='Better one',
        key='e',
        events=[
            Event(25, 26), Event(70, 71), Event(700, 701)
        ]
    ))
    
    app.doc = doc
    
    app.run()