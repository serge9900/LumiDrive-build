"""Add opt-in Vice Sunset after the unchanged 0.8.0 theme pipeline."""
from pathlib import Path
import hashlib
import json
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1]).resolve()
app = 'fermata/src/main/'
util = 'depends/utils/src/main/'
helper = 'me.aap.utils.ui.LumiThemeColors'


def snapshot():
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts}


before = snapshot()
allowed = set()


def write(path, content):
    if path.endswith('.xml'):
        ET.fromstring(content)
    (root / path).write_text(content.rstrip() + '\n', encoding='utf-8')
    allowed.add(path)


def replace(path, old, new):
    content = (root / path).read_text(encoding='utf-8')
    if content.count(old) != 1:
        raise RuntimeError(f'Expected one anchor in {path}: {old[:80]}')
    write(path, content.replace(old, new))


# 2..6 are legacy upstream themes. Never reinterpret an existing preference as Vice.
prefs = app + 'java/me/aap/fermata/ui/activity/MainActivityPrefs.java'
replace(prefs, 'int THEME_CLASSIC = 6;', 'int THEME_CLASSIC = 6;\n\tint THEME_VICE_SUNSET = 7;')
replace(prefs, 'value < THEME_DARK || value > THEME_LIGHT',
        'value != THEME_DARK && value != THEME_LIGHT && value != THEME_VICE_SUNSET')
settings = app + 'java/me/aap/fermata/ui/fragment/SettingsFragment.java'
replace(settings, 'o.values = new int[]{R.string.lumi_theme_classic, R.string.theme_light};',
        'o.values = new int[]{R.string.lumi_theme_classic, R.string.theme_light, R.string.lumi_theme_vice_sunset};')
replace(settings, 'o.valuesMap = new int[]{MainActivityPrefs.THEME_DARK, MainActivityPrefs.THEME_LIGHT};',
        'o.valuesMap = new int[]{MainActivityPrefs.THEME_DARK, MainActivityPrefs.THEME_LIGHT, MainActivityPrefs.THEME_VICE_SUNSET};')
for directory in ('values', 'values-ru'):
    write(app + f'res/{directory}/lumi_vice_names.xml',
          '<resources><string name="lumi_theme_vice_sunset">Vice Sunset</string></resources>')
replace(app + 'java/me/aap/fermata/ui/activity/MainActivityDelegate.java',
        '''@StyleRes int theme = (Prefs.instance.getThemePref(auto) == MainActivityPrefs.THEME_LIGHT)
                ? R.style.AppTheme_Light : R.style.AppTheme_Dark;''',
        '''@StyleRes int theme = switch (Prefs.instance.getThemePref(auto)) {
            case MainActivityPrefs.THEME_LIGHT -> R.style.AppTheme_Light;
            case MainActivityPrefs.THEME_VICE_SUNSET -> auto
                    ? R.style.AppTheme_ViceSunset_Auto : R.style.AppTheme_ViceSunset;
            default -> R.style.AppTheme_Dark;
        };''')

write(util + 'res/values/lumi_vice_attrs.xml', '''<resources>
    <attr name="lumiViceSunset" format="boolean"/>
</resources>''')
palette = {
    'lumiViceSunset': 'true',
    'android:colorBackground': '#140F24', 'colorPrimaryDark': '#140F24',
    'colorPrimary': '#302341', 'colorOnPrimary': '#45E5DD',
    'colorSecondary': '#302341', 'colorOnSecondary': '#BD97FF',
    'android:textColorPrimary': '#F8EEFF', 'android:textColorSecondary': '#B7A6D0',
    'android:textColorTertiary': '#F8EEFF', 'android:textColorHint': '#B7A6D0',
    'colorSurface': '#302341', 'colorOnSurface': '#F8EEFF',
    'colorPrimarySurface': '#302341', 'colorOnPrimarySurface': '#F8EEFF',
    'colorSecondaryVariant': '#38283F', 'boxStrokeColor': '#BD97FF',
    'colorAccent': '#FF5DA6', 'colorControlNormal': '#BD97FF',
    'colorControlActivated': '#45E5DD', 'rippleColor': '#3345E5DD',
    'lumiNavStart': '#38283F', 'lumiNavEnd': '#38283F', 'alpha': '1',
    'android:isLightTheme': 'false', 'android:windowLightStatusBar': 'false',
    'android:windowLightNavigationBar': 'false',
    'floatingActionButtonStyle': '@style/LumiViceFloatingButton',
    'appStreamProgressStyle': '@style/LumiViceStreamProgress',
    'appSeekBarStyle': '@style/LumiViceSeekBar',
}
write(app + 'res/values/theme_vice_sunset.xml', '<resources>\n'
      '<style name="AppTheme.ViceSunset" parent="AppTheme">\n' +
      ''.join(f'    <item name="{k}">{v}</item>\n' for k, v in palette.items()) +
      '''</style>
<style name="AppTheme.ViceSunset.Auto" parent="AppTheme.ViceSunset">
    <item name="colorPrimary">#140F24</item>
    <item name="colorControlNormal">#B7A6D0</item>
</style>
<style name="LumiViceFloatingButton" parent="LumiDrive.FloatingButtonStyle">
    <item name="backgroundTint">#FF5DA6</item>
    <item name="tint">#140F24</item>
    <item name="borderColor">#FF5DA6</item>
    <item name="borderFocusColor">#45E5DD</item>
</style>
<style name="LumiViceStreamProgress" parent="AppTheme.StreamProgressStyle">
    <item name="indicatorColor">#FFAA7D</item>
</style>
<style name="LumiViceSeekBar" parent="AppTheme.SeekBarStyle">
    <item name="android:thumbTint">#45E5DD</item>
    <item name="android:progressTint">#FF5DA6</item>
    <item name="android:secondaryProgressTint">#BD97FF</item>
</style>
</resources>''')

