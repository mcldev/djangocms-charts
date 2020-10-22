

def transpose(the_array):
    ret = map(list, zip(*the_array))
    ret = list(ret)
    return ret


def get_unique_list(dict_list, key="id"):
    # https://stackoverflow.com/questions/10024646/how-to-get-list-of-objects-with-unique-attribute
    seen = set()
    return [seen.add(d[key]) or d for d in dict_list if d and d[key] not in seen]


def color_variants(hex_colors, brightness_offset=1):
    return [color_variant(c, brightness_offset) for c in hex_colors]

def color_variant(hex_color, brightness_offset=1):
    """ takes a color like #87c95f and produces a lighter or darker variant """
    # https://chase-seibert.github.io/blog/2011/07/29/python-calculate-lighterdarker-rgb-colors.html
    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
    # hex() produces "0x88", we want just "88"
    return "#" + "".join([hex(i)[2:] for i in new_rgb_int])
