#!/usr/bin/env python3
"""First LumiDrive test branding patch for Fermata 2.0.2 (GPL-3.0)."""
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
strings = root / "fermata/src/main/res/values/strings.xml"
icon = root / "fermata/src/main/res/drawable/launcher.xml"
settings = root / "settings.gradle"
for p in (strings, icon, settings, root / "LICENSE", root / "fermata/build.gradle"):
    if not p.is_file():
        raise SystemExit(f"Missing upstream file: {p}")

names = {
    "app_name_mobile_release": "LumiDrive",
    "app_name_auto_release": "LumiDrive",
    "app_name_mobile_debug": "LumiDrive Dev",
    "app_name_auto_debug": "LumiDrive Dev",
    "mirror_service_name_release": "LumiDrive Mirror",
    "mirror_service_name_debug": "LumiDrive Dev Mirror",
    "mirror_fs_service_name_release": "LumiDrive FS Mirror",
    "mirror_fs_service_name_debug": "LumiDrive Dev FS Mirror",
    "media_service_name_auto_release": "LumiDrive Media",
    "media_service_name_auto_debug": "LumiDrive Dev Media",
}
# Change base translations as well, so branding is not locale-dependent.
for path in (root / "fermata/src/main/res").glob("values*/strings.xml"):
    original = path.read_text(encoding="utf-8")
    changed = original
    for key, label in names.items():
        pattern = re.compile(r'(<string\s+name="' + re.escape(key) + r'"[^>]*>)([^<]*)(</string>)')
        changed = pattern.sub(lambda m: m.group(1) + label + m.group(3), changed)
    if path == strings:
        for key in names:
            if not re.search(r'<string\s+name="' + key + r'"', changed):
                raise SystemExit(f"Missing base resource: {key}")
    if changed != original:
        path.write_text(changed, encoding="utf-8")

icon.write_text("""<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#14243A"
        android:pathData="M8,0 H100 Q108,0 108,8 V100 Q108,108 100,108 H8 Q0,108 0,100 V8 Q0,0 8,0 Z"/>
    <path android:fillColor="#54CEFF"
        android:pathData="M23,22 H36 V72 H61 V85 H23 Z"/>
    <path android:fillColor="#FFFFFF"
        android:pathData="M63,38 L88,54 L63,70 Z"/>
</vector>
""", encoding="utf-8")
content = settings.read_text(encoding="utf-8")
content, n = re.subn(r"rootProject\.name\s*=\s*(['\"]).*?\1",
                     "rootProject.name = 'LumiDrive'", content, count=1)
if n != 1:
    raise SystemExit("Root project name not found")
settings.write_text(content, encoding="utf-8")
(root / "LUMIDRIVE_CHANGES.md").write_text("""# LumiDrive changes to Fermata 2.0.2

Original project: https://github.com/AndreyPavlenko/Fermata
Copyright: Andrey Pavlenko and contributors.
License: GNU GPL-3.0; original LICENSE and copyright notices retained.

- Branding changed to LumiDrive in default/translations where present.
- Main launcher drawable replaced with LumiDrive vector artwork.
- Gradle root project name changed to LumiDrive.
- Application ID set via build parameters to com.lumi.drive.auto.
- IPTV, web, YouTube and car services otherwise remain upstream code.

This is an experimental test build, not a verified release.
The prebuilt auto SDK dependency must be reviewed before public distribution.
""", encoding="utf-8")
print("LumiDrive branding applied successfully.")



# LumiDrive v0.3: purple / pink / cyan visual identity, rounded controls,
# adaptive launcher and Android Auto icons. Keep playback code untouched.
import xml.etree.ElementTree as ET

def write_xml(relative_path, xml):
    p = root / relative_path
    if not p.parent.is_dir():
        raise SystemExit(f"Missing resource directory: {p.parent}")
    ET.fromstring(xml)
    p.write_text(xml.rstrip() + "\n", encoding="utf-8")

def replace_exact(relative_path, before, after):
    p = root / relative_path
    old = p.read_text(encoding="utf-8")
    if before not in old:
        raise SystemExit(f"Cannot find expected text in {relative_path}: {before[:90]}")
    p.write_text(old.replace(before, after), encoding="utf-8")

colors = {
    "background": "#130D26",
    "surface": "#24173D",
    "panel": "#1C1232",
    "deep": "#0C0A1D",
    "purple": "#AE8AFF",
    "pink": "#FF7AC8",
    "cyan": "#8FE7FF",
    "white": "#FFF8FF",
}

def main_theme(name):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme.{name}">
        <item name="android:colorBackground">{colors['background']}</item>
        <item name="colorPrimaryDark">{colors['deep']}</item>
        <item name="colorPrimary">{colors['panel']}</item>
        <item name="colorOnPrimary">{colors['cyan']}</item>
        <item name="android:textColorPrimary">{colors['white']}</item>
        <item name="colorSecondary">{colors['surface']}</item>
        <item name="colorOnSecondary">{colors['purple']}</item>
        <item name="android:textColorSecondary">#EFE9FA</item>
        <item name="boxStrokeColor">#8463A9</item>
        <item name="alpha">1</item>
        <item name="colorSecondaryVariant">{colors['pink']}</item>
        <item name="android:textColorTertiary">{colors['white']}</item>
        <item name="colorSurface">#302047</item>
        <item name="colorOnSurface">{colors['white']}</item>
        <item name="colorPrimarySurface">#302047</item>
        <item name="colorOnPrimarySurface">{colors['white']}</item>
        <item name="colorAccent">{colors['pink']}</item>
        <item name="rippleColor">#668FE7FF</item>
        <item name="android:textColorHint">#BDAED9</item>
        <item name="colorControlNormal">#B99DE0</item>
        <item name="colorControlActivated">{colors['cyan']}</item>
    </style>
</resources>
"""

# The default phone theme was Classic. Auto used Dark. Style both paths.
write_xml("fermata/src/main/res/values/theme_dark.xml", main_theme("Dark"))
write_xml("fermata/src/main/res/values/theme_purple.xml", main_theme("Purple"))
replace_exact(
    "fermata/src/main/java/me/aap/fermata/ui/activity/MainActivityPrefs.java",
    'THEME_MAIN = Pref.i("THEME_MAIN", THEME_CLASSIC)',
    'THEME_MAIN = Pref.i("THEME_MAIN", THEME_PURPLE)',
)
replace_exact(
    "fermata/src/main/res/values/theme.xml",
    '<item name="cornerRadius">5dp</item>',
    '<item name="cornerRadius">20dp</item>',
)
replace_exact(
    "fermata/src/main/res/values/theme.xml",
    '<item name="android:forceDarkAllowed" tools:targetApi="q">true</item>',
    '<item name="android:forceDarkAllowed" tools:targetApi="q">false</item>',
)

# Accent the shared Material toolbar, navbar and floating action button.
replace_exact(
    "fermata/src/main/res/values/theme.xml",
    '<item name="appMediaItemStyle">@style/AppTheme.MediaItemStyle</item>',
    '<item name="appMediaItemStyle">@style/AppTheme.MediaItemStyle</item>\n'
    '        <item name="floatingActionButtonStyle">@style/LumiDrive.FloatingButtonStyle</item>',
)
write_xml("fermata/src/main/res/values/lumidrive_styles.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="LumiDrive.FloatingButtonStyle" parent="Theme.Utils.Base.FloatingButtonStyle">
        <item name="backgroundTint">#362252</item>
        <item name="tint">#8FE7FF</item>
        <item name="borderColor">#FF7AC8</item>
        <item name="borderFocusColor">#8FE7FF</item>
        <item name="rippleColor">#AE8AFF</item>
    </style>
</resources>
""")

