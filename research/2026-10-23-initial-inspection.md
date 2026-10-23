# Initial binary inspection — 7.27.302

Date: 2026-10-23

## Supplied package
- Container: APKMirror .apkm bundle, not a standalone APK.
- Package: `com.google.android.youtube.tv`
- Version: `7.27.302`; version code `727302320`
- Variant: **armeabi-v7a, Android 12L+ (API 32 minimum)**.
- Contents: `base.apk` and `split_config.armeabi_v7a.apk`.
- Base APK SHA-256: `2e103f9f3198e46309d3c65bf77e50d7c1061f1083388d06ba0b846b5cf81f45`
- ARM split SHA-256: `a23e53dd7062d40f09549dc5531f8a7640ac1b9e9f771b0065d27e271f31adbc`

## Preliminary findings
A raw case-insensitive byte scan of `classes2.dex` found the strings:
- `playbackSpeed`
- `playback_speed`
- `playbackRate`
- `not available on this device`

These strings **do not establish** that any one of them controls the speed UI or error; no call graph or enforcement point has been verified. They are only search leads.

## Important compatibility warning
This APK variant requires Android API 32 (Android 12L) or newer. **The Sony X9000H's installed Android version has not been verified.** Do not attempt installation until `adb shell getprop ro.build.version.sdk` confirms compatibility. A different APK variant may be required.

## Next steps
1. Verify TV API level and architecture.
2. Run JADX analysis on extracted `base.apk`, retaining the split for installation context.
3. Identify actual call sites and distinguish local checks from server-delivered configuration.
4. Do not publish or commit proprietary APK binaries.

**Status:** Binary structure and string presence confirmed; no functional patch identified or tested.
