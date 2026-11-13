from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

root = Path(sys.argv[1]).resolve()
app = 'fermata/src/main/'
util = 'depends/utils/src/main/'

def write(p, s):
    if p.endswith('.xml'): ET.fromstring(s)
    (root / p).write_text(s + '\n', encoding='utf-8')

def replace(p, old, new):
    s = (root / p).read_text(encoding='utf-8')
    if s.count(old) != 1: raise RuntimeError(f'Unexpected anchor: {p}: {old[:70]}')
    write(p, s.replace(old, new))

prefs = app + 'java/me/aap/fermata/ui/activity/MainActivityPrefs.java'
replace(prefs, 'THEME_MAIN = Pref.i("THEME_MAIN", THEME_PURPLE)',
        'THEME_MAIN = Pref.i("THEME_MAIN", THEME_SYSTEM)')
replace(prefs, 'return (AUTO && auto) ? getIntPref(THEME_AA) : getIntPref(THEME_MAIN);', '''
        Pref<IntSupplier> key = (AUTO && auto) ? THEME_AA : THEME_MAIN;
        int value = getIntPref(key);
        if (value < THEME_DARK || value > THEME_SYSTEM) {
            value = THEME_DARK;
            applyIntPref(key, value);
        }
        return value;''')
settings = app + 'java/me/aap/fermata/ui/fragment/SettingsFragment.java'
replace(settings, '\t\tps.addListPref(o -> {\n\t\t\to.store = a.getPrefs();\n\t\t\to.pref = theme;',
        '\t\ta.getPrefs().getThemePref(theme == MainActivityPrefs.THEME_AA);\n'
        '\t\tps.addListPref(o -> {\n\t\t\to.store = a.getPrefs();\n\t\t\to.pref = theme;')
replace(settings, '''o.values = new int[]{R.string.theme_dark, R.string.theme_light, R.string.theme_system,
					R.string.theme_black, R.string.theme_star_wars, R.string.theme_purple,
					R.string.theme_classic};''', '''o.values = new int[]{R.string.theme_system, R.string.theme_light, R.string.theme_dark};
            o.valuesMap = new int[]{MainActivityPrefs.THEME_SYSTEM,
                    MainActivityPrefs.THEME_LIGHT, MainActivityPrefs.THEME_DARK};''')

# Styles explicitly declare light/dark identity; shared XML consumes theme attributes.
palette = {
 'android:colorBackground':'#F7F4FB', 'colorPrimaryDark':'#ECE6F4',
 'colorPrimary':'#F1ECF7', 'colorOnPrimary':'#42275F',
 'android:textColorPrimary':'#241831', 'colorSecondary':'#FFFFFF',
 'colorOnSecondary':'#62427F', 'android:textColorSecondary':'#51425F',
 'boxStrokeColor':'#D6CADD', 'alpha':'1', 'colorSecondaryVariant':'#E5D8F5',
 'android:textColorTertiary':'#2A173D', 'colorSurface':'#F6F0FC',
 'colorOnSurface':'#241831', 'colorPrimarySurface':'#EDE3F7',
 'colorOnPrimarySurface':'#241831', 'colorAccent':'#74429B',
 'rippleColor':'#3074429B', 'android:textColorHint':'#6B5B78',
 'colorControlNormal':'#62427F', 'colorControlActivated':'#74429B',
 'android:isLightTheme':'true', 'android:windowLightStatusBar':'true',
 'android:windowLightNavigationBar':'true',
}
write(app + 'res/values/theme_light.xml', '<resources><style name="AppTheme.Light">' +
      ''.join(f'<item name="{k}">{v}</item>' for k,v in palette.items()) + '</style></resources>')
dark = app + 'res/values/theme_dark.xml'
s = (root / dark).read_text(encoding='utf-8')
s = s.replace('</style>', '<item name="android:isLightTheme">false</item>'
              '<item name="android:windowLightStatusBar">false</item>'
              '<item name="android:windowLightNavigationBar">false</item></style>')
write(dark, s)

