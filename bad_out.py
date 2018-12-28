from drafter.draft import ImageDraft, PdfDraft
from drafter.nodes import Text
from drafter.layouts import Column
from drafter.color import rgb

def sample():
    return Column(
        width=150,
        height=150,
        bg_color=rgb(255, 255, 255)
    ).add(
        Text(text='जिमाली',
             width = '100%',
             height = '100%')
    )

PdfDraft('./text.pdf').draw(sample())