# The main launcher and the AA media service each have their own adaptive icons.
write_xml("fermata/src/main/res/drawable/lumidrive_background.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <gradient android:angle="135" android:startColor="#3D1A63"
        android:centerColor="#251544" android:endColor="#10122D" />
</shape>
""")
write_xml("fermata/src/main/res/drawable/lumidrive_mark.xml", """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#AE8AFF"
        android:pathData="M54,13 C77,13 95,31 95,54 C95,77 77,95 54,95 C31,95 13,77 13,54 C13,31 31,13 54,13 Z"/>
    <path android:fillColor="#27153D"
        android:pathData="M54,21 C73,21 87,35 87,54 C87,73 73,87 54,87 C35,87 21,73 21,54 C21,35 35,21 54,21 Z"/>
    <path android:fillColor="#8FE7FF"
        android:pathData="M32,31 L43,31 L43,68 L57,68 L57,78 L32,78 Z"/>
    <path android:fillColor="#FF7AC8"
        android:pathData="M57,35 L79,54 L57,73 Z"/>
    <path android:fillColor="#FFFFFF"
        android:pathData="M34,33 L39,33 L39,36 L34,36 Z"/>
</vector>
""")
write_xml("fermata/src/main/res/drawable/lumidrive_monochrome.xml", """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#FFFFFF"
        android:pathData="M32,31 L43,31 L43,68 L57,68 L57,78 L32,78 Z"/>
    <path android:fillColor="#FFFFFF"
        android:pathData="M57,35 L79,54 L57,73 Z"/>
</vector>
""")
write_xml("fermata/src/main/res/drawable/launcher.xml", """<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@drawable/lumidrive_background" />
    <item android:drawable="@drawable/lumidrive_mark" />
</layer-list>
""")
write_xml("fermata/src/main/res/drawable-anydpi-v26/launcher.xml", """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/lumidrive_background" />
    <foreground android:drawable="@drawable/lumidrive_mark" />
    <monochrome android:drawable="@drawable/lumidrive_monochrome" />
</adaptive-icon>
""")
write_xml("fermata/src/auto/res/drawable/media_service.xml", """<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@drawable/lumidrive_background" />
    <item android:drawable="@drawable/lumidrive_mark" />
</layer-list>
""")
write_xml("fermata/src/auto/res/drawable-anydpi-v26/media_service.xml", """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/lumidrive_background" />
    <foreground android:drawable="@drawable/lumidrive_mark" />
</adaptive-icon>
""")

# Rounded, stateful navigation/toolbar controls: the utility library owns them.
write_xml("depends/utils/src/main/res/drawable/lumidrive_nav_button.xml", """<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_selected="true">
        <shape><gradient android:angle="0" android:startColor="#60419A"
            android:endColor="#A83F91" /><corners android:radius="22dp" /></shape>
    </item>
    <item android:state_pressed="true">
        <shape><solid android:color="#7855B9"/><corners android:radius="22dp" /></shape>
    </item>
    <item android:state_focused="true">
        <shape><solid android:color="#503B7D"/>
            <stroke android:width="1dp" android:color="#8FE7FF"/>
            <corners android:radius="22dp" /></shape>
    </item>
    <item>
        <shape><solid android:color="#221732"/><corners android:radius="22dp" /></shape>
    </item>
</selector>
""")
write_xml("depends/utils/src/main/res/drawable/lumidrive_toolbar_button.xml", """<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_pressed="true">
        <shape><solid android:color="#623E88"/><corners android:radius="22dp" /></shape>
    </item>
    <item android:state_focused="true">
        <shape><solid android:color="#3E285B"/>
            <stroke android:width="1dp" android:color="#FF7AC8"/>
            <corners android:radius="22dp" /></shape>
    </item>
    <item>
        <shape><solid android:color="#2D1B47"/><corners android:radius="22dp" /></shape>
    </item>
</selector>
""")
write_xml("fermata/src/main/res/drawable/lumidrive_control_button.xml", """<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_pressed="true">
        <shape><gradient android:angle="0" android:startColor="#AE55A8"
            android:endColor="#6052B3" /><corners android:radius="18dp" /></shape>
    </item>
    <item android:state_focused="true">
        <shape><solid android:color="#48306C"/>
            <stroke android:width="1dp" android:color="#8FE7FF"/>
            <corners android:radius="18dp" /></shape>
    </item>
    <item>
        <shape><solid android:color="#322045"/>
            <stroke android:width="1dp" android:color="#70478C"/>
            <corners android:radius="18dp" /></shape>
    </item>
</selector>
""")
replace_exact(
    "depends/utils/src/main/java/me/aap/utils/ui/view/NavBarView.java",
    "b.setBackgroundResource(R.drawable.focusable_shape_transparent);",
    "b.setBackgroundResource(R.drawable.lumidrive_nav_button);",
)
replace_exact(
    "depends/utils/src/main/java/me/aap/utils/ui/view/ToolBarView.java",
    "b.setBackgroundResource(R.drawable.focusable_shape_transparent);",
    "b.setBackgroundResource(R.drawable.lumidrive_toolbar_button);",
)

# Change ONLY the five playback controls, leave seek and menu behavior alone.
for name in ("control_panel_view.xml", "control_panel_view2.xml"):
    panel = root / "fermata/src/main/res/layout" / name
    xml = panel.read_text(encoding="utf-8")
    for control in ("control_prev", "control_rw", "control_play_pause", "control_ff", "control_next"):
        pattern = re.compile(r'(<me\.aap\.utils\.ui\.view\.ImageButton\b(?:(?!/>).)*?'
                             r'android:id="@\+id/' + re.escape(control) + r'"(?:(?!/>).)*?)/>', re.S)
        # Some layout variants place the id on a different line, but still in the same element.
        matches = list(pattern.finditer(xml))
        if not matches:
            continue
        if len(matches) > 1:
            raise SystemExit(f"Duplicate control button {control} in {name}")
        original = matches[0].group(0)
        changed = original.replace(
            'android:background="@drawable/focusable_shape_transparent"',
            'android:background="@drawable/lumidrive_control_button"',
        )
        if changed == original:
            raise SystemExit(f"Missing button background: {control} in {name}")
        xml = xml[:matches[0].start()] + changed + xml[matches[0].end():]
    ET.fromstring(xml)
    panel.write_text(xml, encoding="utf-8")

# Monotonic versionCode for updating v0.2 on the same phone.
catalog = root / "gradle/libs.versions.toml"
original_catalog = catalog.read_text(encoding="utf-8")
if 'appVersionCode = "268"' not in original_catalog or 'appVersionName = "2.0.2"' not in original_catalog:
    raise SystemExit("Pinned Fermata 2.0.2 catalog changed; review version before patch")
catalog.write_text(
    original_catalog.replace('appVersionCode = "268"', 'appVersionCode = "283"')
                    .replace('appVersionName = "2.0.2"', 'appVersionName = "0.7.1"'),
    encoding="utf-8",
)

changes = root / "LUMIDRIVE_CHANGES.md"
changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.3 visual refresh
- Purple, pink and cyan dark themes for phone and Android Auto.
- Rounded toolbar, navigation, media and control-panel buttons.
- Replaced phone launcher, adaptive icon and Android Auto media icon.
- Default phone theme is now LumiDrive Purple; AA theme uses matching Dark palette.
- Package remains com.lumi.drive.auto; versionCode increased to 283.
""", encoding="utf-8")
print("LumiDrive v0.3 colorful rounded UI and adaptive icons applied successfully.")


# LumiDrive v0.4: prevent the separate LumiDrive package from offering
# upstream Fermata APK updates, which would be misleading and incompatible.
replace_exact(
    "fermata/src/main/java/me/aap/fermata/ui/activity/MainActivity.java",
    "public void checkUpdates() {\n\t\tif (!BuildConfig.AUTO) return;",
    "public void checkUpdates() {\n\t\tif (getPackageName().startsWith(\"com.lumi.drive\")) return;\n\t\tif (!BuildConfig.AUTO) return;",
)


# LumiDrive v0.4, stage 1: apply a distinct layered phone background.
# This is a real runtime resource change, not a mockup. Keep all view IDs and
# navigation handlers unchanged while the card launcher is developed.
write_xml("fermata/src/main/res/drawable/lumidrive_home_background.xml", """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <gradient android:angle="270"
        android:startColor="#10091E"
        android:centerColor="#1C1030"
        android:endColor="#10091E" />
</shape>
""")
replace_exact(
    "fermata/src/main/res/layout/main_activity.xml",
    'android:id="@+id/main_activity"\n    android:layout_width',
    'android:id="@+id/main_activity"\n    android:layout_width',
)
replace_exact(
    "fermata/src/main/res/layout/main_activity.xml",
    'android:background="?android:colorPrimary"',
    'android:background="@drawable/lumidrive_home_background"',
)
replace_exact(
    "fermata/src/main/res/layout/main_activity.xml",
    'android:background="?android:colorBackground"',
    'android:background="@drawable/lumidrive_home_background"',
)
print("LumiDrive v0.4 stage 1 phone background applied.")

# LumiDrive 0.5: copy the separately maintained, real home UI Java source.
dashboard = Path(__file__).resolve().parent / "src" / "LumiDriveDashboard.java"
if not dashboard.is_file():
    raise SystemExit(f"Missing LumiDrive dashboard source: {dashboard}")
(root / "fermata/src/main/java/me/aap/fermata/ui/activity/LumiDriveDashboard.java").write_text(
    dashboard.read_text(encoding="utf-8"), encoding="utf-8")
# Do NOT intercept ToolBarView touch/long-click events. This view contains
# Save (tick), Cancel (X) and Back actions, which must retain upstream handlers.
# The LumiDrive home remains available via the bottom nav overflow "Главная".
# LumiDrive 0.5: open new home when launched normally on the phone.
# Leave Android Auto, mirroring and deep-link intent flows untouched.
replace_exact(
    "fermata/src/main/java/me/aap/fermata/ui/activity/MainActivityDelegate.java",
    "private void defaultIntent() {",
    "private void defaultIntent() {\n"
    "\t\tif (!getAppActivity().isCarActivity() && !FermataApplication.get().isMirroringMode()) {\n"
    "\t\t\tif (getActiveFragment() == null) showFragment(R.id.folders_fragment);\n"
    "\t\t\tpost(() -> LumiDriveDashboard.show(this));\n"
    "\t\t\tcheckUpdates();\n"
    "\t\t\treturn;\n"
    "\t\t}\n",
)

# Back button closes LumiDrive first rather than exiting the underlying player.
replace_exact(
    "fermata/src/main/java/me/aap/fermata/ui/activity/MainActivity.java",
    "public void handleOnBackPressed() {\n"
    "\t\t\t\tgetActivityDelegate().onSuccess(MainActivityDelegate::onBackPressed);",
    "public void handleOnBackPressed() {\n"
    "\t\t\t\tif (LumiDriveDashboard.hide(MainActivity.this)) return;\n"
    "\t\t\t\tgetActivityDelegate().onSuccess(MainActivityDelegate::onBackPressed);",
)

# LumiDrive 0.5.1: override About text in ALL installed locales, not only
# the base strings.xml. The Russian translation previously displayed Fermata.
about_en = """<H1 align="center">LumiDrive</H1>
        <p>LumiDrive brings IPTV, YouTube, web browsing and local media together.</p>
        <p><b>Developer:</b> Sergey Vardanyan</p>
        <p><b>Version:</b> %1$s (%2$d)</p>
        <p><b>Support:</b> <a href="https://app.binance.com/uni-qr/Jv3MYVZ8">Donate via Binance Pay</a> (User-92ef9)</p>
        <hr/>
        <p><small>Open-source notices: Based on Fermata Media Player
        by Andrey Pavlenko and contributors (GNU GPL-3.0).
        <a href="%3$s">Original source and license</a>.</small></p>"""
