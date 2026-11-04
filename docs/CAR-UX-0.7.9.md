# LumiDrive 0.7.9 — Android Auto usability beta

This is a **test build**, not a public stable GitHub Release. It changes only presentation and phone entry points.

## Android Auto home screen

- Replace the 4 dashboard icons with crisp 32dp vector art for IPTV, YouTube, Browser, and Library; Settings has a matching glyph.
- Compact 2×2 grid, smaller margins, accessible labels including each tile subtitle, and improved highlighted focus state for touch/rotary/D-pad.
- Focused cards gain a stronger border and subtle elevation/scale.
- Clarify that Spotify and Yandex Music are separate supported Android Auto media apps accessible from the **Android Auto app launcher**, not from unofficial intents inside LumiDrive.
- Browser card retains the explicit Google homepage.
- Keep current playback, Auto pause/resume protection, navigation, IPTV and all existing settings.

## Phone home screen

- Add Spotify and Yandex Music entry points below Favorites and Settings.
- Each entry launches the **installed third-party app**. If absent, it offers a choice to open the corresponding **official Google Play listing**.
- App icons use the genuine installed package icon; an original music-note fallback appears only when the app isn't installed.
- No access to account credentials, subscriptions, streams or listening data.

## Why not embed Spotify/Yandex streams in LumiDrive?

Android Auto normally restricts launching another app's activity directly on a head unit. Both services have their own Android Auto media apps and should be accessed from Android Auto's launcher.

Spotify's official App Remote SDK is a separate future integration path: it requires a registered Spotify developer application, explicit user authorization and a supported playback flow. This test does **not** embed Spotify's player or implement a Yandex Music streaming API.

## Safe test checklist

1. Install the **v0.7.9 beta APK** from GitHub Actions only after the build passes; don't uninstall the working v0.7.8.
2. Phone: tap **Spotify** and **Яндекс Музыка**, confirming each installed app opens; test one missing app if possible.
3. Car **parked**: verify all four tile destinations, larger focus highlights and Back/Home navigation.
4. Reconnect Android Auto: verify no unwanted IPTV autoplay.
5. Confirm web browser, IPTV, YouTube, media files, favorites and settings still work.
6. Spotify and Yandex Music should be selected using their own Android Auto launcher icons, not from LumiDrive's media screen.

**No new privacy permissions:** Manifest only adds package visibility for `com.spotify.music` and `ru.yandex.music`.

## Русский

Тестовая версия 0.7.9 улучшает главный экран **LumiDrive в автомобиле**: новые векторные иконки, более заметное выделение карточек и более компактное расположение элементов.

В **телефонной** версии добавлены ярлыки Spotify и Яндекс Музыки. Они запускают настоящие приложения, если установлены, или предлагают открыть официальные страницы Google Play.

**В Android Auto сами Spotify и Яндекс Музыка открываются через меню приложений Android Auto.** LumiDrive не пытается обойти ограничения Android Auto и не воспроизводит их защищённые потоки внутри себя.

Тестировать интерфейс машины нужно только в припаркованном автомобиле.

Based on Fermata Media Player (GPL‑3.0).