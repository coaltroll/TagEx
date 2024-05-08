import curses
import re
import sys
import os
from typing import TypedDict
import music_tag
import questionary
import npyscreen

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

unique_metadata_fields = [
    "tracktitle",
    "tracknumber",
    "comment",
]

metadata_fields = [
    *unique_metadata_fields,
    "album",
    "albumartist",
    "artist",
    "genre",
    "year",
    "composer",
    "totaldiscs",
    "totaltracks",
    "compilation",
    "discnumber",
]


def valid_audio_format(filename: str) -> bool:
    for extension in SUPPORTED_AUDIO_EXTENSIONS:
        if filename.endswith(extension):
            return True
    return False


class MusicFile(TypedDict):
    filename: str
    filepath: str
    metadata_item: music_tag.MetadataItem


def read_music_files(directory_path: str) -> list[MusicFile]:
    return sorted(
        [
            {
                "filename": filename,
                "filepath": (filepath := os.path.join(directory_path, filename)),
                "metadata_item": music_tag.load_file(filepath),
            }
            for filename in os.listdir(directory_path)
            if valid_audio_format(filename)
        ],
        key=lambda file: file["metadata_item"]["tracknumber"].first or file["filename"],
    )


class TitleMultiLineEdit(npyscreen.TitleText):
    _entry_type = npyscreen.MultiLineEdit


class ChoiceSelectButton(npyscreen.ButtonPress):
    def __init__(self, screen, choices, *args, **keywords):
        self.choices = choices
        self.result = choices[0]
        super().__init__(screen, *args, **keywords)

    def whenPressed(self):
        self.result = questionary.select(
            "Pick a field to help differentiate between the music files.",
            choices=self.choices,
        ).ask()
        curses.initscr().clear()
        curses.curs_set(2)
        self.parent.DISPLAY()


class ApplyRegexButton(npyscreen.ButtonPress):
    def __init__(self, screen, metaDataField, results, directory, *args, **keywords):
        self.metaDataField = metaDataField
        self.results = results
        self.directory = directory
        super().__init__(screen, *args, **keywords)

    def whenPressed(self):
        if npyscreen.notify_ok_cancel(
            "Are you sure you want to apply the results to all files?", title=""
        ):
            music_files = read_music_files(self.directory)

            for i, f in enumerate(music_files):
                f["metadata_item"][self.metaDataField] = self.results[i]
                f["metadata_item"].save()
            self.parent.update()

class ParentUpdatingTitleText(npyscreen.TitleText):
    def when_value_edited(self):
        self.parent.update()


class ParentUpdatingTitleFilenameCombo(npyscreen.TitleFilenameCombo):
    def when_value_edited(self):
        self.parent.update()


class RegexForm(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        _, x = self.useable_space()
        self.dir = self.add(
            ParentUpdatingTitleFilenameCombo,
            name="Directory:",
            select_dir=True,
            value=self.get_directory(),
            begin_entry_at=14,
        )
        self.regex = self.add(ParentUpdatingTitleText, name="Regex:", begin_entry_at=14)
        self.replace = self.add(
            ParentUpdatingTitleText, name="Replace:", begin_entry_at=14
        )
        self.status = self.add(
            TitleMultiLineEdit,
            max_height=3,
            name="Status:",
            begin_entry_at=14,
            editable=False,
            value="OK",
        )

        self.applyRegexButton = self.add(
            ApplyRegexButton,
            name="[ Apply Regex ]",
            metaDataField="",
            results=[],
            directory="",
        )

        initial_button_name = " " * (x // 3 - 6)

        self.nextrely += 1
        self.disButton = self.add(
            ChoiceSelectButton, choices=unique_metadata_fields, name=initial_button_name
        )

        self.nextrely -= 1
        self.originButton = self.add(
            ChoiceSelectButton,
            choices=metadata_fields,
            relx=x // 3,
            name=initial_button_name,
        )

        self.nextrely -= 1
        self.resultButton = self.add(
            ChoiceSelectButton,
            choices=metadata_fields,
            relx=(x // 3) * 2,
            name=initial_button_name,
        )
        self.grid = self.add(
            npyscreen.GridColTitles,
            editable=False,
        )
        self.grid.default_column_number = 3

        self.update()

    def display(self, clear=False):
        self.disButton.name = f"Distinction ({self.disButton.result}) ▼"
        self.originButton.name = f"Origin ({self.originButton.result}) ▼"
        self.resultButton.name = f"Result ({self.resultButton.result}) ▼"
        return super().display(clear)

    def update(self):
        self.update_grid()
        self.update_apply_button()

    def update_apply_button(self):
        if self.grid.values and len(self.grid.values) > 0:
            self.applyRegexButton.hidden = False
            self.applyRegexButton.metaDataField = self.resultButton.result
            self.applyRegexButton.directory = self.dir.value
            self.applyRegexButton.results = list(map(lambda n: n[2], self.grid.values))
        else:
            self.applyRegexButton.hidden = True

        self.applyRegexButton.update()

    def update_grid(self):
        music_files = read_music_files(self.dir.value)

        if not music_files:
            self.status.value = f"""No files with a supported extension type found in directory '{self.dir.value}'.
Supported extensions:
{SUPPORTED_AUDIO_EXTENSIONS}"""
            self.status.update()
            self.grid.values = []
            self.grid.update()
            return

        self.status.value = "OK"
        self.status.update()
        self.grid.values = []

        for f in music_files:
            try:
                self.grid.values.append(
                    [
                        str(f["metadata_item"][self.disButton.result]),
                        str(f["metadata_item"][self.originButton.result]),
                        re.sub(
                            self.regex.value or "",
                            self.replace.value or "",
                            str(f["metadata_item"][self.originButton.result])
                        )
                        if "\x00"
                        not in re.sub(
                            self.regex.value or "",
                            self.replace.value or "",
                            str(f["metadata_item"][self.originButton.result]),
                        )
                        else "error"
                    ]
                )

            except re.error:
                self.grid.values.append(
                    [
                        str(f["metadata_item"][self.disButton.result]),
                        str(f["metadata_item"][self.originButton.result]),
                        "error",
                    ]
                )

        self.grid.update()

    def get_directory(self):
        directory = os.getcwd()
        if len(sys.argv) > 1:
            directory = os.path.join(directory, sys.argv[1])

        if not os.path.isdir(directory):
            print(f"ERROR: '{directory}' does not exist or is not a directory.")
            return 1

        return directory


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", RegexForm, name="TagEx")


def _main() -> int:
    MyApplication().run()
    return 0


if __name__ == "__main__":
    sys.exit(_main())
