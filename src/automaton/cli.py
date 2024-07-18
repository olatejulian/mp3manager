import logging
import sys
from typing import Optional

from typer import Typer

from .pdf import PDF, PdfMetaData
from .series import get_season_episode, is_video_file, video_name_format
from .utils import (
    directory_name,
    get_file_extension,
    list_filenames,
    rename_file,
    verify_path,
)

logger = logging.getLogger()

cli = Typer()


@cli.command()
def rename_series_episodes(path: str) -> None:
    try:
        if verify_path(path):
            filenames = list_filenames(path)

            for filename in filenames:
                if is_video_file(filename):
                    if season_episode := get_season_episode(filename):
                        new_name = video_name_format(
                            directory_name(path),
                            season_episode,
                            get_file_extension(filename),
                        )

                        rename_file(path, filename, new_name)

                        msg = f"Renamed: {filename} -> {new_name} successfully"

                        logging.info(msg=msg)

        else:
            raise FileNotFoundError(f"Directory not found: {path}")

    # pylint: disable=broad-except
    except Exception as e:
        logger.exception(e, stack_info=True)

        sys.exit(1)


@cli.command()
def rename_subtitles(path: str) -> None:
    raise NotImplementedError


@cli.command()
def rename_pdf_title(path: str, name: Optional[str] = None) -> None:
    pdf = PDF(path)

    if not name:
        name = directory_name(path)

    pdf.set_metadata(metadata=PdfMetaData(title=name))
