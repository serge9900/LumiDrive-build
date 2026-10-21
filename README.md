# LumiDrive — test APK builds

LumiDrive is an experimental Android multimedia application based on the open-source [Fermata Media Player](https://github.com/AndreyPavlenko/Fermata) by Andrey Pavlenko and contributors.

**Current status:** build pipeline for a first Android 16 test APK; no APK has been verified yet. It is intended for testing on a parked car and on the phone. Original Fermata remains a separate app.

**License:** GNU GPL version 3, as for the upstream project. This repository contains build orchestration and a branding patch. A build checks out the original source and applies those modifications; see workflow logs for the pinned tag. Before distributing a finished release, publish the complete corresponding modified source code and preserve upstream attribution and third-party notices.

**How to build:** Open the **Actions** tab, select **Build LumiDrive APK**, click **Run workflow**, and wait for the Android APK artifact. Building requires no local Android Studio.

**Note:** This build does not change Android Auto restrictions or guarantee compatibility with any particular head unit.
