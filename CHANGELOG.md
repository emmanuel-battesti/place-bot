## [2.0.0] - 2025-12-19
### Removed
- Removed dependency on `simple-playground`. All playground-related code has been integrated into the `place_bot` package to simplify maintenance.

### Changed
- Consolidated playground functionality into `place_bot` (many internal refactorings and API changes).
- Updated packaging and imports to remove external dependency and centralize code.
- Migrated packaging to `pyproject.toml`; removed `setup.py` and `requirements.txt`. Installation and developer instructions updated accordingly.
- Examples and internal modules updated to use the local `place_bot` modules.

### Breaking
- This is a breaking release: public APIs and import paths have changed. Downstream projects must update imports and initialization code.

### Migration notes
- Replace imports from `simple_playground` with the equivalent modules under `place_bot.simu_world` or `place_bot.simulation`.
- Update any code that previously relied on `simple-playground` entry points to use the new `place_bot` APIs.
- Run the test-suite and update examples if you maintain downstream integrations.

## [1.2.0] - 2025-05-22
### Changed
- Refactoring of `my_robot_random.py` (code cleaned and reorganized)
- New display of lidar (faster)
- More comments in the code
- Renamed variables for clarity
- Improved `MouseMeasure` class

## [1.1.0] - 2023-03-06
### Added
- Add License file
- add parameter "use_shaders" directly in argument of the constructor of ClosedPlayground

### Changed
- Improving doc install
- Cleaning of the requirements file

### Fixed

## [1.0.0] - 2023-03-06

## [0.0.0] - 2022-11-18
### Added
- Initial commit

### Changed

### Fixed

[Unreleased]: https://github.com/emmanuel-battesti/place-bot/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/emmanuel-battesti/place-bot/releases/tag/v2.0.0
[1.2.0]: https://github.com/emmanuel-battesti/place-bot/releases/tag/v1.2.0
[1.1.0]: https://github.com/emmanuel-battesti/place-bot/releases/tag/v1.1.0
[1.0.0]: https://github.com/emmanuel-battesti/place-bot/releases/tag/v1.0.0
[0.0.0]: https://github.com/emmanuel-battesti/place-bot/releases/tag/v0.0.0
