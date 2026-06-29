# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project attempts to match the major and minor versions of
[stactools](https://github.com/stac-utils/stactools) and increments the patch
number as needed.

## [Unreleased]

### Changed

- Item ID format ([#9](https://github.com/stactools-packages/sentinel3/pull/9))
- Use kebab-case for asset keys ([#13](https://github.com/stactools-packages/sentinel3/pull/13))
- Use snake_case for item properties ([#13](https://github.com/stactools-packages/sentinel3/pull/15))
- Use standard array shape and size ordering ([#16](https://github.com/stactools-packages/sentinel3/pull/16))
- Apply fixes to ensure valid geometric parameters, as well as proper handling
  of antimeridian behavior ([#17](https://github.com/stactools-packages/sentinel3/pull/17))

### Fixed

- Support the OLCI Collection 4 (v4.01) level 2 water processing baseline:
  data objects absent from a manifest (such as the OC4Me chlorophyll product
  `chlOc4meData`, removed in Collection 4) are skipped instead of raising a
  `RuntimeError`, and the new `chlor_a`, `fluorescence`, and `iop_lsd`
  products are turned into assets when present
- Use correct EO Extension attribute names and units ([#13](https://github.com/stactools-packages/sentinel3/pull/15))
- Use un-stripped `instance_id` to check for strip granules and apply geometry
  fix ([#19](https://github.com/stactools-packages/sentinel3/pull/19))
- Close file handles ([#21](https://github.com/stactools-packages/sentinel3/pull/21))
- Prevent addition of `'s3:shape'` to safe-manifest asset
  ([#22](https://github.com/stactools-packages/sentinel3/pull/23))
- Make `s3:spatial_resolution` unit meters ([#29](https://github.com/stactools-packages/sentinel3/pull/29))
- Don't add EO extension to radar products
  ([#26](https://github.com/stactools-packages/sentinel3/pull/30))

## [0.4.0] - 2023-03-31

First tagged release.

[Unreleased]: https://github.com/stactools-packages/sentinel3/compare/v0.4.0..HEAD
[0.4.0]: https://github.com/stactools-packages/sentinel3/releases/tag/v0.4.0
