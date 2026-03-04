#!/usr/bin/env python

import logging
from pathlib import Path
from typing import Annotated

import typer

from earthdata_downloader.bbox import BoundingBox, BoundingBoxParser
from earthdata_downloader.load import (
    ImageType,
    Satellite,
    ExampleDataSetBeaufortSea as ExampleDataSet,
)
from earthdata_downloader.load import load as load_

_logger = logging.getLogger(__name__)

app = typer.Typer(
    name="earthdata-downloader",
    add_completion=False,
    help="Download data from NASA Earthdata.",
)


@app.callback()
def main(
    quiet: Annotated[
        bool, typer.Option(help="Make the program less talkative.")
    ] = False,
    verbose: Annotated[
        bool, typer.Option(help="Make the program more talkative.")
    ] = False,
    debug: Annotated[
        bool, typer.Option(help="Make the program much more talkative.")
    ] = False,
):
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    elif quiet:
        level = logging.ERROR
    else:
        level = logging.WARNING

    logging.basicConfig(level=level)
    return


@app.command(help="Download an image.")
def load(
    outfile: Annotated[Path, typer.Argument()],
    datetime: str = ExampleDataSet.datetime,
    wrap: str = ExampleDataSet.wrap,
    satellite: Satellite = ExampleDataSet.satellite,
    kind: ImageType = ExampleDataSet.kind,
    bbox: Annotated[
        BoundingBox,
        typer.Option(click_type=BoundingBoxParser()),
    ] = ExampleDataSet.bbox,
    scale: Annotated[
        int, typer.Option(help="size of a pixel in units of the bounding box")
    ] = ExampleDataSet.scale,
    crs: str = ExampleDataSet.crs,
    ts: int = ExampleDataSet.ts,
    format: str = "image/tiff",
    validate: Annotated[bool, typer.Option(help="validate the image")] = True,
):
    _logger.debug(locals())

    result = load_(
        datetime=datetime,
        wrap=wrap,
        satellite=satellite,
        kind=kind,
        bbox=bbox,
        scale=scale,
        crs=crs,
        ts=ts,
        format=format,
        validate=validate,
    )

    with open(outfile, "wb") as f:
        f.write(result.content)

    return


if __name__ == "__main__":
    app()
