# PS5SX2 — PLDMNGR Source

A small PLDMNGR-compatible catalog containing the official PS5SX2 ELF payloads.

## Add to PLDMNGR

In PLDMNGR, open **Settings → Manage Sources → Add Source** and add:

```
https://raw.githubusercontent.com/barelynotlegal/PLDMNGR-ps5sx2/main/payloads.json
```

## Automatic updates

GitHub Actions checks the official [Swordpdf/PS5SX2 releases](https://github.com/Swordpdf/PS5SX2/releases) every two hours and regenerates `payloads.json` when a new release changes the available ELF assets. You can also run the workflow manually from the **Actions** tab.

Only ELF payload assets are listed. The PS5SX2 application ZIP is not an ELF payload; use the project's installer/updater and follow the official release notes for app installation and compatibility.

## Important

The helper variants are intended for different ShadowMountPlus versions. Read the official PS5SX2 release notes before choosing which helper to install or autoload. This catalog does not decide which variant is right for your console.