A = '{http://schemas.android.com/apk/res/android}'
ET.register_namespace('android', A[1:-1])
for p in [util+'res/drawable/lumidrive_nav_button.xml', util+'res/drawable/lumidrive_toolbar_button.xml',
          app+'res/drawable/lumidrive_control_button.xml']:
    doc = ET.parse(root / p).getroot()
    for item in doc:
        active = any(item.get(A+k) == 'true' for k in ('state_focused','state_selected','state_pressed'))
        for node in item.iter('solid'): node.set(A+'color', '?attr/colorSecondaryVariant' if active else '?attr/colorSecondary')
        for node in item.iter('stroke'): node.set(A+'color', '?attr/colorAccent' if active else '?attr/boxStrokeColor')
    write(p, ET.tostring(doc, encoding='unicode'))
for name in ('media_item', 'media_item_border'):
    p = app + f'res/color/{name}.xml'
    doc = ET.parse(root / p).getroot()
    for item in doc:
        active = any(item.get(A+k) == 'true' for k in ('state_focused','state_selected','state_pressed','state_activated'))
        item.set(A+'color', ('?attr/colorAccent' if active else '?attr/boxStrokeColor') if name.endswith('border')
                 else ('?attr/colorSecondaryVariant' if active else '?attr/colorSecondary'))
    write(p, ET.tostring(doc, encoding='unicode'))
write(app + 'res/drawable/lumidrive_home_background.xml',
      '<shape xmlns:android="http://schemas.android.com/apk/res/android"><solid android:color="?android:attr/colorBackground"/></shape>')
write(app + 'res/values/lumidrive_styles.xml', '''<resources>
<style name="LumiDrive.FloatingButtonStyle" parent="Theme.Utils.Base.FloatingButtonStyle">
<item name="backgroundTint">?attr/colorSecondaryVariant</item>
<item name="tint">?attr/colorOnSecondary</item>
<item name="borderColor">?attr/boxStrokeColor</item>
<item name="borderFocusColor">?attr/colorAccent</item>
<item name="rippleColor">?attr/rippleColor</item>
</style></resources>''')
for mode in ('grid','list'):
    replace(app + f'res/layout/media_item_{mode}_layout.xml',
            'android:tint="#EBDDFA"', 'android:tint="?attr/colorOnSecondary"')

write(util + 'java/me/aap/utils/ui/LumiThemeColors.java', '''package me.aap.utils.ui;
import android.content.Context;
import android.content.res.TypedArray;
public final class LumiThemeColors {
    private LumiThemeColors() {}
    public static boolean light(Context c) {
        TypedArray a = c.obtainStyledAttributes(new int[]{android.R.attr.isLightTheme});
        boolean light = a.getBoolean(0, false); a.recycle(); return light;
    }
    public static int attr(Context c, int attr) {
        TypedArray a = c.obtainStyledAttributes(new int[]{attr});
        int color = a.getColor(0, 0xff241831); a.recycle(); return color;
    }
    public static int text(Context c) { return attr(c, android.R.attr.textColorPrimary); }
    public static int secondary(Context c) { return attr(c, android.R.attr.textColorSecondary); }
    public static int surface(Context c) { return attr(c, com.google.android.material.R.attr.colorSurface); }
    public static int label(Context c, int original) {
        return light(c) ? text(c) : original;
    }
    public static int background(Context c, int original) {
        if (original == 0 || !light(c)) return original;
        return 0xfff1eaf8;
    }
    public static int edge(Context c, int original) {
        return original == 0 ? 0 : (light(c) ? 0xff9676b3 : original);
    }
}''')
helper = 'me.aap.utils.ui.LumiThemeColors'

# Both dashboards have static drawing helpers: pass their own Context, never global state.
for name in ('LumiDriveDashboard', 'LumiDriveAutoHome'):
    p = app + f'java/me/aap/fermata/ui/activity/{name}.java'
    s = (root / p).read_text(encoding='utf-8')
    s = s.replace('round(', 'round(ctx, ').replace('gradient(', 'gradient(ctx, ')
    s = s.replace('round(ctx, int', 'round(Context ctx, int').replace('gradient(ctx, int', 'gradient(Context ctx, int')
    s = s.replace('view.setTextColor(color);', f'view.setTextColor({helper}.label(ctx, color));')
    s = s.replace('ColorStateList.valueOf(color)', f'ColorStateList.valueOf({helper}.label(ctx, color))')
    s = s.replace('ColorStateList.valueOf(CYAN)', f'ColorStateList.valueOf({helper}.label(ctx, CYAN))')
    s = s.replace('ColorStateList.valueOf(accents[index])', f'ColorStateList.valueOf({helper}.label(ctx, accents[index]))')
    s = s.replace('logo.setGravity(Gravity.CENTER);', 'logo.setGravity(Gravity.CENTER);\n        logo.setTextColor(0xffffffff);')
    # Color transforms are confined to drawing helpers, preserving all listeners.
    marker = 'private static GradientDrawable round(Context ctx, int color, int radius, int border) {'
    assert marker in s
    s = s.replace(marker, marker + f'\n        color = {helper}.background(ctx, color);\n        border = {helper}.edge(ctx, border);')
    first,last = ('first','last') if name.endswith('AutoHome') else ('start','end')
    marker = f'private static GradientDrawable gradient(Context ctx, int {first}, int {last}, int radius, int border) {{'
    assert marker in s
    s = s.replace(marker, marker + f'''
        if ({first} != 0xFF7F4BC2 && {first} != 0xFF854BC7) {{
            {first} = {helper}.background(ctx, {first});
            {last} = {helper}.background(ctx, {last});
            border = {helper}.edge(ctx, border);
        }}''')
    write(p, s)

