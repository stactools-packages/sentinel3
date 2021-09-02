# stactools-sentinel3

- Name: sentinel3
- Package: `stactools.sentinel3`
- PyPI: https://pypi.org/project/stactools-sentinel3/
- Owner: @chorng & @willrayeo
- Dataset homepage: https://registry.opendata.aws/sentinel-3/
- STAC extensions used:
  - [eo](https://github.com/stac-extensions/eo)
  - [proj](https://github.com/stac-extensions/projection/)
  - [sat](https://github.com/stac-extensions/sat)

This repository will assist you in the generation of STAC files for Sentinel 3 OLCI and SLSTR datasets.

## Examples

### STAC

- [OLCI Item](examples/S3A_OL_1_EFR____20210820T103153_20210820T103453_20210820T124206_0179_075_222_2160_LN1_O_NR_002.json.json)
- [SLSTR Item](examples/S3A_SL_1_RBT____20210827T074336_20210827T074636_20210827T094954_0179_075_320_3060_LN2_O_NR_004.json)

### Command-line usage

Description of the command line functions

```bash
$ stac sentinel3 create-item source destination
```

Use `stac sentinel3 --help` to see all subcommands and options.
