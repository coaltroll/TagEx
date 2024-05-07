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
    # raise Exception()
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
            "Pick a field to help differentiate the music files.",
            choices=self.choices,
        ).ask()
        curses.initscr().clear()
        curses.curs_set(2)
        self.parent.DISPLAY()


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


class RegexForm(npyscreen.Form):
    directory = ""

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        _, x = self.useable_space()
        self.dir = self.add(
            npyscreen.TitleFilenameCombo,
            name="Directory:",
            select_dir=True,
            value=self.get_directory(),
            begin_entry_at=14,
        )
        self.regex = self.add(npyscreen.TitleText, name="Regex:", begin_entry_at=14)
        self.replace = self.add(npyscreen.TitleText, name="Replace:", begin_entry_at=14)
        self.status = self.add(
            TitleMultiLineEdit,
            max_height=3,
            name="Status:",
            begin_entry_at=14,
            editable=False,
            value="OK",
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

        self.adjust_widgets()

    def display(self, clear=False):
        self.disButton.name = f"Distinction ({self.disButton.result})"
        self.originButton.name = f"Origin ({self.originButton.result})"
        self.resultButton.name = f"Result ({self.resultButton.result})"
        self.update_grid()
        return super().display(clear)

    def adjust_widgets(self):
        if self.dir.value == self.directory:
            return
        self.directory = self.dir.value
        self.update_grid()

    def update_grid(self):
        music_files = read_music_files(self.directory)

        if not music_files:
            self.status.value = f"""No files with a supported extension type found in directory '{self.directory}'.
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
                            str(f["metadata_item"][self.originButton.result]),
                        ),
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

        # if self.grid.values[0][2] != "Airbag" and self.grid.values[0][2] != "":
        #     raise Exception(self.grid.values)
        self.grid.update()

        # self.grid.values = [
        #     [
        #         f["metadata_item"][self.disButton.result].value,
        #         origin_field := f["metadata_item"][self.originButton.result].value,
        #         "" try re.sub(
        #             self.regex.value or "",
        #             self.replace.value or "",
        #             origin_field
        #         ),
        #     ]
        #     for f in music_files
        # ]

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
        # self.addForm("SHIT", ShitForm, name="TagEx", app=self)


def _main() -> int:
    # current_directory = os.getcwd()
    # if len(sys.argv) > 1:
    #     music_directory = os.path.join(current_directory, sys.argv[1])
    # else:
    #     print("press tab for autocomplete")
    #     music_directory = os.path.join(
    #         current_directory,
    #         questionary.path(
    #             "Path to DIRECTORY with music files:",
    #             default="./",
    #             complete_style=prompt_toolkit.shortcuts.CompleteStyle.READLINE_LIKE,
    #         ).ask(),
    #     )

    # if not os.path.isdir(music_directory):
    #     print(f"ERROR: '{music_directory}' does not exist or is not a directory.")
    #     return 1

    # music_files = read_music_files(music_directory)

    # if not music_files:
    #     print(
    #         f"ERROR: No files with a supported extension type found in directory '{music_directory}'."
    #     )
    #     print("Supported extensions:")
    #     print(SUPPORTED_AUDIO_EXTENSIONS)
    #     return 1

    # music_filenames: list[str] = list(map(lambda file: file["filename"], music_files))
    # print("Music files:")
    # print(music_filenames)

    # load_all = questionary.confirm("Edit all files? (default: yes)").ask()
    # loaded_music_files: list[MusicFile] = music_files
    # if not load_all:
    #     music_filenames_to_load = questionary.checkbox(
    #         "Select music files to edit",
    #         choices=music_filenames,
    #         validate=(
    #             lambda list_of_selected: "Must select one or more files to edit"
    #             if not list_of_selected
    #             else True
    #         ),
    #     ).ask()
    #     loaded_music_files = list(
    #         filter(
    #             lambda file: file["filename"] in music_filenames_to_load, music_files
    #         )
    #     )

    # print(loaded_music_files)

    MyApplication().run()

    return 0


if __name__ == "__main__":
    sys.exit(_main())
