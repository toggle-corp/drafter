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


def hx(hexstr):
    h = hexstr.lstrip('#')
    rgb_t = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return rgb(*rgb_t)


def alpha(color, alpha):
    return [color[0], color[1], color[2], alpha]
