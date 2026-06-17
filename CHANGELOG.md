# Changelog

## [2.0.0] - 2026-06-14

### Added
- `pyproject.toml` with Python 3.9+ requirement
- `deep-translator` for Google translation (replaces broken `tkk` scraping)
- Optional `GOOGLE_TRANSLATE_API_KEY` for official Google Cloud Translation API
- UTF-8 / UTF-16 BOM auto-detection for `.strings` files (`io_utils.py`)
- Android `strings.xml` parsing via `ElementTree` (CDATA / nested text)
- `--names` flag to translate only selected Android string keys
- Channel auto-fallback (Youdao ↔ Google)
- Unit tests (`test/test_v2.py`)
- GitHub Actions CI

### Changed
- **Default translation channel: Youdao** (`-c youdao`)
- `-c` flag is now respected (no longer overridden by ping)
- CLI entry point moved to `mkTranslation/cli.py`
- README install instructions prioritize GitHub install

### Removed
- Python 2 support
- Legacy Google `tkk` token scraper in `network.py`

### Fixed
- `UnicodeDecodeError` on UTF-16 `.strings` files (#8)
- `UnicodeEncodeError` on Python 2 / non-UTF-8 writes (#4)
- Android XML strings skipped by regex (#6)
- Google `AttributeError` / `IndexError` on token fetch (#7, #10)
- Youdao `KeyError` on CDATA/HTML strings — improved with XML parser (#9)
- `translate` command not found — document `python -m mkTranslation.cli` (#1)
- Network/channel selection issues (#2)

## [1.6.1] and earlier

See [GitHub Releases](https://github.com/mythkiven/mkTranslate/releases) for legacy versions.
PyPI latest remains **1.6.1**; **2.0+ is distributed via GitHub**.