about_ru = """<H1 align="center">LumiDrive</H1>
        <p>LumiDrive — медиаплеер с IPTV, YouTube, браузером и медиатекой.</p>
        <p><b>Разработчик:</b> Sergey Vardanyan</p>
        <p><b>Версия:</b> %1$s (%2$d)</p>
        <p><b>Поддержать:</b> <a href="https://app.binance.com/uni-qr/Jv3MYVZ8">Binance Pay</a> (User-92ef9)</p>
        <hr/>
        <p><small>Лицензии: основан на Fermata Media Player,
        автор Андрей Павленко и участники проекта (GNU GPL-3.0).
        <a href="%3$s">Исходный код и лицензия</a>.</small></p>"""
about_pattern = re.compile(
    r'(<string\s+name="about_html"[^>]*><!\[CDATA\[)(.*?)(\]\]></string>)',
    re.S,
)
about_count = 0
for path in sorted((root / "fermata/src/main/res").glob("values*/strings.xml")):
    raw = path.read_text(encoding="utf-8")
    translated = (path.parent.name == "values-ru")
    label = about_ru if translated else about_en
    changed, hits = about_pattern.subn(lambda m: m.group(1) + label + m.group(3), raw)
    if hits > 1:
        raise SystemExit(f"Multiple About text entries in {path}")
    if hits:
        path.write_text(changed, encoding="utf-8")
        about_count += 1
if about_count < 2:
    raise SystemExit("About translations not found")

# This is the user's own Binance Pay receive link, decoded from the QR
# image they supplied. It is launched externally; the payer chooses an amount
# and explicitly confirms the transfer inside Binance.
for locale, label in (
    ("values", "Donate"),
    ("values-ru", "Поддержать"),
):
    path = root / "fermata/src/main/res" / locale / "strings.xml"
    raw = path.read_text(encoding="utf-8")
    if 'name="lumidrive_donate"' in raw:
        raise SystemExit(f"Duplicate Donate resource in {path}")
    addition = '    <string name="lumidrive_donate">' + label + '</string>\n'
    if raw.count("</resources>") != 1:
        raise SystemExit(f"Unexpected resource XML in {path}")
    path.write_text(raw.replace("</resources>", addition + "</resources>"),
                    encoding="utf-8")

nav_path = "fermata/src/main/java/me/aap/fermata/ui/fragment/NavBarMediator.java"
replace_exact(
    nav_path,
    'if (BuildConfig.AUTO) b.addItem(R.id.nav_donate, R.drawable.coffee, R.string.donate);',
    'if (BuildConfig.AUTO && !a.isCarActivityNotMirror()) '
    'b.addItem(R.id.nav_donate, R.drawable.coffee, R.string.lumidrive_donate);',
)
replace_exact(
    nav_path,
    'v.setOnClickListener(t -> openUrl(t.getContext(), url));',
    'v.setMovementMethod(android.text.method.LinkMovementMethod.getInstance());',
)
nav_file = root / nav_path
nav_text = nav_file.read_text(encoding="utf-8")
anchor_start = '\t\tMainActivityDelegate a;\n\t\tif (BuildConfig.AUTO && (item.getItemId() == R.id.nav_donate)) {'
anchor_end = '\n\t\treturn false;\n\t}\n\n\tprivate static void openUrl('
start = nav_text.find(anchor_start)
stop = nav_text.find(anchor_end, start)
if start == -1 or stop == -1:
    raise SystemExit("Upstream donation block changed; refusing an unsafe patch")
new_donation = """\t\tif (BuildConfig.AUTO && (item.getItemId() == R.id.nav_donate)) {
            openUrl(item.getContext(), "https://app.binance.com/uni-qr/Jv3MYVZ8");
            return true;
        }
"""
nav_text = nav_text[:start] + new_donation + nav_text[stop:]
nav_file.write_text(nav_text, encoding="utf-8")

# Do not offer generic old donate descriptions as if they were LumiDrive's.
# Licensing and original author attribution remain available under About.

changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.5.0 home experience
- Phone now opens the full-screen LumiDrive dashboard on normal launcher starts.
- Russian navigation labels, integrated module icons and a continue-watching shortcut.
- Original IPTV, YouTube, browser, library, favorites, settings and playback remain routed
  through their existing fragments; return to home via toolbar long press.
- Android Auto and screen mirroring skip the new home screen.
- Phone Back hides the new home without closing the player.
- About screen is branded LumiDrive; original GPL attribution remains visible.
- Version 0.5.0 / 272 for updating the installed 0.4.2 / 271.
""", encoding="utf-8")
changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.5.1 top spacing / Home / PayPal
- Respect the status bar inset on the phone dashboard.
- Add a persistent center-bottom one-tap Home shortcut on phone pages.
- Update About across locales: LumiDrive developer identity/version; legal attribution retained.
- Remove original donation choices and links; show PayPal placeholder with no payment URL.
- Version 0.5.1 / 273.
""", encoding="utf-8")
print("LumiDrive v0.5.1 phone UI, About, and PayPal support option applied.")

# LumiDrive 0.5.2: the Home shortcut belongs in the nav-bar overflow ("More")
# with YouTube, Web Browser, and Menu — never floating above video controls.
write_xml("fermata/src/main/res/values/lumidrive_nav.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <item name="lumidrive_home" type="id"/>
    <string name="lumidrive_home_title">Home</string>
</resources>
""")
write_xml("fermata/src/main/res/values-ru/lumidrive_nav.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="lumidrive_home_title">Главная</string>
</resources>
""")
write_xml("fermata/src/main/res/drawable/lumidrive_home_icon.xml", """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp"
    android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#8FE7FF"
        android:pathData="M12,2 L2,11 L4,13 L5,12.1 V21 H10 V15 H14 V21 H19 V12.1 L20,13 L22,11 Z"/>
</vector>
""")

replace_exact(
    nav_path,
    'import me.aap.fermata.ui.activity.MainActivityDelegate;',
    'import me.aap.fermata.ui.activity.MainActivityDelegate;\n'
    'import me.aap.fermata.ui.activity.LumiDriveDashboard;',
)
replace_exact(
    nav_path,
    '\t\t\t\tcase "menu":\n'
    '\t\t\t\t\titems.add(create(ctx, R.id.menu, me.aap.utils.R.drawable.menu, R.string.menu,',
    '\t\t\t\tcase "menu":\n'
    '\t\t\t\t\tif (!MainActivityDelegate.get(ctx).getAppActivity().isCarActivity()\n'
    '\t\t\t\t\t\t\t&& !FermataApplication.get().isMirroringMode()) {\n'
    '\t\t\t\t\t\titems.add(create(ctx, R.id.lumidrive_home, R.drawable.lumidrive_home_icon,\n'
    '\t\t\t\t\t\t\t\tR.string.lumidrive_home_title, false));\n'
    '\t\t\t\t\t}\n'
    '\t\t\t\t\titems.add(create(ctx, R.id.menu, me.aap.utils.R.drawable.menu, R.string.menu,',
)
replace_exact(
    nav_path,
    'public void itemSelected(View item, int id, ActivityDelegate a) {\n'
    '\t\tif (id == R.id.menu) {',
    'public void itemSelected(View item, int id, ActivityDelegate a) {\n'
    '\t\tif (id == R.id.lumidrive_home) {\n'
    '\t\t\tLumiDriveDashboard.show(MainActivityDelegate.get(item.getContext()));\n'
    '\t\t} else if (id == R.id.menu) {',
)
replace_exact(
    nav_path,
    'protected boolean extItemSelected(OverlayMenuItem item) {\n'
    '\t\tif (item.getItemId() == R.id.menu) {',
    'protected boolean extItemSelected(OverlayMenuItem item) {\n'
    '\t\tif (item.getItemId() == R.id.lumidrive_home) {\n'
    '\t\t\tLumiDriveDashboard.show(MainActivityDelegate.get(item.getContext()));\n'
    '\t\t\treturn true;\n'
    '\t\t} else if (item.getItemId() == R.id.menu) {',
)
changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.5.2 navigation convenience
- Remove center-screen floating shortcut because it overlays video playback controls.
- Add "Главная" / "Home" with home icon to the bottom navigation overflow popover.
- A single tap on this popover entry opens the full-screen LumiDrive home.
- Keep the Home entry out of Android Auto and mirroring mode.
- Version 0.5.2 / 274, upgrading 0.5.1 / 273.
""", encoding="utf-8")
print("LumiDrive v0.5.2 non-obstructive Home navigation applied.")


# v0.5.3 regression guard: toolbar's original controls must remain untouched.
activity_java = (root / "fermata/src/main/java/me/aap/fermata/ui/activity/MainActivityDelegate.java").read_text(encoding="utf-8")
if "toolBar.setOnLongClickListener(v -> {" in activity_java:
    raise SystemExit("Regression: dashboard must never intercept toolbar touch events")
if activity_java.count("LumiDriveDashboard.show(this)") != 1:
    raise SystemExit("Expected exactly one phone-home launch call in defaultIntent")
changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.5.3 toolbar regression fix
- Remove the outdated toolbar long-press handler.
- Preserve original Back, Save and Cancel toolbar behavior, including IPTV source forms.
- Keep one-tap "Главная" in the bottom navigation overflow popover.
- Version 0.5.3 / 275.
""", encoding="utf-8")
print("LumiDrive 0.5.3 toolbar input handler fix applied.")

changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.5.4 direct Binance Pay support
- Remove the inactive PayPal donation placeholder.
- "Поддержать"/"Donate" opens the owner's Binance Pay receive URL on first tap.
- The owner supplied a Binance Pay QR that encodes: https://app.binance.com/uni-qr/Jv3MYVZ8
- Support link is also visible and clickable in the About page.
- Do not initiate payments in-app; payer must review and confirm in Binance.
- Version 0.5.4 / 276.
""", encoding="utf-8")
print("LumiDrive v0.5.4 Binance Pay support URL installed.")

# LumiDrive 0.5.5: Keep Yandex Maps in our web browser instead of following
# Yandex's native-app deep links. The browser must keep its normal HTTP(S)
# loading and Youtube routing behavior unchanged.
web_client = "modules/web/src/main/java/me/aap/fermata/addon/web/FermataWebClient.java"
replace_exact(
    web_client,
    "\t\tif (isYoutubeUri(request.getUrl())) {",
    "\t\t// Yandex Maps may redirect mobile WebViews to its native app using\n"
    "\t\t// intent://maps.yandex.ru/... or yandexmaps://. Consume only those\n"
    "\t\t// navigations so the current https:// maps page remains visible.\n"
    "\t\tif (shouldStayOnYandexMapsWebsite(request.getUrl())) return true;\n"
    "\t\tif (isYoutubeUri(request.getUrl())) {",
)
replace_exact(
    web_client,
    "\tpublic static boolean isYoutubeUri(Uri uri) {",
    """\tprivate static boolean shouldStayOnYandexMapsWebsite(Uri uri) {
        String scheme = uri.getScheme();
        if ("yandexmaps".equalsIgnoreCase(scheme)) return true;
        if (!"intent".equalsIgnoreCase(scheme)) return false;

        String host = uri.getHost();
        return ("maps.yandex.ru".equalsIgnoreCase(host) ||
                "maps.yandex.com".equalsIgnoreCase(host));
    }

    public static boolean isYoutubeUri(Uri uri) {""",
)
web_source = (root / web_client).read_text(encoding="utf-8")
if web_source.count("shouldStayOnYandexMapsWebsite(request.getUrl())") != 1:
    raise SystemExit("Yandex Maps WebView override missing or duplicated")
if "if (isYoutubeUri(request.getUrl())) {" not in web_source:
    raise SystemExit("YouTube browser routing must remain intact")

changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.5.5 Yandex Maps website
- WebView ignores native Yandex Maps deep links (intent://maps.yandex.ru
  or yandexmaps://) rather than attempting to navigate to unsupported schemes.
- The current https:// Yandex Maps page stays inside LumiDrive.
- No external Yandex Maps app is launched, and no media or AA code is changed.
- Version 0.5.5 / 277.
""", encoding="utf-8")
print("LumiDrive 0.5.5 targeted Yandex Maps WebView fix applied.")


# LumiDrive 0.5.6 — prevent Android Auto transport auto-resume on connection.
# The AA host often issues an unsolicited MediaSession onPlay() shortly after
# connecting. In unmodified Fermata this falls back to getLastPlayedItem(),
# which can launch a saved live IPTV channel. Don't delete last-played history.
# Route actual user actions (tap, chosen channel or notification play) around
# this gate; the car service resets it on disconnect.
callback_path = "fermata/src/main/java/me/aap/fermata/media/service/MediaSessionCallback.java"
replace_exact(
    callback_path,
    "\tprivate boolean playOnPrepared;",
    """\tprivate boolean playOnPrepared;
    // Only protects the Android Auto app variant during a car connection.
    private volatile boolean blockAutomaticCarResume;
    private volatile boolean carPlaybackExplicitlyStarted;

    public void beginCarSessionWithoutAutoplay() {
        if (!BuildConfig.AUTO) return;
        carPlaybackExplicitlyStarted = false;
        blockAutomaticCarResume = true;
        // If the AA host already started playback before this car activity
        // connected, silence it; non-pausable live streams are stopped by onPause().
        if (isPlaying()) onPause();
    }

    public void preventUnrequestedCarResume() {
        if (!BuildConfig.AUTO || carPlaybackExplicitlyStarted) return;
        blockAutomaticCarResume = true;
        if (isPlaying()) onPause();
    }

    public void allowExplicitCarPlayback() {
        blockAutomaticCarResume = false;
        carPlaybackExplicitlyStarted = true;
    }

    public void endCarSession() {
        blockAutomaticCarResume = false;
        carPlaybackExplicitlyStarted = false;
    }
""",
)
replace_exact(
    callback_path,
    "\t@Override\n\tpublic void onPlay() {\n\t\tplayerTask.cancel();",
    """\t@Override
    public void onPlay() {
        // Ignore automatic resume commands while AA is first connecting.
        // Deliberate actions in LumiDrive call allowExplicitCarPlayback().
        if (BuildConfig.AUTO && blockAutomaticCarResume) {
            Log.i("LumiDrive: ignored unsolicited Android Auto Play request");
            return;
        }
        playerTask.cancel();""",
)
replace_exact(
    callback_path,
    "\t@Override\n\tpublic void onPlayFromMediaId(String mediaId, Bundle extras) {\n\t\tplayerTask.cancel();",
    """\t@Override
    public void onPlayFromMediaId(String mediaId, Bundle extras) {
        // An item chosen explicitly from the AA library is a user action.
        allowExplicitCarPlayback();
        playerTask.cancel();""",
)
# The on-screen phone/AA player controls call onPlay() directly through this
# binder. Whitelist them without whitelisting the AA host's unsolicited onPlay.
uibinder_path = "fermata/src/main/java/me/aap/fermata/media/service/FermataServiceUiBinder.java"
replace_exact(
    uibinder_path,
    "\tpublic void playItem(PlayableItem i, long pos) {\n\t\tif (i.equals(getCurrentItem())",
    "\tpublic void playItem(PlayableItem i, long pos) {\n"
    "\t\tsessionCallback.allowExplicitCarPlayback();\n"
    "\t\tif (i.equals(getCurrentItem())",
)
replace_exact(
    uibinder_path,
    "\t\t\tif (isPlaying()) getMediaSessionCallback().onPause();\n"
    "\t\t\telse getMediaSessionCallback().onPlay();",
    "\t\t\tif (isPlaying()) getMediaSessionCallback().onPause();\n"
    "\t\t\telse {\n"
    "\t\t\t\tgetMediaSessionCallback().allowExplicitCarPlayback();\n"
    "\t\t\t\tgetMediaSessionCallback().onPlay();\n"
    "\t\t\t}",
)
replace_exact(
    uibinder_path,
    "\t\t} else {\n\t\t\tmediaController.getTransportControls().play();\n\t\t}\n\t\treturn true;",
    "\t\t} else {\n"
    "\t\t\tgetMediaSessionCallback().allowExplicitCarPlayback();\n"
    "\t\t\tmediaController.getTransportControls().play();\n"
    "\t\t}\n\t\treturn true;",
)
# AA connects to the MediaBrowserService before (or instead of) launching
# the activity in some vehicles. Arm the gate before the media host issues Play.
service_path = "fermata/src/main/java/me/aap/fermata/media/service/FermataMediaService.java"
replace_exact(
    service_path,
    "\tpublic IBinder onBind(Intent intent) {\n\t\tif (BuildConfig.D || !intent.hasExtra(INTENT_ATTR_NOTIF_COLOR)) {",
    "\tpublic IBinder onBind(Intent intent) {\n"
    "\t\tif (BuildConfig.AUTO && !ACTION_MEDIA_SERVICE.equals(intent.getAction())) {\n"
    "\t\t\tcallback.preventUnrequestedCarResume();\n"
    "\t\t}\n"
    "\t\tif (BuildConfig.D || !intent.hasExtra(INTENT_ATTR_NOTIF_COLOR)) {",
)
# A tap on the app's Play action in the media notification is explicit.
replace_exact(
    service_path,
    "\t\t\t\t\tcase INTENT_PLAY -> callback.onPlay();",
    "\t\t\t\t\tcase INTENT_PLAY -> {\n"
    "\t\t\t\t\t\tcallback.allowExplicitCarPlayback();\n"
    "\t\t\t\t\t\tcallback.onPlay();\n"
    "\t\t\t\t\t}",
)
# Car UI attachment can occur without a MediaBrowserService bind, so arm it
# here as well. The phone activity is unaffected.
car_activity_path = "fermata/src/auto/java/me/aap/fermata/auto/MainCarActivity.java"
replace_exact(
    car_activity_path,
    "\tprivate MainActivityDelegate onCreate(Bundle state, FermataMediaServiceConnection s) {\n"
    "\t\tMainActivityDelegate d = new MainActivityDelegate(this, s.createBinder());",
    "\tprivate MainActivityDelegate onCreate(Bundle state, FermataMediaServiceConnection s) {\n"
    "\t\ts.getMediaSessionCallback().beginCarSessionWithoutAutoplay();\n"
    "\t\tMainActivityDelegate d = new MainActivityDelegate(this, s.createBinder());",
)
car_service_path = "fermata/src/auto/java/me/aap/fermata/auto/CarService.java"
replace_exact(
    car_service_path,
    "\t\tif ((cb != null) && cb.isPlaying()) cb.onPause();\n"
    "\t\ts.disconnect();",
    "\t\tif (cb != null) {\n"
    "\t\t\tif (cb.isPlaying()) cb.onPause();\n"
    "\t\t\tcb.endCarSession();\n"
    "\t\t}\n"
    "\t\ts.disconnect();",
)

