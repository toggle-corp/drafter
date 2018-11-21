from drafter.draft import Draft
from drafter.utils import Rect
from drafter.layouts import Row, Column


root = Column(
    bg_color=[1, 0, 0, 1],
).add(
    Row(
        bg_color=[0, 1, 0, 1],
        w=50,
        h=50,
        margin=Rect(16),
    ),
    Row(
        bg_color=[0, 0, 1, 1],
        w=100,
        h=100,
        justify='start',
        align='end',
        relative=True,
    ).add(
        Row(
            bg_color=[1, 0, 1, 1],
            wr=0.25,
            h=50,
            margin=Rect(8),
        ),
        Row(
            bg_color=[1, 1, 1, 0.75],
            wr=0.25,
            h=20,
            margin=Rect(8),
        ),
        Row(
            bg_color=[0, 1, 1, 0.3],
            absolute=True,
            right=8,
            top=-10,
            w=20,
            h=20,
        ),
    ),
)

Draft(root).save('test.png')
