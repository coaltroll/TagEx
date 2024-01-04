import sys
import os
import music_tag

SUPPORTED_AUDIO_EXTENSIONS = [
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


def valid_audio_format(filename):
    for ext in SUPPORTED_AUDIO_EXTENSIONS:
        if filename.endswith(ext):
            return True
    return False


def read_music_files(directory_path):
    return [
        {
            "filename": filename,
            "filepath": (filepath := os.path.join(directory_path, filename)),
            "metadata_item": music_tag.load_file(filepath),
        }
        for filename in os.listdir(directory_path)
        if valid_audio_format(filename)
    ]


def _main():
    music_directory = os.getcwd()

    if len(sys.argv) > 1:
        music_directory = os.path.join(music_directory, sys.argv[1])

    if not os.path.isdir(music_directory):
        print(
            f"ERROR: Directory '{music_directory}' does not exist or is not a directory."
        )
        return 1

    metadata_items = map(
        lambda audio_file: audio_file["metadata_item"],
        read_music_files(music_directory),
    )
    for audio_file in metadata_items:
        print(audio_file["title"])

    return 0


if __name__ == "__main__":
    sys.exit(_main())