# Guard against accidentally restoring auto-resume or affecting the phone UI.
cb_content = (root / callback_path).read_text(encoding="utf-8")
if cb_content.count("if (BuildConfig.AUTO && blockAutomaticCarResume)") != 1:
    raise SystemExit("AA autoplay guard missing or duplicated")
if cb_content.count("allowExplicitCarPlayback();") != 1:
    raise SystemExit("AA explicit-selection handler missing")
car_content = (root / car_activity_path).read_text(encoding="utf-8")
if car_content.count("beginCarSessionWithoutAutoplay();") != 1:
    raise SystemExit("AA car session startup guard missing")

changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.5.6 Android Auto autoplay suppression
- Suppress unsolicited media-session Play sent on initial Android Auto attach.
- Preserve the last IPTV channel and viewing history; don't delete saved media.
- Keep explicit channel selection, play/pause UI and notification Play functional.
- Reset guard on car disconnect. Phone media playback remains unchanged.
- AA's external transport Play commands are intentionally ignored while the
  guard is active; interact with LumiDrive's controls/select media to unlock.
- Version 0.5.6 / 278.
""", encoding="utf-8")
print("LumiDrive 0.5.6 Android Auto automatic resume suppression applied.")


# LumiDrive 0.5.7 — replace BOTH Android Auto mirror-service icons.
# Fermata defines mirror/mirror_fs in src/auto and separate API-26 adaptive
# icons; earlier LumiDrive branding changed only launcher/media_service.
# Rebrand drawable resources without modifying MirrorService/MirrorServiceFS.
write_xml("fermata/src/auto/res/drawable/lumidrive_mirror_mark.xml", """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <!-- Cyan monitor and stand with a purple bezel. -->
    <path android:fillColor="#AE8AFF"
        android:pathData="M21,27 H87 V76 H21 Z"/>
    <path android:fillColor="#27153D"
        android:pathData="M27,33 H81 V70 H27 Z"/>
    <path android:fillColor="#8FE7FF"
        android:pathData="M49,76 H59 V83 H49 Z M38,83 H70 V88 H38 Z"/>
    <!-- LumiDrive L and play triangle, matching the application palette. -->
    <path android:fillColor="#8FE7FF"
        android:pathData="M35,41 H41 V61 H49 V66 H35 Z"/>
    <path android:fillColor="#FF7AC8"
        android:pathData="M57,42 L74,53 L57,64 Z"/>
</vector>
""")
write_xml("fermata/src/auto/res/drawable/lumidrive_mirror_fs_mark.xml", """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <!-- Fullscreen mirror: four bright corners and central LumiDrive mark. -->
    <path android:fillColor="#AE8AFF"
        android:pathData="M22,22 H86 V86 H22 Z"/>
    <path android:fillColor="#27153D"
        android:pathData="M29,29 H79 V79 H29 Z"/>
    <path android:fillColor="#8FE7FF"
        android:pathData="M32,35 H45 V40 H37 V48 H32 Z M63,35 H76 V48 H71 V40 H63 Z M32,60 H37 V69 H45 V74 H32 Z M71,60 H76 V74 H63 V69 H71 Z"/>
    <path android:fillColor="#8FE7FF"
        android:pathData="M42,45 H48 V61 H55 V66 H42 Z"/>
    <path android:fillColor="#FF7AC8"
        android:pathData="M57,44 L70,55 L57,65 Z"/>
</vector>
""")
write_xml("fermata/src/auto/res/drawable/mirror.xml", """<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@drawable/lumidrive_background"/>
    <item android:drawable="@drawable/lumidrive_mirror_mark"/>
</layer-list>
""")
write_xml("fermata/src/auto/res/drawable/mirror_fs.xml", """<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@drawable/lumidrive_background"/>
    <item android:drawable="@drawable/lumidrive_mirror_fs_mark"/>
</layer-list>
""")
write_xml("fermata/src/auto/res/drawable-anydpi-v26/mirror.xml", """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/lumidrive_background"/>
    <foreground android:drawable="@drawable/lumidrive_mirror_mark"/>
    <monochrome android:drawable="@drawable/lumidrive_monochrome"/>
</adaptive-icon>
""")
write_xml("fermata/src/auto/res/drawable-anydpi-v26/mirror_fs.xml", """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/lumidrive_background"/>
    <foreground android:drawable="@drawable/lumidrive_mirror_fs_mark"/>
    <monochrome android:drawable="@drawable/lumidrive_monochrome"/>
</adaptive-icon>
""")

manifest = (root / "fermata/src/auto/AndroidManifest.xml").read_text(encoding="utf-8")
if manifest.count('android:icon="@drawable/mirror"') != 1 or manifest.count('android:icon="@drawable/mirror_fs"') != 1:
    raise SystemExit("Mirror service manifest icons changed upstream; inspect before release")
for marker in ("mirror.xml", "mirror_fs.xml"):
    for directory in ("drawable", "drawable-anydpi-v26"):
        target = root / "fermata/src/auto/res" / directory / marker
        if "lumidrive_" not in target.read_text(encoding="utf-8"):
            raise SystemExit(f"Missing branded icon: {target}")

# Update assistive description to reflect branded mirror service name; leave
# upstream copyright/license attribution elsewhere completely untouched.
for path in (root / "fermata/src/main/res").glob("values*/strings.xml"):
    original = path.read_text(encoding="utf-8")
    revised = original.replace("Fermata Mirror", "LumiDrive Mirror")
    if revised != original:
        path.write_text(revised, encoding="utf-8")

changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.5.7 Android Auto mirror-service icons
- Both 'LumiDrive Mirror' and 'LumiDrive FS Mirror' now use LumiDrive
  cyan/violet/pink artwork instead of upstream Fermata's mirror glyph.
- Covers legacy drawable and Android 8+ adaptive icons.
- Service manifest entries and mirroring behavior remain unchanged.
- Assistive descriptions refer to LumiDrive Mirror.
- Version 0.5.7 / 279.
""", encoding="utf-8")
print("LumiDrive 0.5.7 branded regular and fullscreen mirror icons applied.")


# LumiDrive Auto UI 1.0 (v0.6.0) — real Android Auto home screen.
# Reuse the existing car activity and media/player fragments; this is a
# removable overlay over the car's ConstraintLayout, not a new media engine.
auto_dashboard = Path(__file__).resolve().parent / "src" / "LumiDriveAutoHome.java"
if not auto_dashboard.is_file():
    raise SystemExit(f"Missing LumiDrive Auto Home source: {auto_dashboard}")
auto_dashboard_text = auto_dashboard.read_text(encoding="utf-8")
if "public final class LumiDriveAutoHome" not in auto_dashboard_text:
    raise SystemExit("Invalid Auto Home Java source")
(root / "fermata/src/main/java/me/aap/fermata/ui/activity/LumiDriveAutoHome.java").write_text(
    auto_dashboard_text, encoding="utf-8"
)

write_xml("fermata/src/main/res/values/lumidrive_auto.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="lumidrive_auto_home">LumiDrive Auto Home</string>
    <string name="lumidrive_auto_tagline">AUTO • MEDIA CENTER</string>
    <string name="lumidrive_auto_welcome">Welcome</string>
    <string name="lumidrive_auto_hint">Everything in one place</string>
    <string name="lumidrive_auto_iptv">IPTV</string>
    <string name="lumidrive_auto_youtube">YouTube</string>
    <string name="lumidrive_auto_browser">Browser</string>
    <string name="lumidrive_auto_library">Library</string>
    <string name="lumidrive_auto_channels">Live channels</string>
    <string name="lumidrive_auto_video">Video</string>
    <string name="lumidrive_auto_websites">Websites</string>
    <string name="lumidrive_auto_files">Media files</string>
    <string name="lumidrive_auto_favorites">★ Favorites</string>
    <string name="lumidrive_auto_settings">Settings</string>
    <string name="lumidrive_auto_parked">For passengers or while parked</string>
    <string name="lumidrive_auto_module_unavailable">This module is not installed</string>
</resources>
""")
write_xml("fermata/src/main/res/values-ru/lumidrive_auto.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="lumidrive_auto_home">Главная LumiDrive</string>
    <string name="lumidrive_auto_tagline">AUTO • МЕДИАЦЕНТР</string>
    <string name="lumidrive_auto_welcome">Добро пожаловать</string>
    <string name="lumidrive_auto_hint">Твои медиа в одном месте</string>
    <string name="lumidrive_auto_iptv">IPTV</string>
    <string name="lumidrive_auto_youtube">YouTube</string>
    <string name="lumidrive_auto_browser">Браузер</string>
    <string name="lumidrive_auto_library">Медиатека</string>
    <string name="lumidrive_auto_channels">Телеканалы</string>
    <string name="lumidrive_auto_video">Видео</string>
    <string name="lumidrive_auto_websites">Веб-сайты</string>
    <string name="lumidrive_auto_files">Файлы</string>
    <string name="lumidrive_auto_favorites">★ Избранное</string>
    <string name="lumidrive_auto_settings">Настройки</string>
    <string name="lumidrive_auto_parked">Для пассажира или на парковке</string>
    <string name="lumidrive_auto_module_unavailable">Этот модуль не установлен</string>
</resources>
""")