# Programmatically created IPTV and diagnostic text must match its actual themed context.
for p in [settings, 'modules/tv/src/main/java/me/aap/fermata/addon/tv/LumiWorldTv.java']:
    s = (root / p).read_text(encoding='utf-8')
    s = re.sub(r'(\b(?:text|save|info|search|empty|view))\.setTextColor\((?:android.graphics.)?Color.WHITE\)',
               lambda m: f'{m[1]}.setTextColor({helper}.text({m[1]}.getContext()))', s)
    s = s.replace('((TextView) view).setTextColor(Color.WHITE)',
                  f'((TextView) view).setTextColor({helper}.text(view.getContext()))')
    s = s.replace('((android.widget.TextView) view).setTextColor(android.graphics.Color.WHITE)',
                  f'((android.widget.TextView) view).setTextColor({helper}.text(view.getContext()))')
    s = s.replace('.setTextColor(android.graphics.Color.WHITE);',
                  f'.setTextColor({helper}.text(a.getContext()));') if 'LumiWorldTv' not in p else s
    for v in ('content','view'):
        s = s.replace(f'{v}.setBackgroundColor(0xff24173d)', f'{v}.setBackgroundColor({helper}.surface({v}.getContext()))')
    s = s.replace('search.setHintTextColor(0xffcccccc)', f'search.setHintTextColor({helper}.secondary(context))')
    write(p, s)
menu = util + 'java/me/aap/utils/ui/menu/OverlayMenuView.java'
replace(menu, 'v.setTextColor(0xfffaf7ff);', f'v.setTextColor({helper}.text(ctx));')
replace(menu, 'panel.setStroke((int) toPx(ctx, 1), 0xff655079);',
        f'panel.setStroke((int) toPx(ctx, 1), {helper}.edge(ctx, 0xff655079));')

# Manifest consumes uiMode changes; explicitly refresh phone UI when following system.
activity = app + 'java/me/aap/fermata/ui/activity/MainActivity.java'
replace(activity, 'private static MainActivity activeInstance;', 'private static MainActivity activeInstance;\n    private int lumiNightMode;')
replace(activity, 'protected void onCreate(Bundle savedInstanceState) {', '''protected void onCreate(Bundle savedInstanceState) {
        lumiNightMode = getResources().getConfiguration().uiMode & android.content.res.Configuration.UI_MODE_NIGHT_MASK;''')
replace(activity, '\t@Override\n\tprotected void onDestroy() {', '''
    @Override
    public void onConfigurationChanged(android.content.res.Configuration config) {
        super.onConfigurationChanged(config);
        int mode = config.uiMode & android.content.res.Configuration.UI_MODE_NIGHT_MASK;
        boolean changed = mode != lumiNightMode;
        lumiNightMode = mode;
        if (changed) getActivityDelegate().onSuccess(a -> {
            boolean auto = isCarActivity() || FermataApplication.get().isMirroringMode();
            if (a.getPrefs().getThemePref(auto) == MainActivityPrefs.THEME_SYSTEM) a.recreate();
        });
    }
    @Override
    protected void onDestroy() {''')
replace('gradle/libs.versions.toml', 'appVersionCode = "297"', 'appVersionCode = "298"')
replace('gradle/libs.versions.toml', 'appVersionName = "0.8.0-preview2"', 'appVersionName = "0.8.0-preview3"')
print('Three-theme selection, legacy preference migration, themed resources and phone uiMode refresh applied')

