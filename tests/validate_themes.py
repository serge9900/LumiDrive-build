"""Validate real generated theme resources, mappings and readable state combinations."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1])
res = root / 'fermata/src/main/res'

def luminance(color):
    assert len(color) == 7 and color.startswith('#'), color
    v = [int(color[i:i+2], 16) / 255 for i in (1,3,5)]
    v = [x/12.92 if x <= .04045 else ((x+.055)/1.055)**2.4 for x in v]
    return sum(x*w for x,w in zip(v, (.2126,.7152,.0722)))

for theme in ('light', 'dark'):
    doc = ET.parse(res / f'values/theme_{theme}.xml')
    colors = {x.get('name'): x.text for x in doc.findall('.//item')}
    assert colors['android:isLightTheme'] == str(theme == 'light').lower()
    pairs = [('android:textColorPrimary', 'android:colorBackground'),
             ('android:textColorSecondary', 'colorSecondary'),
             ('android:textColorTertiary', 'colorSecondaryVariant'),
             ('colorOnSurface', 'colorSurface'), ('colorOnPrimary', 'colorPrimary'),
             ('colorOnSecondary', 'colorSecondaryVariant')]
    for fg,bg in pairs:
        hi,lo = sorted((luminance(colors[fg]), luminance(colors[bg])), reverse=True)
        ratio = (hi+.05)/(lo+.05)
        assert ratio >= 4.5, (theme,fg,bg,ratio)
        print(f'{theme}: {fg} on {bg}: {ratio:.2f}:1')

settings = (root / 'fermata/src/main/java/me/aap/fermata/ui/fragment/SettingsFragment.java').read_text()
assert 'o.values = new int[]{R.string.theme_system, R.string.theme_light, R.string.theme_dark};' in settings
assert 'o.valuesMap = new int[]{MainActivityPrefs.THEME_SYSTEM,' in settings
assert 'R.string.theme_star_wars' not in settings
assert 'R.string.theme_purple' not in settings

ns = '{http://schemas.android.com/apk/res/android}'
for name in ('media_item','media_item_border'):
    for item in ET.parse(res / f'color/{name}.xml').getroot():
        assert item.get(ns+'color').startswith('?attr/'), item.attrib
for mode in ('grid','list'):
    doc = ET.parse(res / f'layout/media_item_{mode}_layout.xml')
    actions = next(x for x in doc.getroot() if x.get(ns+'id') == '@+id/lumi_item_actions')
    assert actions.get(ns+'tint') == '?attr/colorOnSecondary'
print('Three-theme menu, shared state colors, action icon tint and contrast checks passed')