# Add Auto Home at car activity initialization, without changing lifecycle,
# permissions, playback or existing Android Auto service implementations.
replace_exact(
    car_activity_path,
    "import me.aap.fermata.ui.activity.MainActivityDelegate;",
    "import me.aap.fermata.ui.activity.MainActivityDelegate;\n"
    "import me.aap.fermata.ui.activity.LumiDriveAutoHome;",
)
replace_exact(
    car_activity_path,
    "\tprivate TextWatcher textWatcher;",
    "\tprivate TextWatcher textWatcher;\n"
    "\tprivate boolean lumiDriveHomeBackDown;",
)
replace_exact(
    car_activity_path,
    "\t\td.onActivityCreate(state);\n\t\treturn d;",
    "\t\td.onActivityCreate(state);\n"
    "\t\tView mainScreen = findViewById(R.id.main_activity);\n"
    "\t\tif (mainScreen != null) mainScreen.post(() -> LumiDriveAutoHome.show(d));\n"
    "\t\treturn d;",
)
replace_exact(
    car_activity_path,
    "\tpublic boolean onKeyDown(int keyCode, KeyEvent keyEvent) {\n"
    "\t\tLog.i(keyEvent);\n",
    "\tpublic boolean onKeyDown(int keyCode, KeyEvent keyEvent) {\n"
    "\t\tLog.i(keyEvent);\n"
    "\t\tif (keyCode == KEYCODE_BACK && LumiDriveAutoHome.hide(findViewById(R.id.main_activity))) {\n"
    "\t\t\tlumiDriveHomeBackDown = true;\n"
    "\t\t\treturn true;\n"
    "\t\t}\n",
)
replace_exact(
    car_activity_path,
    "\tpublic boolean onKeyUp(int keyCode, KeyEvent keyEvent) {\n"
    "\t\tLog.i(keyEvent);\n",
    "\tpublic boolean onKeyUp(int keyCode, KeyEvent keyEvent) {\n"
    "\t\tLog.i(keyEvent);\n"
    "\t\tif (keyCode == KEYCODE_BACK && lumiDriveHomeBackDown) {\n"
    "\t\t\tlumiDriveHomeBackDown = false;\n"
    "\t\t\treturn true;\n"
    "\t\t}\n",
)
# MainCarActivity uses a software D-pad cursor which searches children from
# first to last. While dashboard is visible, target its real overlay first,
# so taps never leak through into hidden video/toolbars underneath.
replace_exact(
    car_activity_path,
    "\t\t\tfloat y = getY();\n"
    "\t\t\tOverlayMenu m = activity.getActiveMenu();",
    "\t\t\tfloat y = getY();\n"
    "\t\t\tViewGroup root = screen();\n"
    "\t\t\tView home = root.findViewWithTag(LumiDriveAutoHome.HOME_TAG);\n"
    "\t\t\tif (home != null) {\n"
    "\t\t\t\ttouch(home, x - home.getX(), y - home.getY(), false);\n"
    "\t\t\t\treturn true;\n"
    "\t\t\t}\n"
    "\t\t\tOverlayMenu m = activity.getActiveMenu();",
)
replace_exact(
    car_activity_path,
    "\t\tpublic boolean onLongClick(View v) {\n"
    "\t\t\tdelayedHide();\n"
    "\t\t\tlongClick(screen(), getX(), getY());",
    "\t\tpublic boolean onLongClick(View v) {\n"
    "\t\t\tdelayedHide();\n"
    "\t\t\tif (LumiDriveAutoHome.isVisible(screen())) return true;\n"
    "\t\t\tlongClick(screen(), getX(), getY());",
)

# Existing "Home" navigation action was phone-only in 0.5.2. Extend it to
# the car, where it now opens a separate design. Keep mirror mode excluded.
nav_source = (root / nav_path).read_text(encoding="utf-8")
original_home_call = "LumiDriveDashboard.show(MainActivityDelegate.get(item.getContext()));"
if nav_source.count(original_home_call) != 2:
    raise SystemExit("Expected exactly two phone Home navigation handlers")
replace_exact(
    nav_path,
    "import me.aap.fermata.ui.activity.LumiDriveDashboard;",
    "import me.aap.fermata.ui.activity.LumiDriveDashboard;\n"
    "import me.aap.fermata.ui.activity.LumiDriveAutoHome;",
)
replace_exact(
    nav_path,
    "\t\t\t\t\tif (!MainActivityDelegate.get(ctx).getAppActivity().isCarActivity()\n"
    "\t\t\t\t\t\t\t&& !FermataApplication.get().isMirroringMode()) {",
    "\t\t\t\t\tif (!FermataApplication.get().isMirroringMode()) {",
)
replace_exact(
    nav_path,
    original_home_call,
    "LumiDriveAutoHome.showForCurrentActivity(MainActivityDelegate.get(item.getContext()));",
)

auto_class_path = root / "fermata/src/main/java/me/aap/fermata/ui/activity/LumiDriveAutoHome.java"
if not auto_class_path.exists():
    raise SystemExit("Missing new Auto Home Java class")
car_content = (root / car_activity_path).read_text(encoding="utf-8")
if car_content.count("LumiDriveAutoHome.show(d)") != 1:
    raise SystemExit("Car Activity missing Auto Home initialization")
if "touch(home, x - home.getX(), y - home.getY(), false);" not in car_content:
    raise SystemExit("Car D-pad cursor did not receive Home hit-test protection")
nav_content = (root / nav_path).read_text(encoding="utf-8")
if nav_content.count("LumiDriveAutoHome.showForCurrentActivity") != 2:
    raise SystemExit("Car Home overflow navigation handler missing or duplicated")

changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.6.0 LumiDrive Auto UI 1.0
- New branded dark-purple landscape car dashboard with IPTV, YouTube,
  Browser, Media Library, Favorites and Settings.
- Clickable large cards use existing fragment destinations, no engine rewrite.
- Android Auto CarActivity shows Home when opened; main phone and screen-mirroring
  activities retain their existing, independent UI.
- Bottom navigation 'Home' opens this dashboard from any regular car section.
- Software D-pad cursor targets this dashboard instead of underlying controls.
- Car Back dismisses Home safely without also processing the key-up event.
- No changes to playback logic, auto-resume guard, permissions or AA safety.
- Experimental preview v0.6.0 / versionCode 280.
""", encoding="utf-8")
print("LumiDrive Auto UI 1.0 home and car navigation enabled (v0.6.0).")

# LumiDrive 0.6.1: Verify author's requested spelling for the user-facing About text.
if about_en.count("Developer:</b> Sergey Vardanyan") != 1 or about_ru.count("Разработчик:</b> Sergey Vardanyan") != 1:
    raise SystemExit("Expected developer name 'Sergey Vardanyan' in both About templates")
if "Serge Vardanyan" in about_en or "Serge Vardanyan" in about_ru:
    raise SystemExit("Outdated developer spelling must not appear in About")

changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.6.1 developer name correction
- Developer/Разработчик in About is now spelled Sergey Vardanyan.
- Applies to English, Russian and fallback About templates for other locales.
- Previous media, UI, Mirror and Android Auto behavior is unchanged.
- Version 0.6.1 / 281.
""", encoding="utf-8")
print("LumiDrive v0.6.1 developer credit corrected to Sergey Vardanyan.")


