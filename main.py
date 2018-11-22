from drafter.draft import ImageDraft, PdfDraft
from drafter.utils import Rect
from drafter.layouts import Row, Column


root = Column(
    bg_color=[1, 0, 0, 1],
    justify='center',
    align='center',
).add(
    Row(
        bg_color=[0, 1, 0, 1],
        width=50,
        height=50,
        margin=Rect([8, 8, 0, 8]),
    ),
    Row(
        bg_color=[0, 0, 1, 1],
        width=100,
        height=100,
        margin=Rect(8),
        justify='start',
        align='end',
        relative=True,
    ).add(
        Row(
            bg_color=[1, 0, 1, 1],
            width='25%',
            height=50,
            margin=Rect(8),
        ),
        Row(
            bg_color=[1, 1, 1, 0.75],
            width='25%',
            height=20,
            margin=Rect(8),
        ),
        Row(
            bg_color=[0, 1, 1, 0.3],
            absolute=True,
            right=8,
            top=-10,
            width=20,
            height=20,
        ),
    ),
)

ImageDraft('test.png').draw(root)
PdfDraft('test.pdf').draw(root)
