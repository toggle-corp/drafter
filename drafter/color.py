import colorsys


def rgb(r, g, b):
    return [
        r / 255,
        g / 255,
        b / 255,
        1,
    ]


def rgba(r, g, b, a):
    return [
        r / 255,
        g / 255,
        b / 255,
        a,
    ]


def hsl(h, s, l):
    return rgb(*colorsys.hls_to_rgb(h, l, s))


def hsla(h, s, l, a):
    return rgba(*colorsys.hls_to_rgb(h, l, s), a)
