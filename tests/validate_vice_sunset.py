"""Check generated resources, preference migration, UI scope and contrast."""
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1])
app = root / 'fermata/src/main'
util = root / 'depends/utils/src/main'
styles = ET.parse(app / 'res/values/theme_vice_sunset.xml').getroot()
styles = {s.get('name'): {i.get('name'): i.text for i in s} for s in styles}
phone = styles['AppTheme.ViceSunset']
car = phone | styles['AppTheme.ViceSunset.Auto']


def luminance(color):
    rgb = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    rgb = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
    return sum(v * w for v, w in zip(rgb, (.2126, .7152, .0722)))


def contrast(fg, bg):
    high, low = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (high + .05) / (low + .05)


for name, colors in [('phone', phone), ('auto', car)]:
    # Include selected rows and navigation, not just the main background.
    foregrounds = ['android:textColorPrimary', 'android:textColorSecondary',
                   'colorOnSecondary', 'colorOnPrimary', 'colorAccent']
    backgrounds = ['android:colorBackground', 'colorSurface', 'colorSecondaryVariant',
                   'lumiNavStart', 'lumiNavEnd']
    ratios = [contrast(colors[f], colors[b]) for f in foregrounds for b in backgrounds]
    assert min(ratios) >= 4.5, (name, min(ratios))
    print(f'{name}: minimum text/accent contrast {min(ratios):.2f}:1')
assert contrast('#140F24', '#FF5DA6') >= 4.5  # FAB and phone logo
assert contrast('#140F24', '#FFAA7D') >= 4.5
assert set(['#140F24', '#302341', '#FF5DA6', '#45E5DD', '#BD97FF', '#F8EEFF', '#B7A6D0']) <= set(phone.values())

prefs = (app / 'java/me/aap/fermata/ui/activity/MainActivityPrefs.java').read_text(encoding='utf-8')
constants = dict((name, int(value)) for name, value in re.findall(r'int (THEME_\w+) = (\d+);', prefs))
assert constants['THEME_VICE_SUNSET'] == 7
condition = re.search(r'if \((value != THEME_DARK.*?)\) \{', prefs).group(1)
accepted = {constants[key] for key in re.findall(r'value != (THEME_\w+)', condition)}
assert accepted == {0, 1, 7}
for stored in [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 999]:
    migrated = stored if stored in accepted else 0
    assert migrated == ({0: 0, 1: 1, 7: 7}.get(stored, 0))
assert 'Pref<IntSupplier> key = (AUTO && auto) ? THEME_AA : THEME_MAIN;' in prefs
settings = (app / 'java/me/aap/fermata/ui/fragment/SettingsFragment.java').read_text(encoding='utf-8')
assert 'new int[]{MainActivityPrefs.THEME_DARK, MainActivityPrefs.THEME_LIGHT, MainActivityPrefs.THEME_VICE_SUNSET}' in settings
delegate = (app / 'java/me/aap/fermata/ui/activity/MainActivityDelegate.java').read_text(encoding='utf-8')
assert '? R.style.AppTheme_ViceSunset_Auto : R.style.AppTheme_ViceSunset' in delegate

toolbar = (util / 'java/me/aap/utils/ui/view/ToolBarView.java').read_text(encoding='utf-8')
title = toolbar[toolbar.index('default TextView createTitleText'):toolbar.index('default boolean backOnTitleClick')]
for token in ['setLayoutParams(t, 0, WRAP_CONTENT)', 'setMarginStart(toIntPx(ctx, 8))',
              'setMarginEnd(toIntPx(ctx, 8))', 'setEllipsize(TextUtils.TruncateAt.END)']:
    assert token in title

audit = json.loads((root / 'LUMIDRIVE_VICE_AUDIT.json').read_text())
allowed_java = {'LumiThemeColors.java', 'ToolBarView.java', 'MainActivityPrefs.java',
                'MainActivityDelegate.java', 'SettingsFragment.java',
                'LumiDriveDashboard.java', 'LumiDriveAutoHome.java', 'MediaItemView.java',
                'NavBarView.java', 'NavButtonView.java'}
for path in audit['changed_presentation_files']:
    assert '/res/' in path or Path(path).name in allowed_java, path
    assert not path.endswith(('theme_dark.xml', 'theme_light.xml')), path
assert not any('mirror' in p.lower() or '/media/' in p for p in audit['changed_presentation_files'])
print('Preference migration, independent car theme, title margins and presentation-only scope passed')

assert contrast('#F8EEFF', '#773E70') >= 4.5
assert contrast('#B7A6D0', '#302341') >= 4.5
banner = ET.parse(app / 'res/drawable/lumi_vice_banner.xml').getroot()
assert banner.tag == 'vector'
dashboard = (app / 'java/me/aap/fermata/ui/activity/LumiDriveDashboard.java').read_text(encoding='utf-8')
assert 'if (vice) {\n            ImageView sunset' in dashboard
assert 'VICE SUNSET' in dashboard and 'Night drive • Neon sunset' in dashboard
auto = (app / 'java/me/aap/fermata/ui/activity/LumiDriveAutoHome.java').read_text(encoding='utf-8')
assert 'lumi_vice_banner' not in auto
print('Reference banner, theme-gated layout and selected navigation contrast passed')
