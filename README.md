# stactools-sentinel3

- Name: sentinel3
- Package: `stactools.sentinel3`
- PyPI: <https://pypi.org/project/stactools-sentinel3/>
- Owner: @chorng & @willrayeo
- Dataset homepage: <https://registry.opendata.aws/sentinel-3/>
- STAC extensions used:
  - [eo](https://github.com/stac-extensions/eo)
  - [proj](https://github.com/stac-extensions/projection/)
  - [sat](https://github.com/stac-extensions/sat)

This repository will assist you in the generation of STAC files for Sentinel 3
OLCI (level 1 EFR, ERR and level 2 LFR, LRR, WFR), SLSTR (level 1 RBT and level
2 FRP, LST, WST), SRAL (level 2 LAN and WAT), and SYNERGY (level 2 AOD, SYN,
V10, VG1, VGP) datasets.

## Examples

### STAC

- [OLCI Level 1 EFR Item](examples/S3A_OL_1_EFR_20211021T073827_20211021T074112_0164_077_334_4320.json)
- [OLCI Level 1 ERR Item](examples/S3B_OL_1_ERR_20210831T200148_20210831T204600_2652_056_242.json)
- [OLCI Level 2 LFR Item](examples/S3A_OL_2_LFR_20210523T003029_20210523T003329_0179_072_102_1980.json)
- [OCLI Level 2 LRR Item](examples/S3B_OL_2_LRR_20210731T214325_20210731T222741_2656_055_186.json)
- [OLCI Level 2 WFR Item](examples/S3A_OL_2_WFR_20210604T001016_20210604T001316_0179_072_273_1440.json)
- [SLSTR Level 1 RBT Item](examples/S3A_SL_1_RBT_20210930T220914_20210930T221214_0180_077_043_5400.json)
- [SLSTR Level 2 FRP Item](examples/S3A_SL_2_FRP_20210802T000420_20210802T000720_0179_074_344_2880.json)
- [SLSTR Level 2 LST Item](examples/S3A_SL_2_LST_20210510T002955_20210510T003255_0179_071_301_5760.json)
- [SLSTR Level 2 WST Item](examples/S3B_SL_2_WST_20210419T051754_20210419T065853_6059_051_247.json)
- [SRAL Level 2 LAN Item](examples/S3A_SR_2_LAN_20210611T011438_20210611T012436_0598_072_373.json)
- [SRAL Level 2 WAT Item](examples/S3A_SR_2_WAT_20210704T012815_20210704T021455_2800_073_316.json)
- [SYNERGY Level 2 AOD Item](examples/S3B_SY_2_AOD_20210512T143315_20210512T151738_2663_052_196.json)
- [SYNERGY Level 2 SYN Item](examples/S3A_SY_2_SYN_20210325T005418_20210325T005718_0180_070_031_1620.json)
- [SYNERGY Level 2 V10 Item](examples/S3A_SY_2_V10_20210911T000000_20210920T235959_EUROPE.json)
- [SYNERGY Level 2 VG1 Item](examples/S3A_SY_2_VG1_20211013T000000_20211013T235959_EUROPE.json)
- [SYNERGY Level 2 VGP Item](examples/S3A_SY_2_VGP_20210703T142237_20210703T150700_2663_073_310.json)

### Command-line usage

Description of the command line functions

```shell
stac sentinel3 create-item source destination
```

Use `stac sentinel3 --help` to see all subcommands and options.

## Developing

Install the development requirements:

```shell
pip install -r requirements-dev.txt
```

We use [pre-commit](https://pre-commit.com/) to lint files on commits.
Install the hooks with:

```shell
pre-commit install
```

If you make changes to the output STAC items, update the examples:

```shell
python scripts/create_examples.py
```
