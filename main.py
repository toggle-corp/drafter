from drafter.draft import ImageDraft, PdfDraft
from drafter.utils import Rect, Border
from drafter.nodes import Text, Canvas
from drafter.shapes import (
    Arc, Pie,
    SolidArrow, OpenArrow,
    String,
)
from drafter.layouts import Row, Column

import math


class MyPie:
    def render(self, ctx):
        pie = Pie(
            center=[50, 50],
            radius=40,
            color=[0.66, 0.46, 0.23, 1],
            line_width=0,
            angle1=0,
            angle2=math.pi*3/4,
        )
        pie.render(ctx)

        text = String(
            text='Pie',
            x=20,
            y=20,
        )
        text.render(ctx)
        tc = text.calc_center(ctx)

        OpenArrow(
            p1=[tc[0] + 5, tc[1] + 5],
            p2=pie.calc_center(),
        ).render(ctx)


class MyDonut:
    def render(self, ctx):
        Arc(
            center=[50, 50],
            radius=40,
            line_color=[0.56, 0.56, 0.23, 1],
            line_width=12,
            angle1=0,
            angle2=math.pi/4,
        ).render(ctx)
        arc1 = Arc(
            center=[50, 50],
            radius=40,
            line_color=[0.25, 0.25, 0.54, 1],
            line_width=12,
            line_dash=[2],
            angle1=math.pi/4 - math.pi / 180,
            angle2=math.pi,
        )
        arc1.render(ctx)
        arc2 = Arc(
            center=[50, 50],
            radius=40,
            line_color=[0.25, 0.54, 0.56, 1],
            line_width=12,
            angle1=math.pi,
            angle2=0,
        )
        arc2.render(ctx)
        SolidArrow(
            p1=[10, 10],
            p2=arc1.calc_center(),
        ).render(ctx)
        SolidArrow(
            p1=[10, 10],
            p2=arc2.calc_center(),
        ).render(ctx)


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
    Row(
        bg_color=[1, 1, 1, 1],
        width=200,
        height=100,
        margin=Rect(4),
    ).add(
        Canvas(
            width='50%',
            height='50%',
            renderer=MyDonut(),
        ),
        Canvas(
            width='50%',
            height='50%',
            renderer=MyPie(),
        )
    ),
)

ImageDraft('test.png').draw(root)
PdfDraft('test.pdf').draw(root)
