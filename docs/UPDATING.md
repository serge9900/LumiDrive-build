# LumiDrive updates · Система обновлений

## Quick overview / Кратко

Beginning with **LumiDrive v0.7.0 (versionCode 282)**, LumiDrive Auto checks the **latest published stable release** of this repository when the phone app is opened.

- **Automatic:** once every 24 hours, if enabled under Settings → Other → "Check for updates on startup".
- **Manual:** Settings → Other → **Check for LumiDrive updates now**.
- **On a new release:** a native dialog offers to download and install the update.
- **On agreement:** LumiDrive downloads the release APK, checks its SHA-256 digest when provided by GitHub, and launches Android's **system package installer**. Android requires installation approval, and may require "Allow from this source".
- **When up to date:** no automatic popup.
- No update dialogs on the Android Auto car screen or in Mirror mode.
- Only the exact `com.lumi.drive.auto` application and official `serge9900/LumiDrive-build` repository are eligible.

**Важно:** в установленной 0.6.1 и старее этой функции нет. Один раз установи 0.7.0 вручную поверх предыдущей версии. Тогда последующие релизы смогут загружаться через приложение.

## Why GitHub Releases, not Actions Artifacts?

Actions **Artifacts** are temporary CI ZIP archives, not stable public links and may require authentication.

The app queries:

`https://api.github.com/repos/serge9900/LumiDrive-build/releases/latest`

Only published **non-prerelease, non-draft** releases with tags `vMAJOR.MINOR.PATCH` are eligible. For tag `v0.7.1` attach an APK named **exactly** `LumiDrive-v0.7.1-arm64.apk` to the matching GitHub Release.

## Publishing an update / Как выпустить обновление

1. Change the app on a new branch, increasing BOTH `versionName` and `versionCode` in `apply_lumidrive.py` (example: `0.7.1`, `283`).
2. Confirm the [Build LumiDrive APK](../.github/workflows/build-lumidrive.yml) test succeeded. Install the preview APK and test on a phone and with Android Auto **while parked**.
3. Publish using a **version tag**, e.g. `v0.7.1`, pointing at the tested commit. On GitHub: **Releases → Draft a new release → Choose a tag → Create a new tag on the tested branch → Publish release**. Alternatively create and push the git tag locally.
4. The tag triggers [Publish LumiDrive APK update](../.github/workflows/publish-lumidrive.yml). This builds an APK from the tagged sources, verifies that the tag matches the embedded version, verifies the APK signature and integrity, and adds the APK plus SHA256SUMS.txt to the release.
5. LumiDrive checks that release on its next automatic check, or immediately via the Settings manual-check button. The user must accept both the app's update question and Android's system installation prompt.

**Важно:** a successful Actions build or a new branch alone is **not** a published update. It must have an APK attached to the public **GitHub Release**.

## Signing, compatibility and security / Безопасность

Android can replace an installed app only if package ID, signing certificate, and increasing versionCode are compatible.

Experimental CI builds currently inherit Fermata 2.0.2's **publicly distributed development signing key** (`res/fermata.jks`). This maintains compatibility for development testing but is **unsafe for general public distribution**, because that private signing key is publicly available.

Before production, generate and securely back up an OWNED private signing keystore. Do not upload keys/passwords to the source repository. Configure these repository **Actions Secrets**:

- `LUMIDRIVE_RELEASE_KEYSTORE_BASE64`
- `LUMIDRIVE_RELEASE_STORE_PASSWORD`
- `LUMIDRIVE_RELEASE_KEY_ALIAS`
- `LUMIDRIVE_RELEASE_KEY_PASSWORD`

The publish workflow can use that private key; otherwise it prints a security warning and uses the legacy test key.

**Changing the signing key means a one-time reinstall is required for previously installed preview versions.** Back up your IPTV playlists/settings before that migration. Keep the new release signing key safe forever.

GitHub Releases delivers the APK via HTTPS; a SHA-256 digest is verified when present; Android independently verifies package signatures and asks for user approval. There is no silent install.

## Limitations

- This implementation targets the Android Auto **arm64 universal APK**.
- The update dialog requires the phone app to be opened, not merely the car connecting.
- No published release yet means no available update.
- A failed network check or a missing APK can be retried manually.
- Android's unknown-app-source permission may be needed. OEM restrictions apply.
- Android Auto driver-distraction restrictions are unchanged.
- Keep copyright notices and the GPL-3.0 source obligations when distributing binaries.

Developer: **Sergey Vardanyan**.
