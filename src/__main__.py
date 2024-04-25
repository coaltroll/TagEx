# import sys
# import os
# import time
# from typing import TypedDict
# import music_tag
# import prompt_toolkit
# import questionary
# import pytermgui as ptg

# SUPPORTED_AUDIO_EXTENSIONS: list[str] = [
#     "aac",
#     "aiff",
#     "dsf",
#     "flac",
#     "m4a",
#     "mp3",
#     "ogg",
#     "opus",
#     "wav",
#     "wv",
# ]


# def valid_audio_format(filename: str) -> bool:
#     for extension in SUPPORTED_AUDIO_EXTENSIONS:
#         if filename.endswith(extension):
#             return True
#     return False


# class MusicFile(TypedDict):
#     filename: str
#     filepath: str
#     metadata_item: music_tag.MetadataItem


# def read_music_files(directory_path: str) -> list[MusicFile]:
#     return [
#         {
#             "filename": filename,
#             "filepath": (filepath := os.path.join(directory_path, filename)),
#             "metadata_item": music_tag.load_file(filepath),
#         }
#         for filename in os.listdir(directory_path)
#         if valid_audio_format(filename)
#     ]


# def _main() -> int:
#     # with ptg.WindowManager() as manager:
#     #     demo = ptg.Container(
#     #         ptg.Window(),
#     #         "[210 bold]Hello world!",
#     #         "",
#     #         ptg.InputField(prompt="Who are you?"),
#     #         "",
#     #         ["Submit!"]
#     #     )

#     #     manager.add(demo)
#     #     manager.run()

#     # with ptg.WindowManager() as manager:
#     #     window = (
#     #         ptg.Window(
#     #             # ptg.Container(""),
#     #             # ptg.Container(""),
#     #             # ptg.Container(""),
#     #             "",
#     #             ptg.InputField("Balazs", prompt="Name: "),
#     #             ptg.InputField("Some street", prompt="Address: "),
#     #             ptg.InputField("+11 0 123 456", prompt="Phone number: "),
#     #             "",
#     #             ptg.Container(
#     #                 "Additional notes:",
#     #                 ptg.InputField(
#     #                     "A whole bunch of\nMeaningful notes\nand stuff", multiline=True
#     #                 ),
#     #                 box="EMPTY_VERTICAL",
#     #             ),
#     #             "",
#     #             ["Submit"],
#     #         )
#     #         .set_title("[210 bold]New contact")
#     #         .center()
#     #     )
#     #     manager.add(window)

#     current_directory = os.getcwd()
#     if len(sys.argv) > 1:
#         music_directory = os.path.join(current_directory, sys.argv[1])
#     else:
#         print("press tab for autocomplete")
#         music_directory = os.path.join(
#             current_directory,
#             questionary.path(
#                 "Path to DIRECTORY with music files:",
#                 default="./",
#                 complete_style=prompt_toolkit.shortcuts.CompleteStyle.READLINE_LIKE,
#             ).ask(),
#         )

#     if not os.path.isdir(music_directory):
#         print(f"ERROR: '{music_directory}' does not exist or is not a directory.")
#         return 1

#     music_files = read_music_files(music_directory)

#     if not music_files:
#         print(
#             f"ERROR: No files with a supported extension type found in directory '{music_directory}'."
#         )
#         print("Supported extensions:")
#         print(SUPPORTED_AUDIO_EXTENSIONS)
#         return 1

#     music_filenames: list[str] = list(map(lambda file: file["filename"], music_files))
#     print("Music files:")
#     print(music_filenames)

#     load_all = questionary.confirm("Edit all files? (default: yes)").ask()
#     loaded_music_files: list[MusicFile] = music_files
#     if not load_all:
#         music_filenames_to_load = questionary.checkbox(
#             "Select music files to edit",
#             choices=music_filenames,
#             validate=(
#                 lambda list_of_selected: "Must select one or more files to edit"
#                 if not list_of_selected
#                 else True
#             ),
#         ).ask()
#         loaded_music_files = list(
#             filter(
#                 lambda file: file["filename"] in music_filenames_to_load, music_files
#             )
#         )

#     print(loaded_music_files)

#     return 0


# if __name__ == "__main__":
#     sys.exit(_main())

# import npyscreen


