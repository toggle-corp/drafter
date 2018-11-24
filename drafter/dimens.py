px_per_inches = 72  # DPI
mm_per_inches = 25.4
units_multiplier = 1


def set_dpi(new_value):
    global px_per_inches
    px_per_inches = new_value


def set_multiplier(new_value):
    global units_multiplier
    units_multiplier = new_value


def inches(val):
    return val * px_per_inches * units_multiplier


def mm(val):
    return val / mm_per_inches * px_per_inches * units_multiplier


def px(val):
    return val * units_multiplier
