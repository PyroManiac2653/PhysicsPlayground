from PIL import Image, ImageDraw, ImageFont
import json
from color_contrast import AccessibilityLevel, check_contrast
import math
from colour import Color

# Role color module

with open("base_colors.json", "r") as f:
    base_colors = json.load(f)
with open("role_colors.json", "r") as f:
    swatch_colors = json.load(f)
scale = 2
swatch_width, swatch_height, swatch_spacing = 50 * scale, 20 * scale, 10 * scale
num_swatches = len(swatch_colors)

base_width = 70 * scale
base_height = ((swatch_height + swatch_spacing) * num_swatches + swatch_spacing)
num_bases = len(base_colors)
header_height = 50 * scale
label_width = 2 * base_width * scale

default_font_size = 16 * scale
default_font = ImageFont.truetype("arial.ttf", default_font_size)

image_width = base_width * num_bases + math.ceil(label_width * 1.5)
image_height = base_height + header_height

color_matrix = None

def get_luminance(color: Color) -> float:
    """
    Calculate the relative luminance of the supplied color.

    Algorithm taken from https://www.w3.org/TR/WCAG21/#dfn-relative-luminance

    :param color: the color to get the luminance from
    :type color: Color
    :return: Luminance value
    :rtype: float
    """

    RsRGB, GsRGB, BsRGB = color.get_rgb()

    R = RsRGB / 12.92 if RsRGB <= 0.04045 else ((RsRGB + 0.055) / 1.055) ** 2.4
    G = GsRGB / 12.92 if GsRGB <= 0.04045 else ((GsRGB + 0.055) / 1.055) ** 2.4
    B = BsRGB / 12.92 if BsRGB <= 0.04045 else ((BsRGB + 0.055) / 1.055) ** 2.4

    luminance = 0.2126 * R + 0.7152 * G + 0.0722 * B

    return luminance

def get_contrast_ratio (foreground_color, background_color):
    fg = Color(foreground_color)
    bg = Color(background_color)

    l1 = get_luminance(fg)
    l2 = get_luminance(bg)

    ratio = (l1 + 0.05) / (l2 + 0.05) if l1 > l2 else (l2 + 0.05) / (l1 + 0.05)
    return ratio


def draw_base_and_swatches(image, colors, swatch_colors, width=base_width, height=base_height, x_offset=0, y_offset=0, accessibility_matrix = None):
    draw = ImageDraw.Draw(image)
    for i, color in enumerate(colors):
        left = i * width + x_offset
        right = left + width + x_offset
        top = y_offset
        bottom = y_offset + height
        y_swatch_start = y_offset + swatch_spacing
        draw.rectangle([left, top, right, bottom], fill=color)
        draw_swatches(image, swatch_colors, left, right, color, y_offset=y_swatch_start, accessibility_matrix=accessibility_matrix)

def draw_swatches(image, colors, x_left, x_right, base_color, width=swatch_width, height=swatch_height, space=swatch_spacing, y_offset=0, accessibility_matrix = None):
    draw = ImageDraw.Draw(image)
    center = (x_left + x_right) / 2
    left = center - width / 2
    right = center + width / 2
    for i, color in enumerate(colors):
        # color swatch
        top = y_offset + i * (height + swatch_spacing)
        bottom = y_offset + i * (height + swatch_spacing) + height
        draw.rectangle([left, top, right, bottom], fill=color["hex"])

        accessibility_label = None
        if accessibility_matrix != None and accessibility_matrix.get(color["hex"]) != None and accessibility_matrix.get(color["hex"]) != None:
            accessibility_label = accessibility_matrix[color["hex"]][base_color]["label"]
        else:
            accessibility_label = get_highest_AL_label(color["hex"], base_color)

        draw.text((left + 3
                    * scale, top), accessibility_label, font=default_font, fill=base_color)

def draw_base_labels(image, labels, width=base_width, height=header_height, x_offset=0, y_offset=0, font=default_font):
    draw = ImageDraw.Draw(image)
    for i, label in enumerate(labels):
        x = (i+.1) * width + x_offset
        y = y_offset + 0.1 * height
        draw.text((x, y), label, font=font, fill="white")

def draw_swatch_labels(image, labels, height=swatch_height+swatch_spacing, x_offset=0, y_offset=0, font=default_font, accessibility_matrix = None):
    draw = ImageDraw.Draw(image)
    for i, label in enumerate(labels):
        y = y_offset + (i+.1) * height
        draw.text((x_offset, y), label, font=font, fill="white")

def get_highest_AL (foreground, background):
    if check_contrast(foreground, background, level = AccessibilityLevel.AAA):
        return AccessibilityLevel.AAA
    elif check_contrast(foreground, background, level = AccessibilityLevel.AA):
        return AccessibilityLevel.AA
    elif check_contrast(foreground, background, level = AccessibilityLevel.AA18):
        return AccessibilityLevel.AA18
    else:
        return None