# Extend existing drawing helpers; Classic and Light retain their exact old paths.
colors = util + 'java/me/aap/utils/ui/LumiThemeColors.java'
replace(colors, '    public static boolean light(Context c) {', '''    public static boolean vice(Context c) {
        TypedArray a = c.obtainStyledAttributes(new int[]{me.aap.utils.R.attr.lumiViceSunset});
        boolean value = a.getBoolean(0, false); a.recycle(); return value;
    }
    public static boolean light(Context c) {''')
replace(colors, '        return light(c) ? text(c) : original;', '''        if (vice(c)) {
            return switch (original) {
                case 0xFFBBAED2, 0xFFB7A8D0 -> 0xFFB7A6D0;
                case 0xFFAE8AFF, 0xFFBDA0FF -> 0xFFBD97FF;
                case 0xFFFF7AC8, 0xFFFF8DCD -> 0xFFFF5DA6;
                case 0xFF8FE7FF, 0xFF94E6FF -> 0xFF45E5DD;
                default -> text(c);
            };
        }
        return light(c) ? text(c) : original;''')
replace(colors, '        if (original == 0 || !light(c)) return original;', '''        if (original == 0) return original;
        if (vice(c)) {
            return switch (original) {
                case 0xFF10091E, 0xFF201135, 0xFF130B26, 0xFF1B112E -> 0xFF140F24;
                default -> 0xFF302341;
            };
        }
        if (!light(c)) return original;''')
replace(colors, '        return original == 0 ? 0 : (light(c) ? 0xff9676b3 : original);', '''        if (vice(c) && original != 0) {
            return (original == 0xFF8FE7FF || original == 0xFF94E6FF)
                    ? 0xFF45E5DD : 0xFFBD97FF;
        }
        return original == 0 ? 0 : (light(c) ? 0xff9676b3 : original);''')
for name in ('LumiDriveDashboard', 'LumiDriveAutoHome'):
    path = app + f'java/me/aap/fermata/ui/activity/{name}.java'
    first, last = ('first', 'last') if name.endswith('AutoHome') else ('start', 'end')
    # The phone logo gets a small sunset accent. The car logo is a flat dark tile.
    replace(path, 'logo.setTextColor(0xffffffff);',
            f'logo.setTextColor({helper}.vice(ctx) ? ' +
            ('0xFFF8EEFF' if name.endswith('AutoHome') else '0xFF140F24') + ' : 0xffffffff);')
    marker = f'        if ({first} != 0xFF7F4BC2 && {first} != 0xFF854BC7) {{'
    replace(path, marker, f'''        if ({helper}.vice(ctx) && ({first} == 0xFF7F4BC2 || {first} == 0xFF854BC7)) {{
            {first} = ''' + ('0xFF302341' if name.endswith('AutoHome') else '0xFFFF5DA6') + f''';
            {last} = ''' + ('0xFF302341' if name.endswith('AutoHome') else '0xFFFFAA7D') + f''';
        }} else if ({first} != 0xFF7F4BC2 && {first} != 0xFF854BC7) {{''')

# The title currently touches the back button in the supplied IPTV screenshot.
# Reserve logical margins inside its existing constrained slot, including filtering.
# No button listeners, visibility, focus order, or page-navigation behavior changes.
toolbar = util + 'java/me/aap/utils/ui/view/ToolBarView.java'
replace(toolbar, '''\t\t\t\tlp.horizontalWeight = 2;
\t\t\t\tlp.endToEnd = PARENT_ID;''', '''\t\t\t\tlp.horizontalWeight = 2;
                lp.setMarginStart(toIntPx(ctx, 8));
                lp.setMarginEnd(toIntPx(ctx, 8));
\t\t\t\tlp.endToEnd = PARENT_ID;''')

after = snapshot()
changed = {p for p in before.keys() | after.keys() if before.get(p) != after.get(p)}
assert changed <= allowed, changed - allowed
write('LUMIDRIVE_VICE_AUDIT.json', json.dumps({
    'baseline': 'v0.8.0', 'changed_presentation_files': sorted(changed),
    'unchanged_files': len(before) - len(changed),
    'classic_light_resources_unchanged': True,
    'device_validation_required': ['IPTV title at large font and toolbar scales',
                                   'theme switching on phone and Android Auto', 'rotary focus'],
}, indent=2))
print('Vice Sunset added; Classic/Light resources and non-presentation files preserved.')
