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

This repository will assist you in the generation of STAC files for Sentinel 3 OLCI (level 1 EFR, ERR and level 2 LFR, LRR, WFR) and SLSTR (level 1 RBT and level 2 FRP, LST, WST) datasets.

## Examples

### STAC

- [OLCI Level 1 EFR Item](examples/S3A_OL_1_EFR____20210820T103153_20210820T103453_20210820T124206_0179_075_222_2160_LN1_O_NR_002.json)
- [OLCI Level 1 ERR Item](examples/S3B_OL_1_ERR____20210902T054142_20210902T062554_20210903T103126_2652_056_262______LN1_O_NT_002.json)
- [OLCI Level 2 LFR Item](examples/S3A_OL_2_LFR____20180105T002409_20180105T002540_20180106T053045_0090_026_216_2069_LN1_O_NT_002.json)
- [OCLI Level 2 LRR Item](examples/S3B_OL_2_LRR____20210902T054142_20210902T062554_20210903T103456_2652_056_262______LN1_O_NT_002.json)
- [OLCI Level 2 WFR Item](examples/S3A_OL_2_WFR____20201006T012547_20201006T012847_20201007T100122_0180_063_302_3060_MAR_O_NT_002.json)
- [SLSTR Level 1 RBT Item](examples/S3A_SL_1_RBT____20210827T074336_20210827T074636_20210827T094954_0179_075_320_3060_LN2_O_NR_004.json)
- [SLSTR Level 2 FRP Item](examples/S3A_SL_2_FRP____20201104T001225_20201104T001525_20201105T060455_0179_064_330_1800_LN2_O_NT_004.json)
- [SLSTR Level 2 LST Item](examples/S3A_SL_2_LST____20180104T004105_20180104T022205_20180930T071122_6059_026_202______LR1_R_NT_003.json)
- [SLSTR Level 2 WST Item](examples/S3A_SL_2_WST____20190505T045344_20190505T063444_20190506T134130_6059_044_204______MAR_O_NT_003.json)

### Command-line usage

Description of the command line functions

```bash
$ stac sentinel3 create-item source destination
```

Use `stac sentinel3 --help` to see all subcommands and options.
