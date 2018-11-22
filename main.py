from drafter.draft import ImageDraft, PdfDraft
from drafter.utils import Rect, Border
from drafter.nodes import Text
from drafter.layouts import Row, Column


root = Column(
    bg_color=[1, 0, 0, 1],
    justify='center',
    align='center',
    border=Border(
        32,
        4,
        [0, 0, 0, 1],
    ),
).add(
    Row(
        bg_color=[0, 1, 0, 1],
        width=50,
        height=50,
        margin=Rect([8, 8, 0, 8]),
        relative=True,
    ).add(
        Text(
            markup="Hello <b>world</b>",
            wrap=True,
            font='Ubuntu italic 10',
            wrap_mode=Text.CHAR_WRAP,
            absolute=True,
            padding=Rect(4),
            top=-10,
            left=8,
            bg_color=[1, 1, 1, 1],
        )
    ),
    Row(
        bg_color=[0, 0, 1, 1],
        width=100,
        height=100,
        margin=Rect(8),
        justify='start',
        align='end',
        relative=True,
        border=Border(
            32,
            4,
            [1, 1, 1, 1],
        ),
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
