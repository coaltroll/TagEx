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

SAMPLES_PATH = os.path.join(os.getcwd(), "samples")


def supported_audio_format(filename):
    for ext in SUPPORTED_AUDIO_EXTENSIONS:
        if filename.endswith(ext):
            return True
    return False


def read_audio_files(directory_path):
    metadata_items = []
    for filename in os.listdir(directory_path):
        if not supported_audio_format(filename):
            continue

        filepath = os.path.join(SAMPLES_PATH, filename)
        metadata_items.append(music_tag.load_file(filepath))
    return metadata_items


def _main():
    for audio_file in read_audio_files(SAMPLES_PATH):
        print(audio_file["title"])

    return 0


if __name__ == "__main__":
    sys.exit(_main())
