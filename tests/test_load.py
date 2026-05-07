from pathlib import Path

import pytest
import requests_mock

from earthdata_downloader.load import DataSet, ImageType, Satellite, load

ExampleDataSetBeaufortSea = DataSet(
    datetime="2016-07-01T00:00:00Z",
    wrap="day",
    satellite=Satellite.terra,
    kind=ImageType.truecolor,
    scale=10000,
    bbox=(
        -2330000,
        -420000,
        -1130000,
        750000,
    ),
    crs="EPSG:3413",
    ts=1683675557694,
)

ExampleDataSetWeddellSea = DataSet(
    datetime="2025-12-09T00:00:00Z",
    wrap="day",
    satellite=Satellite.terra,
    kind=ImageType.landmask,
    scale=10000,
    bbox=(
        -1279248,
        904965,
        -679248,
        1504965,
    ),
    crs="EPSG:3031",
    ts=1683675557694,
)

ExampleDataSetAntarctica = DataSet(
    datetime="2025-12-09T00:00:00Z",
    wrap="day",
    satellite=Satellite.terra,
    kind=ImageType.landmask,
    scale=100000,
    bbox=(
        -5000000,
        -5000000,
        5000000,
        5000000,
    ),
    crs="EPSG:3031",
    ts=1683675557694,
)


@pytest.mark.slow
@pytest.mark.parametrize("satellite", Satellite)
@pytest.mark.parametrize("kind", ImageType)
@pytest.mark.parametrize("dataset", [ExampleDataSetBeaufortSea, ExampleDataSetWeddellSea, ExampleDataSetAntarctica], ids=["beaufort-sea", "weddell-sea", "antarctica"])
def test_load_runs_without_crashing_for_different_parameters(kind, satellite, dataset):
    load(kind=kind,
         satellite=satellite,
         scale=dataset.scale,
         datetime=dataset.datetime,
         wrap=dataset.wrap,
         bbox=dataset.bbox,
         crs=dataset.crs,
         ts=dataset.ts,
         )


def test_error_on_empty_file():
    with requests_mock.Mocker() as m:
        m.get(
            "https://wvs.earthdata.nasa.gov/api/v1/snapshot",
            content=Path("tests/load/empty.tiff").read_bytes(),
        )
        with pytest.raises(AssertionError):
            load()
