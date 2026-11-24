# Vice Sunset (unreleased)

Third explicit appearance option alongside Classic and Light. Based on the exact
v0.8.0 source, with no version bump, release or installation. The new patch runs
after `apply_themes.py`; the original Classic/Light validator still runs first.

Choose **Settings → Interface → Theme → Vice Sunset**. Phone and Android Auto
retain separate preferences. Restart the Android Auto app after changing its
theme, as in 0.8.0. Stored theme IDs 0 and 1 retain their meanings; Vice uses 7,
leaving legacy IDs 2–6 on the existing Classic migration path.

The shared palette styles IPTV/media lists, browser/YouTube app controls,
settings, menus, dialogs and playback chrome. Web pages and video imagery retain
their own content colors. Phone and car dashboards use their own themed context.
The phone logo has a small pink/peach gradient; the car dashboard uses flat dark
surfaces without new animation. No third-party branding or artwork is included.

The IPTV screenshot shows the title immediately against the back button. The
shared title now reserves 8dp on both sides within its existing constrained,
single-line, ellipsized slot. Button actions, focus order and filter behavior are
unchanged. A physical-device check is still needed before claiming the reported
overlap is resolved at every screen width and scaling setting.

## Validation

Run the original patch pipeline and `tests/validate_themes.py`, followed by:

```
python3 apply_vice_sunset.py upstream
python3 tests/validate_vice_sunset.py upstream
```

The patch records hashes across the generated source tree to verify that only
the declared presentation files changed. The validator checks contrast across
normal and selected surfaces, theme mappings and legacy migration, title margins,
and the change scope. The existing three Java test suites run in CI along with
the Android Auto universal APK build. CI creates a test artifact only.

Before release, check all three themes on a phone in portrait/landscape, including
large fonts and toolbar scaling; IPTV root/group/channel views and filtering;
YouTube/browser controls; media selection; settings/dialogs; and Android Auto
touch/rotary focus. Verify switching back restores Classic/Light. Playback,
autostart, updates and LumiMirror receive no new functional changes.
