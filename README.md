# LumiDrive — Android multimedia project

**LumiDrive v0.3 (experimental)** is an Android multimedia app based on the open-source
[Fermata Media Player](https://github.com/AndreyPavlenko/Fermata) by Andrey Pavlenko and contributors.

## LumiDrive design — v0.3

- Dark purple background and panels
- Rounded playback, toolbar and navigation buttons
- Pink, violet and cyan accent colors
- New main launcher and Android Auto media icons (including Android 16 adaptive icon)
- Existing IPTV, Browser and YouTube code retained
- Application ID: `com.lumi.drive.auto`
- Version code: `269` (install update over v0.2)
- Android Auto functionality **not yet verified** for LumiDrive; original Fermata can remain installed

## Build APK without Android Studio

1. Go to **Actions → Build LumiDrive APK → Run workflow** on the `main` branch.
2. Wait for the workflow to complete successfully.
3. Open the completed run's **Summary** and download artifact `LumiDrive-v0.3-APK-arm64`.
4. Extract `LumiDrive-v0.3-arm64.apk` and install on an arm64 Android phone.
5. Test on phone first, then on a parked vehicle with a passenger-operated interface.

This build runs a **pinned Fermata 2.0.2** checkout and applies
[`apply_lumidrive.py`](./apply_lumidrive.py) to the checked-out sources.
The repository contains the build script and all project-specific modifications, not a
pre-verified APK.

**Troubleshooting**: If the build fails, open the red job and share the failing Gradle step.
If an update fails due to signing, do not uninstall your working Fermata. Our app has a
different package ID. Check the package/signature of the LumiDrive test app first.

## Open-source license and attribution

GPL-3.0, consistent with Fermata. Preserve the original copyright notices and provide
complete corresponding source code and modifications with public binary distributions.
Third-party components (including the Android Auto AAR) still require license review
before publishing LumiDrive as a public release.

**Important**: A successful build or install does not guarantee compatibility with
a specific Android Auto host, and does not remove platform restrictions.
