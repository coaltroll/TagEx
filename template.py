from typing import Optional, TypedDict


class MusicFile(TypedDict):
    album: str
    albumartist: str
    artists: list[str]
    artwork: Optional[bytes]
    comment: str
    compilation: Optional[bool]
    composers: list[str]
    discnumber: Optional[int]
    genre: list[str]
    lyrics: str
    totaldiscs: Optional[int]
    totaltracks: Optional[int]
    tracknumber: Optional[int]
    tracktitle: str
    year: Optional[int]
    isrc: str


def fun(music_files: list[MusicFile]) -> list[MusicFile]:
    def per_file(f: MusicFile) -> MusicFile:
        # ...modify your music file
        return f

    music_files = list(map(per_file, music_files))

    return music_files


f: MusicFile = {
    "album": "",
    "albumartist": "",
    "artists": [],
    "artwork": None,
    "comment": "",
    "compilation": None,
    "composers": [],
    "discnumber": None,
    "genre": [],
    "lyrics": "",
    "totaldiscs": None,
    "totaltracks": None,
    "tracknumber": None,
    "tracktitle": "",
    "year": None,
    "isrc": "",
}

# set artwork
with open("/sample/cover.jpg", "rb") as img_in:
    f["artwork"] = img_in.read()

# remove tags
f["compilation"] = None
