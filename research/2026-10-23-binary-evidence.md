# Investigation outcome: YouTube TV 7.27.302

**Status: No verified functional patch. Do not install or distribute an APK labeled patched.**

## Input inspected
User-supplied APKMirror APKM, package `com.google.android.youtube.tv`, version `7.27.302`, ARM v7a, minimum Android API 32.

APKM includes `base.apk` and `split_config.armeabi_v7a.apk`. The base APK contains `classes.dex`, `classes2.dex`, and `classes3.dex`.

## Direct DEX string evidence
Case-insensitive raw-byte occurrences:

| String | classes.dex | classes2.dex | classes3.dex |
|---|---:|---:|---:|
| playbackSpeed | 0 | 2 | 0 |
| playback_speed | 0 | 2 | 0 |
| playbackRate | 0 | 10 | 0 |
| not available on this device | 0 | 2 | 0 |

These are string occurrences, **not proof of a specific eligibility gate or patch point**. No JADX call graph or runtime trace has yet established the actual cause of the playback-speed restriction.

## Blockers
- No verified instruction sequence, method, or server feature flag identified to change.
- No functional patch can be claimed from string matching alone.
- No Sony X9000H runtime test performed.
- Uploaded APKM is not committed to the repository and cannot be accessed by the GitHub runner without a configured private input source.
- This APKM requires API 32+, which must be verified against the actual TV.

## Engineering decision
**Do not produce an arbitrary modified APK**: it would be indistinguishable from a fake fix, potentially compromise the package signature and complicate rollback. Continue with real call-site analysis and device diagnostics before attempting any bytecode modification.
