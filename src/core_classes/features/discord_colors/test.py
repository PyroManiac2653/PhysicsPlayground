from colors_accessibility import AccessibilityProcessor, Color

rgb_color = Color('rgb', [120, 198, 73])
hex_color = Color('hex', '#783957')

processor = AccessibilityProcessor(rgb_color, hex_color)
wcag_compliant_colors = processor.get_all_wcag_compliant_color()
print(wcag_compliant_colors.get('lightness').get('background'))