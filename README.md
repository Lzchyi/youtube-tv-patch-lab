# YouTube TV Patch Lab

**Status: APKM investigation pipeline; no working playback-speed patch has been identified.**

Independent, non-commercial personal research into playback-speed availability on a personally owned Android TV.

## Disclaimer
This project is not affiliated with, endorsed by, or supported by Google, YouTube, Sony, or APKMirror. All trademarks belong to their owners. This repository does not host proprietary YouTube APKs or modified YouTube binaries. Personal-use intent does not itself confer rights to redistribute or modify copyrighted software. You are responsible for applicable law, terms, and device safety.

## Investigation workflow
The GitHub Actions workflow accepts an **authorised APKM file** through a short-lived HTTPS direct-download URL stored in repository Actions secret `APK_SOURCE_URL`. It downloads the file to the temporary runner, extracts `base.apk`, runs `aapt` and JADX, searches playback-speed-related references, and uploads only JSON/Markdown reports. **No patched APK is generated.**

1. Keep the repository private.
2. Place your APKM in temporary private file storage that provides a direct, expiring HTTPS download URL.
3. In repository Settings → Secrets and variables → Actions, create secret `APK_SOURCE_URL` containing that URL.
4. Run Actions → **Investigate YouTube TV APKM** → Run workflow.
5. Download the `youtube-tv-research` artifact and review it.
6. Delete/revoke the temporary download URL and repository secret after use.

**Security note:** Anyone who can edit the workflow can potentially access Actions secrets. Use only trusted collaborators. The APKM must not be committed. The source URL is not printed by the workflow, but the external file host will receive a download request.

## Local investigation (no upload needed)
Install Python 3.11+, JADX and Android SDK `aapt`, then run:

```bash
python3 scripts/analyze_bundle.py /path/to/youtube.apkm --output report
```

## Target and compatibility
Initial supplied version: 7.27.302, split APKM with `base.apk` and `split_config.armeabi_v7a.apk`. This variant requires Android API 32+. Check the TV's SDK level before attempting installation. See `research/2026-10-23-initial-inspection.md`.

## Next technical milestone
Trace actual references and call sites; distinguish local capability checks from remote configuration. Only build a narrow patch if there is evidence for a testable modification and a safe rollback procedure.
