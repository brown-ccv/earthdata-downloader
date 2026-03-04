# earthdata-downloader

Downloads data from NASA Earthdata using the NASA Worldview Snapshots API.

## Installation

### Preparation

```sh
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

### For regular use

```sh
pip install .
```

### For development

```sh
pip install -e ".[dev]"
```

## CLI

Upon installation the `earthdata-downloader` command will be available. View its help with:

```sh
earthdata-downloader --help
```

## Usage

```bash
mkdir -p data/
earthdata-downloader load data/tci.tiff --kind truecolor
earthdata-downloader load data/cld.tiff --kind cloud
earthdata-downloader load data/lnd.tiff --kind landmask
```

To get data from Aqua, rather than Terra:

```bash
earthdata-downloader load data/tci.tiff --kind truecolor --satellite aqua
earthdata-downloader load data/cld.tiff --kind cloud --satellite aqua
```
