from drafter.draft import PdfDraft
from drafter.nodes import NP_Text
from drafter.layouts import Column
from drafter.utils import Rect

PdfDraft('./test.pdf').draw(
    Column(width = 1000,
           height = 1000).add(
        NP_Text(
            text = 'जिमाली',
            font='Roboto Light 8',
            padding=Rect(10)
        )
    )
)
