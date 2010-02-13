
from .document import Document, Track


templates = {

    'Development': [
        dict(name='Qwer', key='q', group='one'),
        dict(name='Wert', key='w', group='two'),
        dict(name='Erty', key='e', group='three'),
        dict(name='Asdf', key='a', group='one'),
        dict(name='Sdfg', key='s', group='two'),
        dict(name='Dfgh', key='d', group='three'),
    ],
    
    'Re-Organized Flies': [
    #this is a new version of general flies that has been edited so that similar
    # behaviours are now together. Walk Away (from Chen et al.) has been removed 
    #and Chase has been redefined to include being persued quickly or slowly. If 
    #necessary I will modify it to be 'fast chase' and 'slow chase' to be more 
    #descriptive of the actual behaviour being scored. Behaviours being done TO
    #the focal individual have been added.
    
        dict(name='approach',                key='u', group=None),
        dict(name='wing threat',             key='o', group=None),
        dict(name='defensive wing threat',   key='r', group=None),
        dict(name='wings erect',             key='p', group=None),
        dict(name='low-level fencing',       key='i', group=None),
        dict(name='high-level fencing',      key='h', group=None),
        dict(name='boxing',                  key='b', group=None),
        dict(name='tussling',                key='n', group=None),
        dict(name='lunging',                 key='k', group=None),
        dict(name='lunged at',               key='f', group=None),
        dict(name='holding',                 key='l', group=None),
        dict(name='held',                    key='d', group=None),
        dict(name='chasing',                 key='j', group=None),
        dict(name='being chased',            key='e', group=None),
        dict(name='turn away',               key='g', group=None),
        dict(name='retreat',                 key='q', group=None),
        dict(name='fly away',                key='w', group=None),
        
        dict(name='arrive (in camera view)', key='s', group=None),
        dict(name='leave (camera view)',     key='a', group=None),
        
    ],
    
    'General Flies': [
        dict(name='approach',                key='u', group=None),
        dict(name='low-level fencing',       key='i', group=None),
        dict(name='wing threat',             key='o', group=None),
        dict(name='high-level fencing',      key='h', group=None),
        dict(name='chasing',                 key='j', group=None),
        dict(name='lunging',                 key='k', group=None),
        dict(name='holding',                 key='l', group=None),
        dict(name='boxing',                  key='b', group=None),
        dict(name='tussling',                key='n', group=None),
        dict(name='walk away',               key='m', group=None),
        dict(name='wings erect',             key='p', group=None),

        dict(name='defensive wing threat',   key='r', group=None),
        dict(name='run away / being chased', key='e', group=None),
        dict(name='fly away',                key='w', group=None),
        dict(name='turn away',               key='g', group=None),
        
        #dict(name='non-aggressive present',  key='f', group=None), these haven't proven useful ~Tanya
        #dict(name='non-aggressive absent',   key='d', group=None), these haven't proven useful ~Tanya
        
        dict(name='non-aggressive arrive',   key='s', group=None),
        dict(name='non-aggressive leave',    key='a', group=None),

    ]

}