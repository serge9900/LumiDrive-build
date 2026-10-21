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
