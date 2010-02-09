
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
        dict(name='approach',                key='p', group=None),
        dict(name='low-level fencing',       key='w', group=None),
        dict(name='wing threat',             key='e', group=None),
        dict(name='high-level fencing',      key='a', group=None),
        dict(name='chasing',                 key='s', group=None),
        dict(name='lunging',                 key='d', group=None),
        dict(name='holding',                 key='a', group=None),
        dict(name='boxing',                  key='s', group=None),
        dict(name='tussling',                key='d', group=None),
        dict(name='walk away',               key='a', group=None),
        dict(name='defensive wing threat',   key='s', group=None),
        dict(name='run away / being chased', key='d', group=None),
        dict(name='fly away',                key='d', group=None),
    ]

}