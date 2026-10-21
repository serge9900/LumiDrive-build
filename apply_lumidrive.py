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
    original_catalog.replace('appVersionCode = "268"', 'appVersionCode = "269"')
                    .replace('appVersionName = "2.0.2"', 'appVersionName = "0.3.0"'),
    encoding="utf-8",
)

changes = root / "LUMIDRIVE_CHANGES.md"
changes.write_text(changes.read_text(encoding="utf-8") + """
## v0.3 visual refresh
- Purple, pink and cyan dark themes for phone and Android Auto.
- Rounded toolbar, navigation, media and control-panel buttons.
- Replaced phone launcher, adaptive icon and Android Auto media icon.
- Default phone theme is now LumiDrive Purple; AA theme uses matching Dark palette.
- Package remains com.lumi.drive.auto; versionCode increased to 269.
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

# v0.4 navigation prototype: show real module routes on long-press of toolbar.
# The regular toolbar tap behavior remains unchanged.
write_xml_path = root / "fermata/src/main/java/me/aap/fermata/ui/activity/LumiDriveDashboard.java"
write_xml_path.write_text("package me.aap.fermata.ui.activity;\n\nimport android.app.AlertDialog;\nimport android.content.Context;\nimport me.aap.fermata.BuildConfig;\nimport me.aap.fermata.R;\nimport me.aap.fermata.addon.AddonInfo;\nimport me.aap.fermata.addon.AddonManager;\nimport me.aap.fermata.addon.FermataAddon;\nimport me.aap.fermata.addon.FermataFragmentAddon;\n\n/**\n * Experimental LumiDrive navigation entry point. Reuses the original fragment\n * handlers; unavailable optional addons are never replaced by fake screens.\n */\npublic final class LumiDriveDashboard {\n    private LumiDriveDashboard() {}\n\n    public static void show(MainActivityDelegate activity) {\n        Context context = activity.getContext();\n        String[] entries = {\"IPTV\", \"YouTube\", \"Browser\", \"Library\", \"Favorites\", \"Settings\"};\n        new AlertDialog.Builder(context)\n                .setTitle(\"LumiDrive\")\n                .setItems(entries, (dialog, selected) -> {\n                    switch (selected) {\n                        case 0: openAddon(activity, \"iptv\"); break;\n                        case 1: openAddon(activity, \"youtube\"); break;\n                        case 2: openAddon(activity, \"browser\"); break;\n                        case 3: activity.showFragment(R.id.folders_fragment); break;\n                        case 4: activity.showFragment(R.id.favorites_fragment); break;\n                        case 5: activity.showFragment(R.id.settings_fragment); break;\n                        default: break;\n                    }\n                }).show();\n    }\n\n    private static void openAddon(MainActivityDelegate activity, String key) {\n        AddonManager manager = AddonManager.get();\n        for (AddonInfo info : BuildConfig.ADDONS) {\n            if (!info.className.toLowerCase(java.util.Locale.ROOT).contains(key)) continue;\n            FermataAddon addon = manager.getAddon(info.className);\n            if (addon instanceof FermataFragmentAddon) {\n                activity.showFragment(((FermataFragmentAddon) addon).getFragmentId());\n                return;\n            }\n        }\n        new AlertDialog.Builder(activity.getContext())\n                .setMessage(\"This module is not available in the current build.\")\n                .setPositiveButton(android.R.string.ok, null).show();\n    }\n}\n", encoding="utf-8")
replace_exact(
    "fermata/src/main/java/me/aap/fermata/ui/activity/MainActivityDelegate.java",
    "toolBar = a.findViewById(R.id.tool_bar);",
    "toolBar = a.findViewById(R.id.tool_bar);\\n"
    "        if (!a.isCarActivity()) {\\n"
    "            toolBar.setOnLongClickListener(v -> {\\n"
    "                LumiDriveDashboard.show(this);\\n"
    "                return true;\\n"
    "            });\\n"
    "        }".replace("\\\\n", "\\n"),
)
print("LumiDrive dashboard navigation prototype installed.")
