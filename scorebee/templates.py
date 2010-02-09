
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
        
        dict(name='defensive wing threat',   key='r', group=None),
        dict(name='run away / being chased', key='e', group=None),
        dict(name='fly away',                key='w', group=None),
        
        dict(name='non-aggressive present',  key='f', group=None),
        dict(name='non-aggressive absent',   key='d', group=None),
        dict(name='non-aggressive arrive',   key='s', group=None),
        dict(name='non-aggressive leave',    key='a', group=None),

    ]

}