# LumiDrive v0.7.0 — first-party in-app APK updates, using the proven Fermata
# download/dialog/installer implementation but ONLY our GitHub releases.
# Older LumiDrive versions intentionally blocked this path to avoid accidentally
# installing the ORIGINAL Fermata. We now explicitly pin our own releases.
main_java_path = "fermata/src/main/java/me/aap/fermata/ui/activity/MainActivity.java"
replace_exact(
    main_java_path,
    'public void checkUpdates() {\n\t\tif (getPackageName().startsWith("com.lumi.drive")) return;\n\t\tif (!BuildConfig.AUTO) return;',
    '''public void checkUpdates() {
        checkUpdates(false);
    }

    /** Check manually from Settings, or quietly at most daily at startup. */
    public void checkUpdates(boolean manual) {
        // Never try to update the separate debug/mobile package with an Auto APK.
        if (!"com.lumi.drive.auto".equals(getPackageName())) return;
        if (!BuildConfig.AUTO) return;''',
)
replace_exact(
    main_java_path,
    'String reqUrl = "https://api.github.com/repos/AndreyPavlenko/Fermata/releases/latest";',
    'String reqUrl = "https://api.github.com/repos/serge9900/LumiDrive-build/releases/latest";',
)
replace_exact(
    main_java_path,
    '''\t\t\t\t\tString tag = json.getString("tag_name");
\t\t\t\t\tString[] res = new String[2];
\t\t\t\t\tres[0] = tag;
\t\t\t\t\tint idx = tag.indexOf('(');
\t\t\t\t\tif (idx != -1) tag = tag.substring(0, idx);

\t\t\t\t\tif (NaturalOrderComparator.compareNatural(BuildConfig.VERSION_NAME, tag.trim()) < 0) {''',
    '''                    String tag = json.getString("tag_name").trim();
                    // Explicit versioned tags only: v0.7.0, v0.7.1, ...
                    if (!tag.matches("v[0-9]+\\\\.[0-9]+\\\\.[0-9]+")) {
                        Log.w("Ignoring unrecognized LumiDrive release tag: ", tag);
                        return completedNull();
                    }
                    String version = tag.substring(1);
                    String[] res = new String[3]; // version, APK URL, sha256 digest
                    res[0] = version;

                    if (NaturalOrderComparator.compareNatural(BuildConfig.VERSION_NAME, version) < 0) {''',
)
replace_exact(
    main_java_path,
    '''\t\t\t\t\t\tString ext = "armeabi".equals(Build.SUPPORTED_ABIS[0]) ? "-arm.apk" : "-arm64.apk";

\t\t\t\t\t\tfor (int i = 0, n = assets.length(); i < n; i++) {
\t\t\t\t\t\t\tJSONObject asset = assets.getJSONObject(i);
\t\t\t\t\t\t\tString name = asset.getString("name");
\t\t\t\t\t\t\tif (name.endsWith(ext)) res[1] = asset.getString("browser_download_url");
\t\t\t\t\t\t}''',
    '''                        String expectedName = "LumiDrive-" + tag + "-arm64.apk";
                        String expectedPrefix =
                                "https://github.com/serge9900/LumiDrive-build/releases/download/"
                                        + tag + "/";
                        for (int i = 0, n = assets.length(); i < n; i++) {
                            JSONObject asset = assets.getJSONObject(i);
                            if (!expectedName.equals(asset.optString("name"))) continue;
                            String download = asset.optString("browser_download_url", "");
                            // Refuse unrelated/misnamed/non-HTTPS artifacts.
                            if (!download.startsWith(expectedPrefix)) continue;
                            res[1] = download;
                            res[2] = asset.optString("digest", "");
                            break;
                        }''',
)
replace_exact(
    main_java_path,
    '''\t\t\t}).main().onSuccess(res -> {
\t\t\t\tif (res == null) return;
\t\t\t\tUiUtils.showQuestion(getContext(), getString(R.string.update),''',
    '''            }).main().onSuccess(res -> {
                if (res == null) {
                    if (manual) showAlert(this, getString(R.string.lumidrive_no_update));
                    return;
                }
                UiUtils.showQuestion(getContext(), getString(R.string.update),''',
)
replace_exact(
    main_java_path,
    '.onSuccess(r -> update(res[1], ps, deletePref));',
    '.onSuccess(r -> update(res[1], res[2], ps, deletePref));',
)
replace_exact(
    main_java_path,
    '''private FutureSupplier<Void> update(String uri, PreferenceStore ps,
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tPref<Supplier<String[]>> deletePref) {''',
    '''private FutureSupplier<Void> update(String uri, String sha256, PreferenceStore ps,
                                                        Pref<Supplier<String[]>> deletePref) {''',
)
replace_exact(
    main_java_path,
    '''\t\t\treturn d.download(uri, f).then(s -> {
\t\t\t\tUri u = (SDK_INT >= Build.VERSION_CODES.N) ?''',
    '''            return d.download(uri, f).then(s -> {
                // GitHub releases expose an optional SHA-256 asset digest.
                // Refuse an altered download before launching Android installer.
                try {
                    if (sha256 != null && sha256.startsWith("sha256:")
                            && !lumiDriveDigestMatches(f, sha256.substring(7))) {
                        //noinspection ResultOfMethodCallIgnored
                        f.delete();
                        App.get().run(() -> showAlert(this,
                                getString(R.string.lumidrive_update_bad_digest)));
                        return failed(new SecurityException("APK SHA-256 mismatch"));
                    }
                } catch (Exception ex) {
                    Log.e(ex, "Cannot verify LumiDrive update download");
                    return failed(ex);
                }
                Uri u = (SDK_INT >= Build.VERSION_CODES.N) ?''',
)
replace_exact(
    main_java_path,
    '\tprivate static File createTempFile(File dir) {',
    '''    private static boolean lumiDriveDigestMatches(File file, String expected)
            throws Exception {
        if (!expected.matches("[0-9a-fA-F]{64}")) return false;
        java.security.MessageDigest hash = java.security.MessageDigest.getInstance("SHA-256");
        try (java.io.FileInputStream input = new java.io.FileInputStream(file)) {
            byte[] block = new byte[65536];
            int count;
            while ((count = input.read(block)) != -1) {
                hash.update(block, 0, count);
            }
        }
        StringBuilder hex = new StringBuilder(64);
        for (byte part : hash.digest()) {
            hex.append(String.format(java.util.Locale.ROOT, "%02x", part & 0xff));
        }
        return expected.equalsIgnoreCase(hex.toString());
    }

    private static File createTempFile(File dir) {''',
)
# Existing automatic checks are already limited to once per 24 h by
# MainActivityPrefs.getCheckUpdatesPref(). Add a manual Settings button.
settings_path = "fermata/src/main/java/me/aap/fermata/ui/fragment/SettingsFragment.java"
replace_exact(
    settings_path,
    '''\t\t\t\to.pref = MainActivityPrefs.CHECK_UPDATES;
\t\t\t\to.title = R.string.check_updates;
\t\t\t});''',
    '''                o.pref = MainActivityPrefs.CHECK_UPDATES;
                o.title = R.string.check_updates;
            });
            if (a.getAppActivity() instanceof me.aap.fermata.ui.activity.MainActivity
                    && !a.isCarActivityNotMirror()) {
                sub1.addButton(o -> {
                    o.title = R.string.lumidrive_check_now;
                    o.onClick = () -> ((me.aap.fermata.ui.activity.MainActivity)
                            a.getAppActivity()).checkUpdates(true);
                });
            }''',
)
write_xml("fermata/src/main/res/values/lumidrive_updates.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="lumidrive_check_now">Check for LumiDrive updates now</string>
    <string name="lumidrive_no_update">No newer published LumiDrive update is available.</string>
    <string name="lumidrive_update_bad_digest">The downloaded update failed its integrity check and will not be installed.</string>
</resources>
""")
write_xml("fermata/src/main/res/values-ru/lumidrive_updates.xml", """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="lumidrive_check_now">Проверить обновления LumiDrive</string>
    <string name="lumidrive_no_update">Новых опубликованных обновлений LumiDrive пока нет.</string>
    <string name="lumidrive_update_bad_digest">Ошибка проверки загруженного обновления. Установка отменена.</string>
</resources>
""")
updated_main = (root / main_java_path).read_text(encoding="utf-8")
if "repos/AndreyPavlenko/Fermata/releases/latest" in updated_main:
    raise SystemExit("SECURITY: updater still points at upstream Fermata!")
if updated_main.count("repos/serge9900/LumiDrive-build/releases/latest") != 1:
    raise SystemExit("Wrong LumiDrive release API endpoint")
if updated_main.count("lumiDriveDigestMatches(f, sha256.substring(7))") != 1:
    raise SystemExit("Update checksum guard missing")
if updated_main.count('if (!"com.lumi.drive.auto".equals(getPackageName())) return;') != 1:
    raise SystemExit("LumiDrive Auto package safety gate missing")
updated_settings = (root / settings_path).read_text(encoding="utf-8")
if updated_settings.count("lumidrive_check_now") != 1:
    raise SystemExit("Manual update check is missing from Settings")

changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.7.0 first-party LumiDrive updates
- Re-enable the existing tested Android update prompt/downloader/installer,
  ONLY for the exact package com.lumi.drive.auto.
- Check the public latest stable release in serge9900/LumiDrive-build,
  never the original upstream Fermata release feed.
- Only accept exact version-tagged LumiDrive-vX.Y.Z-arm64.apk assets.
- Verify GitHub's SHA256 asset digest when present before install.
- Preserve the 24-hour automatic check interval, user-controlled toggle,
  system installation confirmation and update cache deletion.
- Add manual "Check for LumiDrive updates" action under phone Settings.
- No checks/prompts while in CarActivity; Android Auto and Mirror unchanged.
- Next releases must be published as GitHub Releases with signed APK assets.
- Version 0.7.0 / versionCode 282.
""", encoding="utf-8")
print("LumiDrive 0.7.0 first-party GitHub Releases updater enabled.")


# Manual update checks should explain network/API errors (including GitHub
# returning 404 before the first published release) rather than seem inert.
replace_exact(
    main_java_path,
    '''\t\t\tif (err != null) {
\t\t\t\tLog.e(err, "Failed to check updates");
\t\t\t\treturn failed(err);''',
    '''            if (err != null) {
                Log.e(err, "Failed to check updates");
                if (manual) App.get().run(() -> showAlert(this,
                        getString(R.string.lumidrive_update_check_failed)));
                return failed(err);''',
)
replace_exact(
    main_java_path,
    '''\t\t\t\t} catch (Exception ex) {
\t\t\t\t\tLog.e(ex, "Failed to parse response");
\t\t\t\t\treturn failed(ex);''',
    '''                } catch (Exception ex) {
                    Log.e(ex, "Failed to parse response");
                    if (manual) App.get().run(() -> showAlert(this,
                            getString(R.string.lumidrive_update_check_failed)));
                    return failed(ex);''',
)
for locale, text_label in (
    ("values", "Update check failed. Check your internet connection or whether a GitHub Release has been published."),
    ("values-ru", "Не удалось проверить обновления. Проверь интернет и наличие опубликованного GitHub Release."),
):
    p = root / "fermata/src/main/res" / locale / "lumidrive_updates.xml"
    current = p.read_text(encoding="utf-8")
    addition = '    <string name="lumidrive_update_check_failed">' + text_label + '</string>\n'
    if current.count("</resources>") != 1:
        raise SystemExit("LumiDrive updates resources invalid")
    updated = current.replace("</resources>", addition + "</resources>")
    ET.fromstring(updated)
    p.write_text(updated, encoding="utf-8")
print("Manual LumiDrive update checks now report GitHub/network failure.")


