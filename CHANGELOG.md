# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - 3/15/2024
### General
- Changed manifest format version to 2
- Re-wrote code for adding files to packs and add-ons to be dynamic
- The Identifier object should now correctly handle paths that have multiple colons.
- JSON Schemas should now be included in the package.

### Refactor
- `todo` submodule to `experimental` which contains objects that are still in development.
- `Identifier.parse` method to `Identifier.of`
- `BlockState` object to `BlockProperty` and added new BlockState which describes a block's ID and its block properties.
- Migrated from `__dict__` to `jsonify` for converting classes to JSON-friendly dictionaries.


### Added
- Feature
- FeatureRule
- Trading
- Geometry
- BlockCullingRules

## [0.0.2] - 2/3/2024
### General
- Added schemas to read any format version. See [Format Version](https://github.com/legopitstop/mcaddon/blob/main/FORMAT_VERSION.md) for supported versions
- Moved empty submodules to `todo`
- Support for [mustache](https://mustache.github.io/) templates when loading JSON files

### Added
- Recipe
- Volume
- Texture
- TerrainTextures
- ItemTextures
- CameraPreset

## [0.0.1] - 1/11/2024
- initial release.
