# LumiDrive 0.7.9 — Automotive UI beta

**Scope:** visual and usability refinements to LumiDrive’s own parked-car home screen only.

## Changes

- Five new original, vector-drawn icons: IPTV, YouTube, Browser, Library, Settings.
- More visible focus border and subtle scale/elevation to help D-pad / rotary navigation.
- Compact, touch-friendly 2×2 media dashboard and clearer accessible labels.
- The Browser tile opens the Google homepage.
- Existing IPTV, media player, YouTube, navigation, Android Auto transport and update safety checks remain unchanged.

## Explicit non-goals

- No external music service SDKs, player integrations, launch shortcuts, music logos, account authorizations or new package-visibility permissions.
- No new behavior on the phone home screen.
- No external application launch from Android Auto.
- The existing stable LumiDrive v0.7.8 is unchanged.

## How to test

1. Install the test APK from the green GitHub Actions run **on top of** installed LumiDrive, without uninstalling the stable version first.
2. On a **parked** car's Android Auto screen, open LumiDrive's home page and check the 4 new icons, focus borders and readability.
3. Check IPTV, YouTube, Browser, Library, Favorites, Settings, and Back/Home.
4. Disconnect and reconnect Android Auto: the last IPTV channel must not auto-play.
5. Check phone home and its existing features still behave exactly like v0.7.8.
6. Report screenshots or diagnostic logs before any public release.

Version 0.7.9 / build 291 is **experimental**. Based on Fermata Media Player under GPL-3.0.

---

## Русский

**LumiDrive 0.7.9** — тестовое улучшение нашего собственного интерфейса Android Auto.

- Пять новых векторных иконок.
- Удобнее управление фокусом и выделение выбранных карточек.
- Компактная сетка IPTV, YouTube, Браузер и Медиатека.
- Без новых интеграций, сторонних музыкальных сервисов и дополнительных разрешений.
- Телефонный интерфейс, IPTV, Android Auto и автообновление оставлены как в версии 0.7.8.

Проверять только на припаркованной машине. Пока это тестовая сборка, не публичный Release.