# def myFunction(*args):
#     F = npyscreen.Form(name="My Test Application")
#     myFW = F.add(npyscreen.TitleText, name="First Widget")
#     F.edit()
#     return myFW.value


# if __name__ == "__main__":
#     print(npyscreen.wrapper_basic(myFunction))
#     print("Blink and you missed it!")

# import os
# import wx


# class MainWindow(wx.Frame):
#     def __init__(self, parent, title):
#         wx.Frame.__init__(self, parent, title=title, size=(800, 500))
#         self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
#         self.CreateStatusBar()  # A StatusBar in the bottom of the window

#         # Setting up the menu.
#         filemenu = wx.Menu()

#         # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
#         menuAbout = filemenu.Append(
#             wx.ID_ABOUT, helpString=" Information about this program"
#         )
#         menuExit = filemenu.Append(wx.ID_EXIT, helpString=" Terminate the program")
#         menuFile = filemenu.Append(
#             wx.ID_FILE,
#             item="&Open File...",
#             helpString=" Open file to write to text box",
#         )

#         # Creating the menubar.
#         menuBar = wx.MenuBar()
#         menuBar.Append(filemenu, "&File")  # Adding the "filemenu" to the MenuBar
#         self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

#         # Set events.
#         self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
#         self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
#         self.Bind(wx.EVT_MENU, self.OnOpen, menuFile)

#         self.Show(True)

#     def OnAbout(self, e):
#         # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
#         dlg = wx.MessageDialog(self, "TagEx is a CLI tool to manually modify music file metadata efficiently and conveniently.", "About TagEx")
#         dlg.ShowModal()  # Show it
#         dlg.Destroy()  # finally destroy it when finished.

#     def OnExit(self, e):
#         self.Close(True)  # Close the frame.

#     def OnOpen(self, e):
#         self.dirname = ""
#         dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
#         if dlg.ShowModal() == wx.ID_OK:
#             self.filename = dlg.GetFilename()
#             self.dirname = dlg.GetDirectory()
#             f = open(os.path.join(self.dirname, self.filename), "r")
#             self.control.SetValue(f.read())
#             f.close()
#         dlg.Destroy()


# app = wx.App(False)
# frame = MainWindow(None, "TagEx")
# app.MainLoop()


import wx
import os


class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname = ""

        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        wx.Frame.__init__(self, parent, title=title, size=(200, -1))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()  # A Statusbar in the bottom of the window

        # Setting up the menu.
        filemenu = wx.Menu()
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", " Open a file to edit")
        menuAbout = filemenu.Append(
            wx.ID_ABOUT, "&About", " Information about this program"
        )
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")  # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Events.
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        for i in range(0, 6):
            self.buttons.append(wx.Button(self, -1, "Button &" + str(i)))
            self.sizer2.Add(self.buttons[i], 1, wx.EXPAND)

        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)

        # Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show()

    def OnAbout(self, e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(
            self,
            "TagEx is a CLI tool to manually modify music file metadata efficiently and conveniently.",
            "About TagEx",
        )
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def OnExit(self, e):
        self.Close(True)  # Close the frame.

    def OnOpen(self, e):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(
                os.path.normpath(os.path.join(self.dirname + os.sep, self.filename)),
                "r",
            )
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()


app = wx.App(False)
frame = MainWindow(None, "TagEx")
app.MainLoop()

# import wx


# class ExamplePanel(wx.Panel):
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent)

#         # create some sizers
#         mainSizer = wx.BoxSizer(wx.VERTICAL)
#         grid = wx.GridBagSizer(hgap=5, vgap=5)
#         hSizer = wx.BoxSizer(wx.HORIZONTAL)

#         self.quote = wx.StaticText(self, label="Your quote: ")
#         grid.Add(self.quote, pos=(0,0))

#         # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
#         self.logger = wx.TextCtrl(self, size=(200,300), style=wx.TE_MULTILINE | wx.TE_READONLY)

#         # A button
#         self.button =wx.Button(self, label="Save")
#         self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)

#         # the edit control - one line version.
#         self.lblname = wx.StaticText(self, label="Your name :")
#         grid.Add(self.lblname, pos=(1,0))
#         self.editname = wx.TextCtrl(self, value="Enter here your name", size=(140,-1))
#         grid.Add(self.editname, pos=(1,1))
#         self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
#         self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)

