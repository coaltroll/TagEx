import sys
import os
from typing import TypedDict
import music_tag
import prompt_toolkit
import questionary

SUPPORTED_AUDIO_EXTENSIONS: list[str] = [
    "aac",
    "aiff",
    "dsf",
    "flac",
    "m4a",
    "mp3",
    "ogg",
    "opus",
    "wav",
    "wv",
]


def valid_audio_format(filename: str) -> bool:
    for extension in SUPPORTED_AUDIO_EXTENSIONS:
        if filename.endswith(extension):
            return True
    return False


class MusicFile(TypedDict):
    filename: str
    filepath: str
    metdata_item: music_tag.MetadataItem


def read_music_files(directory_path: str) -> list[MusicFile]:
    return [
        {
            "filename": filename,
            "filepath": (filepath := os.path.join(directory_path, filename)),
            "metadata_item": music_tag.load_file(filepath),
        }
        for filename in os.listdir(directory_path)
        if valid_audio_format(filename)
    ]


def _main() -> int:
    current_directory = os.getcwd()
    if len(sys.argv) > 1:
        music_directory = os.path.join(current_directory, sys.argv[1])
    else:
        print("press tab for autocomplete")
        music_directory = os.path.join(
            current_directory,
            questionary.path(
                "Path to DIRECTORY with music files:",
                default="./",
                complete_style=prompt_toolkit.shortcuts.CompleteStyle.READLINE_LIKE,
            ).ask(),
        )

    if not os.path.isdir(music_directory):
        print(f"ERROR: '{music_directory}' does not exist or is not a directory.")
        return 1

    music_files = read_music_files(music_directory)

    if not music_files:
        print(
            f"ERROR: No files with a supported extension type found in directory '{music_directory}'."
        )
        print("Supported extensions:")
        print(SUPPORTED_AUDIO_EXTENSIONS)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(_main())
