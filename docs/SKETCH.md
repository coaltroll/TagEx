## Linting
To be implemented. (since it will probably use functionality from the manual tagging tool)

## Manual Tagging
TagEx is a CLI tool to manually modify music file metadata efficiently and conveniently.

### Features
- Manually edit a metadata field or filename for each file.
  - Individually:
    - Type something, press enter, repeat.
  - Collectively:
    - type something, press enter, apply to all selected files.
- *Edit directory names?*

### Metadata tags to edit 
- **music-tag name (windows name)**
- album (Album)
- albumartist (Album artist) 
- artist (Contributing artists)
- artwork
- comment (Comments)
- compilation (Part of a compilation)
- composer (Composers)
- discnumber
- genre (Genre)
- lyrics
- totaldiscs
- totaltracks
- tracknumber (#)
- tracktitle (Title)
- year (Year)
- isrc

### Usage

1. Pick the directory with the music files
2. Pick which music files to load
3. Define variables
4. Use variables or manual input to edit all music files or one at a time

#### Sketches for steps

##### Step 1: Pick the directory with the music files
- Feed directory as command line argument
  - `tagex "./[1987] Whenever You Need Somebody"`
- Use `tagex` and give user [Questionary file path prompt](https://questionary.readthedocs.io/en/stable/pages/types.html#file-path)

*error handling if no supported files found in directory selected:*
```
No files with a supported extension type found in directory DIRECTORY.
Supported extensions:
SUPPORTED_EXTENSIONS 
```

##### Step 2: Pick which music files to load
- Show loadable music files through [music-tag](https://github.com/KristoforMaynard/music-tag) and use [Questionary confirmation prompt](https://questionary.readthedocs.io/en/stable/pages/types.html#confirmation) if user wants to edit all files or select which to edit. 
  - If user wants to select which files to edit, give user a [Questionary checkbox prompt](https://questionary.readthedocs.io/en/stable/pages/types.html#checkbox) to select music files from the ones available
    - *error handling if no files picked:* Reset checkbox prompt and show error message: `Must select one or more files to edit`

##### Step 3: Define variables

##### Step 4: Use variables or manual input to edit loaded music file(s)