#         # the combobox Control
#         self.sampleList = ['friends', 'advertising', 'web search', 'Yellow Pages']
#         self.lblhear = wx.StaticText(self, label="How did you hear from us ?")
#         grid.Add(self.lblhear, pos=(3,0))
#         self.edithear = wx.ComboBox(self, size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
#         grid.Add(self.edithear, pos=(3,1))
#         self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
#         self.Bind(wx.EVT_TEXT, self.EvtText,self.edithear)

#         # add a spacer to the sizer
#         grid.Add((10, 40), pos=(2,0))

#         # Checkbox
#         self.insure = wx.CheckBox(self, label="Do you want Insured Shipment ?")
#         grid.Add(self.insure, pos=(4,0), span=(1,2), flag=wx.BOTTOM, border=5)
#         self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.insure)

#         # Radio Boxes
#         radioList = ['blue', 'red', 'yellow', 'orange', 'green', 'purple', 'navy blue', 'black', 'gray']
#         rb = wx.RadioBox(self, label="What color would you like ?", pos=(20, 210), choices=radioList,  majorDimension=3,
#                          style=wx.RA_SPECIFY_COLS)
#         grid.Add(rb, pos=(5,0), span=(1,2))
#         self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)

#         hSizer.Add(grid, 0, wx.ALL, 5)
#         hSizer.Add(self.logger)
#         mainSizer.Add(hSizer, 0, wx.ALL, 5)
#         mainSizer.Add(self.button, 0, wx.CENTER)
#         self.SetSizerAndFit(mainSizer)

#     def EvtRadioBox(self, event):
#         self.logger.AppendText("EvtRadioBox: %d\n" % event.GetInt())

#     def EvtComboBox(self, event):
#         self.logger.AppendText("EvtComboBox: %s\n" % event.GetString())

#     def OnClick(self, event):
#         self.logger.AppendText(" Click on object with Id %d\n" % event.GetId())

#     def EvtText(self, event):
#         self.logger.AppendText("EvtText: %s\n" % event.GetString())

#     def EvtChar(self, event):
#         self.logger.AppendText("EvtChar: %d\n" % event.GetKeyCode())
#         event.Skip()

#     def EvtCheckBox(self, event):
#         self.logger.AppendText("EvtCheckBox: %d\n" % event.Checked())


# # app = wx.App(False)
# # frame = wx.Frame(None, size=(500, 500))
# # panel = ExamplePanel(frame)
# # frame.Show()
# # app.MainLoop()
# app = wx.App(False)
# frame = wx.Frame(None, title="Demo with Notebook")
# panel = ExamplePanel(frame)
# frame.Show()
# app.MainLoop()

# import wx
# import wx.grid

# class GridFrame(wx.Frame):
#     def __init__(self, parent):
#         wx.Frame.__init__(self, parent)

#         # Create a wxGrid object
#         grid = wx.grid.Grid(self, -1)

#         # Then we call CreateGrid to set the dimensions of the grid
#         # (100 rows and 10 columns in this example)
#         grid.CreateGrid(12, 3)

#         # We can set the sizes of individual rows and columns
#         # in pixels
#         # grid.SetRowSize(0, 60)
#         # grid.SetColSize(0, 120)

#         # And set grid cell contents as strings
#         # grid.SetCellValue(0, 0, 'wxGrid is good')

#         # We can specify that some cells are read.only
#         # grid.SetCellValue(0, 3, 'This is read.only')
#         # grid.SetReadOnly(0, 3)

#         # Colours can be specified for grid cell contents
#         # grid.SetCellValue(3, 3, 'green on grey')
#         # grid.SetCellTextColour(3, 3, wx.GREEN)
#         # grid.SetCellBackgroundColour(3, 3, wx.LIGHT_GREY)

#         # We can specify the some cells will store numeric
#         # values rather than strings. Here we set grid column 5
#         # to hold floating point values displayed with width of 6
#         # and precision of 2
#         # grid.SetColFormatFloat(5, 6, 2)
#         grid.SetCellValue(0, 6, '3.1415')

#         self.Show()


# if __name__ == '__main__':
#     app = wx.App(0)
#     frame = GridFrame(None)
#     app.MainLoop()
