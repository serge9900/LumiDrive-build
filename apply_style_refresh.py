"""Visual-only skin on top of 0.7.12; fail if any behavior/layout file changes."""
from pathlib import Path
import hashlib
import json
import sys
import xml.etree.ElementTree as ET

A = '{http://schemas.android.com/apk/res/android}'
APP = 'fermata/src/main/res/'
UTIL = 'depends/utils/src/main/res/'


def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts}


def apply(root):
    before = snapshot(root)
    changed = set()

    def write(path, content):
        ET.fromstring(content)
        (root / path).write_text(content + '\n', encoding='utf-8')
        changed.add(path)

    palette = {
        'android:colorBackground': '#100E18', 'colorPrimaryDark': '#0D0B13',
        'colorPrimary': '#181420', 'colorOnPrimary': '#E8DFF8',
        'android:textColorPrimary': '#FAF7FF', 'colorSecondary': '#211B2D',
        'colorOnSecondary': '#C8B5F0', 'android:textColorSecondary': '#D9D0E6',
        'boxStrokeColor': '#393047', 'alpha': '1',
        'colorSecondaryVariant': '#51406C', 'android:textColorTertiary': '#FFFFFF',
        'colorSurface': '#292136', 'colorOnSurface': '#FAF7FF',
        'colorPrimarySurface': '#292136', 'colorOnPrimarySurface': '#FAF7FF',
        'colorAccent': '#D6B5FF', 'rippleColor': '#40C8B5F0',
        'android:textColorHint': '#B5A8C5', 'colorControlNormal': '#C8B5F0',
        'colorControlActivated': '#E0C8FF',
    }
    for name in ('Dark', 'Purple'):
        values = ''.join(f'<item name="{key}">{value}</item>' for key, value in palette.items())
        write(APP + f'values/theme_{name.lower()}.xml',
              f'<resources><style name="AppTheme.{name}">{values}</style></resources>')

    theme = APP + 'values/theme.xml'
    original = (root / theme).read_text(encoding='utf-8')
    expected = '<item name="cornerRadius">20dp</item>'
    if original.count(expected) != 1:
        raise RuntimeError('Unexpected baseline corner radius')
    write(theme, original.replace(expected, '<item name="cornerRadius">12dp</item>'))

    write(APP + 'drawable/lumidrive_home_background.xml',
          f'<shape xmlns:android="http://schemas.android.com/apk/res/android">'
          '<gradient android:angle="270" android:startColor="#171221" '
          'android:centerColor="#100E18" android:endColor="#100E18" /></shape>')

    def shape(fill, border, radius):
        return (f'<shape><solid android:color="{fill}"/>'
                f'<stroke android:width="1dp" android:color="{border}"/>'
                f'<corners android:radius="{radius}dp"/></shape>')

    # Preserve the baseline selector states/order; only replace their appearance.
    for path in (UTIL + 'drawable/lumidrive_nav_button.xml',
                 UTIL + 'drawable/lumidrive_toolbar_button.xml',
                 APP + 'drawable/lumidrive_control_button.xml'):
        tree = ET.fromstring((root / path).read_text(encoding='utf-8'))
        for item in tree:
            states = item.attrib
            if states.get(A + 'state_pressed') == 'true':
                fill, border = '#624A82', '#E0C8FF'
            elif states.get(A + 'state_focused') == 'true':
                fill, border = '#49365F', '#EAD9FF'
            elif states.get(A + 'state_selected') == 'true':
                fill, border = '#49365F', '#C8A3F4'
            else:
                fill, border = '#211B2D', '#30273E'
            for child in list(item):
                item.remove(child)
            item.append(ET.fromstring('<wrapper xmlns:android="http://schemas.android.com/apk/res/android">'
                                     + shape(fill, border, 12) + '</wrapper>')[0])
        ET.register_namespace('android', A[1:-1])
        write(path, ET.tostring(tree, encoding='unicode'))

    write(APP + 'values/lumidrive_styles.xml', '''<resources>
    <style name="LumiDrive.FloatingButtonStyle" parent="Theme.Utils.Base.FloatingButtonStyle">
        <item name="backgroundTint">#49365F</item>
        <item name="tint">#FAF7FF</item>
        <item name="borderColor">#8E72B2</item>
        <item name="borderFocusColor">#EAD9FF</item>
        <item name="rippleColor">#C8B5F0</item>
    </style></resources>''')

    # No changes to layouts, IDs, text sizes, padding, menu timers or Java/Kotlin.
    after = snapshot(root)
    actual = {p for p in before.keys() | after.keys() if before.get(p) != after.get(p)}
    if not actual <= changed:
        raise RuntimeError('Non-visual files modified: ' + str(actual - changed))
    report = {
        'baseline': '0.7.12', 'changed_resources': sorted(actual),
        'unchanged_files': len(before) - len(actual),
        'behavior_and_layout_files_unchanged': True,
        'device_validation_required': ['rotary focus', 'up/down menus and auto-hide',
                                       'playback', 'IPTV add source', 'phone and Android Auto'],
    }
    (root / 'LUMIDRIVE_STYLE_AUDIT.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    version = root / 'gradle/libs.versions.toml'
    value = version.read_text(encoding='utf-8')
    if 'appVersionName = "0.7.12"' not in value or 'appVersionCode = "295"' not in value:
        raise RuntimeError('Expected 0.7.12 / 295 baseline')
    version.write_text(value.replace('appVersionName = "0.7.12"', 'appVersionName = "0.8.0-preview1"')
                      .replace('appVersionCode = "295"', 'appVersionCode = "296"'), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    apply(Path(sys.argv[1]).resolve())