# LumiDrive v0.7.1 — published-release lookup and native log viewer.
# GitHub returns HTTP 404 for /releases/latest until a Release exists. Listing
# /releases returns HTTP 200 with [] instead. Preserve the vetted v0.7.0
# release APK filename, package name, SHA-256 verification, and installer.
replace_exact(
    main_java_path,
    'String reqUrl = "https://api.github.com/repos/serge9900/LumiDrive-build/releases/latest";',
    'String reqUrl = "https://api.github.com/repos/serge9900/LumiDrive-build/releases?per_page=20";',
)
replace_exact(
    main_java_path,
    'JSONObject json = new JSONObject(TextUtils.toString(p, UTF_8));',
    '''JSONArray releases = new JSONArray(TextUtils.toString(p, UTF_8));
                    JSONObject json = null;
                    for (int n = 0; n < releases.length(); n++) {
                        JSONObject candidate = releases.getJSONObject(n);
                        if (candidate.optBoolean("draft") || candidate.optBoolean("prerelease"))
                            continue;
                        json = candidate;
                        break;
                    }
                    // No published stable Release is normal, not a network error.
                    if (json == null) return completedNull();''',
)
replace_exact(
    main_java_path,
    'if (manual) showAlert(this, getString(R.string.lumidrive_no_update));',
    '''if (manual) {
                        new androidx.appcompat.app.AlertDialog.Builder(this)
                                .setTitle(R.string.update)
                                .setMessage(R.string.lumidrive_no_update)
                                .setPositiveButton(android.R.string.ok, null)
                                .setNeutralButton(R.string.lumidrive_open_builds,
                                        (dialog, which) -> startActivity(new Intent(
                                                Intent.ACTION_VIEW,
                                                Uri.parse("https://github.com/serge9900/LumiDrive-build/actions"))))
                                .show();
                    }''',
)
# New log filename is returned to AndroidLogger and the share FileProvider, so
# it also updates the share-sheet name. Migrate old history on first run.
application_path = "fermata/src/main/java/me/aap/fermata/FermataApplication.java"
replace_exact(
    application_path,
    'return new File(dir, "Fermata.log");',
    '''File lumiLog = new File(dir, "LumiDrive.log");
        File oldLog = new File(dir, "Fermata.log");
        if (!lumiLog.exists() && oldLog.isFile()) {
            // Best effort: preserve log history from earlier LumiDrive builds.
            if (!oldLog.renameTo(lumiLog)) {
                Log.w("Could not rename old Fermata.log to LumiDrive.log");
            }
        }
        return lumiLog;''',
)
# Previous "Open log" only opened an ACTION_SEND share chooser. A user wanting
# to VIEW the logs should be able to inspect them in LumiDrive first, and share
# the correct LumiDrive.log filename if troubleshooting requires it.
replace_exact(
    settings_path,
    '''\tprivate void openLog(MainActivityDelegate a) {
\t\ttry {
\t\t\tvar i = new Intent(Intent.ACTION_SEND);
\t\t\tvar app = FermataApplication.get();
\t\t\tvar f = app.getLogFile();
\t\t\tUri u = (SDK_INT >= Build.VERSION_CODES.N) ?
\t\t\t\t\tFileProvider.getUriForFile(app, app.getPackageName() + ".FileProvider", f) :
\t\t\t\t\tUri.fromFile(f);
\t\t\ti.setType("text/plain");
\t\t\ti.putExtra(Intent.EXTRA_STREAM, u);
\t\t\ta.startActivity(Intent.createChooser(i, app.getString(R.string.open_log)));
\t\t} catch (Exception err) {
\t\t\tLog.e(err);
\t\t\tshowAlert(a.getContext(), err.getLocalizedMessage());
\t\t}
\t}''',
    '''\tprivate void openLog(MainActivityDelegate a) {
        try {
            File file = FermataApplication.get().getLogFile();
            String content;
            if (!file.isFile() || file.length() == 0) {
                content = getString(R.string.lumidrive_log_empty);
            } else {
                // Keep the viewer responsive even when the log is large.
                int length = (int) Math.min(24000L, file.length());
                byte[] bytes = new byte[length];
                try (java.io.RandomAccessFile input =
                             new java.io.RandomAccessFile(file, "r")) {
                    input.seek(input.length() - length);
                    input.readFully(bytes);
                }
                content = (file.length() > length
                        ? getString(R.string.lumidrive_log_truncated) + "\\n\\n" : "")
                        + new String(bytes, UTF_8);
            }
            a.createDialogBuilder()
                    .setTitle("LumiDrive.log")
                    .setMessage(content)
                    .setNeutralButton(R.string.lumidrive_share_log,
                            (dialog, which) -> shareLumiDriveLog(a))
                    .setPositiveButton(android.R.string.ok, null)
                    .show();
        } catch (Exception err) {
            Log.e(err, "Failed to view LumiDrive log");
            showAlert(a.getContext(), err.getLocalizedMessage());
        }
    }

    private void shareLumiDriveLog(MainActivityDelegate a) {
        try {
            FermataApplication app = FermataApplication.get();
            File file = app.getLogFile();
            if (!file.isFile()) {
                showAlert(a.getContext(), getString(R.string.lumidrive_log_empty));
                return;
            }
            Uri uri = (SDK_INT >= Build.VERSION_CODES.N)
                    ? FileProvider.getUriForFile(
                            app, app.getPackageName() + ".FileProvider", file)
                    : Uri.fromFile(file);
            Intent intent = new Intent(Intent.ACTION_SEND);
            intent.setType("text/plain");
            intent.putExtra(Intent.EXTRA_STREAM, uri);
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            a.startActivity(Intent.createChooser(intent,
                    getString(R.string.lumidrive_share_log)));
        } catch (Exception err) {
            Log.e(err, "Failed to share LumiDrive log");
            showAlert(a.getContext(), err.getLocalizedMessage());
        }
    }''',
)
# Use localized feedback. The absence of any releases is not a connection
# failure, and the still-experimental APKs live under GitHub Actions.
for locale, messages in (
    ("values", {
        "lumidrive_no_update": "No newer published LumiDrive release is available yet. Test APK builds are available on GitHub Actions.",
        "lumidrive_update_check_failed": "Could not contact GitHub to check for updates. Please check your connection and try again."
    }),
    ("values-ru", {
        "lumidrive_no_update": "Новых опубликованных релизов LumiDrive пока нет. Тестовые APK доступны в GitHub Actions.",
        "lumidrive_update_check_failed": "Не удалось связаться с GitHub для проверки обновлений. Проверь интернет и попробуй снова."
    })
):
    resources = root / "fermata/src/main/res" / locale / "lumidrive_updates.xml"
    xml = resources.read_text(encoding="utf-8")
    for string_name, label in messages.items():
        xml, count = re.subn(
            r'(<string name="' + re.escape(string_name) + r'">).*?(</string>)',
            lambda m: m.group(1) + label + m.group(2),
            xml,
            count=1
        )
        if count != 1:
            raise SystemExit(f"Missing existing update label: {locale}/{string_name}")
    added = """    <string name="lumidrive_open_builds">Open APK builds</string>
    <string name="lumidrive_log_empty">No log entries yet.</string>
    <string name="lumidrive_log_truncated">Showing the latest 24 KB of the log.</string>
    <string name="lumidrive_share_log">Share LumiDrive.log</string>
""" if locale == "values" else """    <string name="lumidrive_open_builds">Открыть сборки APK</string>
    <string name="lumidrive_log_empty">Записей в журнале пока нет.</string>
    <string name="lumidrive_log_truncated">Показаны последние 24 КБ журнала.</string>
    <string name="lumidrive_share_log">Поделиться LumiDrive.log</string>
"""
    if xml.count("</resources>") != 1: raise SystemExit("Invalid update resource file")
    xml = xml.replace("</resources>", added + "</resources>")
    ET.fromstring(xml)
    resources.write_text(xml, encoding="utf-8")

for locale, before, after in (
    ("values", '<string name="open_log">Open log file</string>',
               '<string name="open_log">View LumiDrive log</string>'),
    ("values-ru", '<string name="open_log">Открыть лог файл</string>',
                  '<string name="open_log">Просмотреть журнал LumiDrive</string>')
):
    xml_path = root / "fermata/src/main/res" / locale / "strings.xml"
    xml = xml_path.read_text(encoding="utf-8")
    if xml.count(before) != 1: raise SystemExit(f"Open-log label changed in {locale}")
    xml = xml.replace(before, after)
    ET.fromstring(xml)
    xml_path.write_text(xml, encoding="utf-8")

# Regression guards: original Auto playback/YouTube/IPTV code remains untouched;
# the official Release APK security validation from 0.7.0 must stay in place.
checked_main = (root / main_java_path).read_text(encoding="utf-8")
if checked_main.count("LumiDrive-build/releases?per_page=20") != 1:
    raise SystemExit("LumiDrive updates must use a 200-safe Releases listing")
if "new JSONArray(TextUtils.toString(p, UTF_8))" not in checked_main:
    raise SystemExit("Expected a GitHub Releases array response")
if "lumiDriveDigestMatches(f, sha256.substring(7))" not in checked_main:
    raise SystemExit("SECURITY: SHA-256 integrity verification was removed")
if 'if (!"com.lumi.drive.auto".equals(getPackageName())) return;' not in checked_main:
    raise SystemExit("SECURITY: Auto-package guard was removed")
checked_app = (root / application_path).read_text(encoding="utf-8")
if 'return lumiLog;' not in checked_app or '"LumiDrive.log"' not in checked_app:
    raise SystemExit("Log rebranding failed")
checked_settings = (root / settings_path).read_text(encoding="utf-8")
if checked_settings.count("shareLumiDriveLog(a)") != 1:
    raise SystemExit("In-app log viewer missing Share action")

changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.7.1 settings maintenance
- GitHub Releases endpoint now uses the listing API; an empty response is
  treated as no published update instead of GitHub HTTP 404/network failure.
- Manual checks show a localized status dialog linking to experimental
  GitHub Actions APK builds when no stable release is available.
- Existing installer, package identity and SHA-256 validation are untouched.
- App logs are named LumiDrive.log, migrating the previous Fermata.log.
- The Settings "View log" action displays the latest 24 KB in an in-app dialog
  and offers a separate Share LumiDrive.log option.
- v0.7.1, versionCode 283; media/Android Auto behavior is unchanged.
""", encoding="utf-8")
print("LumiDrive v0.7.1 update-check and log-viewer fixes applied.")