def get_AL_label (accessibility_level):
    if accessibility_level == AccessibilityLevel.AAA:
        return "AA"
    elif accessibility_level == AccessibilityLevel.AA:
        return "AAA"
    elif accessibility_level == AccessibilityLevel.AA18:
        return "AA18"
    else:
        return "X"

def get_AL_rank (accessibility_level):
    if accessibility_level == AccessibilityLevel.AAA:
        return 3
    elif accessibility_level == AccessibilityLevel.AA:
        return 2
    elif accessibility_level == AccessibilityLevel.AA18:
        return 1
    else:
        return 0

def get_highest_AL_label (foreground, background):
    highest_AL = get_highest_AL(foreground, background)
    return get_AL_label(highest_AL)

def get_highest_AL_matrix (foreground_colors, background_colors):
    matrix = {}
    for fg in foreground_colors:
        matrix[fg] = { "best": { "level": None, "label": None, "ratio": None, "ratio_label": None },
                       "worst": { "level": None, "label": None, "ratio": None, "ratio_label": None } }            

        bFirst = True
        for bg in background_colors:
            matrix[fg][bg] = {}
            matrix[fg][bg]["level"] = get_highest_AL(fg, bg)
            matrix[fg][bg]["label"] = get_AL_label(matrix[fg][bg]["level"])
            ratio = get_contrast_ratio(fg, bg)
            matrix[fg][bg]["ratio"] = ratio
            matrix[fg][bg]["ratio_label"] = "{:.1f}".format(ratio) + ":1"
            if bFirst:
                matrix[fg]["best"]["level"] = matrix[fg]["worst"]["level"] = matrix[fg][bg]["level"]
                matrix[fg]["best"]["label"] = matrix[fg]["worst"]["label"] = matrix[fg][bg]["label"]
                matrix[fg]["best"]["ratio"] = matrix[fg]["worst"]["ratio"] = matrix[fg][bg]["ratio"]
                matrix[fg]["best"]["ratio_label"] = matrix[fg]["worst"]["ratio_label"] = matrix[fg][bg]["ratio_label"]
            else:
                if get_AL_rank(matrix[fg][bg]["level"]) > get_AL_rank(matrix[fg]["best"]["level"]):
                    matrix[fg]["best"]["level"] = matrix[fg][bg]["level"]
                    matrix[fg]["best"]["label"] = matrix[fg][bg]["label"]
                elif get_AL_rank(matrix[fg][bg]["level"]) < get_AL_rank(matrix[fg]["worst"]["level"]):
                    matrix[fg]["worst"]["level"] = matrix[fg][bg]["level"]
                    matrix[fg]["worst"]["label"] = matrix[fg][bg]["label"]

                if matrix[fg][bg]["ratio"] > matrix[fg]["best"]["ratio"]:
                    matrix[fg]["best"]["ratio"] = matrix[fg][bg]["ratio"]
                    matrix[fg]["best"]["label"] = matrix[fg][bg]["label"]
                elif matrix[fg][bg]["ratio"] < matrix[fg]["worst"]["ratio"]:
                    matrix[fg]["worst"]["ratio"] = matrix[fg][bg]["ratio"]
                    matrix[fg]["worst"]["ratio_label"] = matrix[fg][bg]["ratio_label"]

            bFirst = False

    return matrix

image = Image.new("RGB", (image_width, image_height), "black")

color_matrix = get_highest_AL_matrix([color["hex"] for color in swatch_colors], [color["hex"] for color in base_colors])

base_color_font_size = 14 * scale
base_color_font = ImageFont.truetype("arial.ttf", base_color_font_size)

draw_base_labels(image, [color["hex"] for color in base_colors], font=base_color_font)
draw_base_labels(image, [color["name"] for color in base_colors], y_offset=header_height/2)
draw_base_and_swatches(image, [color["hex"] for color in base_colors], swatch_colors, y_offset=header_height, accessibility_matrix = color_matrix)

def get_swatch_label(color):
    c = color["hex"]
    str_ALs = "  (" + color_matrix[c]["worst"]["label"]
    if (color_matrix[c]["best"]["level"] != color_matrix[c]["worst"]["level"]):
        str_ALs += "-" + color_matrix[c]["best"]["label"]
    str_ALs += ")"
    str_ALs = "  (" + color_matrix[c]["worst"]["ratio_label"]
    if (color_matrix[c]["best"]["ratio"] != color_matrix[c]["worst"]["ratio"]):
        str_ALs += "-" + color_matrix[c]["best"]["ratio_label"]
    str_ALs += ")"
    return color["name"] + str_ALs
draw_swatch_labels(image, [get_swatch_label(color) for color in swatch_colors], x_offset=base_width * num_bases + swatch_spacing, y_offset=header_height + swatch_spacing)
draw_swatch_labels(image, [("(" + color["hex"] + ")") for color in swatch_colors], x_offset=base_width * num_bases + swatch_spacing + label_width, y_offset=header_height + swatch_spacing)


image.save("discord_colors.png")

print("Image saved as 'discord_colors.png'")
