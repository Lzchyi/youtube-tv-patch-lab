# YouTube TV Playback-Speed Research Lab

> **Status: Research only. No working playback-speed patch has been identified or verified.**

## Purpose
This is an independent, non-commercial personal research project for investigating playback-speed availability in the official YouTube application on an Android TV device I own.

## Disclaimer
This project is **not affiliated with, endorsed by, or supported by Google, YouTube, Sony, or their affiliates**. All product names and trademarks belong to their respective owners.

The repository contains research scripts and workflows only. It does **not** distribute proprietary YouTube APKs, copyrighted application assets, Google credentials, or modified YouTube binaries. Users must supply application files they are authorised to analyse and comply with applicable laws and terms. Personal-use intent does not itself grant permission to copy, modify, or distribute proprietary software.

Research results and experimental modifications may be incomplete, unreliable, or incompatible. No claim is made that playback-speed restrictions can be bypassed. Use at your own risk; preserve a rollback path and do not disable device security protections.

## Current capabilities
- Inspect an APK locally without installing it.
- Record SHA-256 and Android package metadata.
- Generate a structured diagnostic report with JADX text-search findings.
- Run a GitHub Actions research workflow on a **user-supplied** APK, without storing the APK as an artifact.

## Privacy and security
- **Use a private repository.** GitHub Actions runners receive the supplied APK, and a public repository may expose workflow metadata.
- Do not commit APKs, tokens, Google account information, or TV logs containing personal data.
- Workflow artifacts contain only reports, not APKs or decoded source.
- Review diagnostic reports before sharing; strings from an APK can include endpoints and identifiers.
- The workflow is manually triggered; it does not download proprietary APKs from third-party mirrors.

## Local analysis
Requires Python 3.11+, Android SDK `aapt` (optional), and JADX (optional).

```bash
python3 scripts/analyze_apk.py /path/to/your/youtube-tv.apk --output report
```

## GitHub Actions
1. Create a **private** GitHub repository and upload these project files.
2. Do not commit your APK. For GitHub Actions, encode your legally obtained APK as base64 and save it in a repository secret named `YOUTUBE_TV_APK_B64`. **GitHub secrets have a 48 KB size limit**, so a normal YouTube APK will not fit. For real APKs, use local analysis until a secure larger-file input workflow is added.
3. Open Actions → **Inspect supplied APK** → Run workflow after configuring a supported input method.
4. Download the `research-report` artifact.

The workflow intentionally stops at investigation. A patch/build pipeline will only be added after identifying a reproducible restriction mechanism.

## Planned investigation
1. Capture device model, firmware, YouTube version, and exact error message.
2. Compare current and historically working app versions from authorised copies.
3. Identify whether local capability checks or remote configuration determine speed availability.
4. Only then evaluate a narrow experimental patch, with installation and rollback testing.
