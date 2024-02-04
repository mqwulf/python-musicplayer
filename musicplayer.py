# Importing Required Modules & libraries
from tkinter import *
from tkinter.ttk import *
import pygame
import os

DEBUG = True

class MusicPlayer:
    """One object of this class represents a tkinter GUI application that plays
    audio files and can write and read a .m3u playlist."""

    def __init__(self, root):
        """TODO: Creates a tkinter GUI application that plays audio files and
        can write and read a .m3u playlist."""
        self.playlistfilename = 'playlist.m3u'
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("1000x200+200+200")
        pygame.init()
        pygame.mixer.init()
        self.track = StringVar()
        self.status = StringVar()
        # Creating trackframe for songtrack label & trackstatus label
        trackframe = LabelFrame(self.root, text="Song Track", relief=GROOVE)
        trackframe.place(x=0, y=0, width=600, height=100)
        # TODO Below make the self.track the textvariable for songtrack and
        # the self.status the textvariable for trackstatus
        songtrack = Label(trackframe,textvariable=self.track).grid(
            row=0, column=0, padx=10, pady=5)
        trackstatus = Label(trackframe,textvariable=self.status).grid(
            row=0, column=1, padx=10, pady=5)

        # Creating buttonframe
        buttonframe = LabelFrame(
            self.root, text="Control Panel", relief=GROOVE)
        # Inserting song control Buttons
        buttonframe.place(x=0, y=100, width=600, height=100)
        Button(buttonframe, text="Play", command=self.playsong).grid(
            row=0, column=0, padx=10, pady=5)
        Button(buttonframe, text="Pause", command=self.pausesong
               ).grid(row=0, column=1, padx=10, pady=5)
        Button(buttonframe, text="Unpause", command=self.unpausesong
               ).grid(row=0, column=2, padx=10, pady=5)
        Button(buttonframe, text="Stop", command=self.stopsong).grid(
            row=0, column=3, padx=10, pady=5)
        # TODO: Insert playlist control Buttons
        Button(buttonframe, text="Refresh From Folder",
               command=self.refresh).grid(row=1, column=3, padx=10, pady=5)
        Button(buttonframe, text="Save Playlist",
               command=self.saveplaylist).grid(
                   row=1, column=1, padx=10, pady=5)
        Button(buttonframe, text="Load Playlist",
               command=self.loadplaylist).grid(
                   row=1, column=0, padx=10, pady=5)
        Button(buttonframe, text="Remove Song", command=self.removesong).grid(
            row=1, column=2, padx=10, pady=5)

        # Creating songsframe
        songsframe = LabelFrame(self.root, text="Song Playlist", relief=GROOVE)
        songsframe.place(x=600, y=0, width=400, height=150)
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set,
                                selectbackground="gold",
                                selectmode=SINGLE, relief=GROOVE)
        # Applying Scrollbar to playlist Listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)

        # Adding playlist search controls
        searchframe = LabelFrame(self.root, relief=GROOVE)
        searchframe.place(x=600, y=145, width=400, height=50)
        search_input = Entry(searchframe, width=30)
        self.inputVar = StringVar()
        # TODO Below make the self.inputVar the textvariable for search_input
        search_input = Entry(searchframe, width=30, textvariable=self.inputVar)
        
        search_input.grid(row=1, column=1, padx=1, pady=1)
        # TODO: bind Return key to call self.search
        search_input.bind(sequence='<Return>', func=self.search)
        Button(searchframe, text="Search",
               command=self.search).grid(row=1, column=2, padx=1, pady=1)

        # Changing directory for fetching songs
        os.chdir("./music")
        # Inserting songs into playlist
        self.refresh()

    def search(self, *args):
        """
        An algorithm is a finite number of instructions or steps that are
        well defined, and it eventually halts, providing a solution
        to a general class of problems.
        This algorithm is searching if the input search query is in the list
        of songs, also deleting all the songs in the current playlist. Then if
        the search query exists, its adding the song to the playlist. If no
        songs at all, its inserting string No songs found into the playlist.
        
        Remove from the self.playlist ListBox any filename that does not
        partially match the characters from the self.inputVar of the
        search_input Entry widget.
        """
        length1 = self.playlist.size()
        songs = self.playlist.get(0, length1)
        self.playlist.delete(0, length1)

        filtered_songs = [song for song in songs if self.inputVar.get().lower()
                           in song.lower()]
        if filtered_songs:
            for idx, song in enumerate(filtered_songs):
                self.playlist.insert(idx, song)
        else:
            self.playlist.insert(0, "No songs found")

    def playsong(self):
        """Displays selected song and its playing status and plays the song."""
        self.track.set(self.playlist.get(ACTIVE))
        self.status.set("-Playing")
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        pygame.mixer.music.play()

    def stopsong(self):
        """Displays stopped status and stops the song."""
        self.status.set("-Stopped")
        pygame.mixer.music.stop()

    def pausesong(self):
        """Displays the paused status and pauses the song."""
        self.status.set("-Paused")
        pygame.mixer.music.pause()

    def unpausesong(self):
        """Displays the playing status and unpauses the song."""
        self.status.set("-Playing")
        pygame.mixer.music.unpause()

    def removesong(self):
        """Deletes the active song from the playlist."""
        self.playlist.delete(ACTIVE)

    def loadplaylist(self):
        """
        TODO: Clears the current playlist and loads a previously saved playlist
        from the music folder. A user friendly message is appended to the
        status
        if a FileNotFoundError is caught(see the demo video).
        All other exception messages are
        appended to the status in their default string form.
        Ignore the lines that start with #.
        """
        self.inputVar.set("")
        filename = "../playlist.m3u"
        playlist = []
        try:
            with open(filename, "r") as file:
                playlist = [a.strip() for a in file if not a.startswith("#")]
            self.playlist.delete(0, END)
            self.playlist.insert(END, *playlist)
        except FileNotFoundError:
            self.status.set(
                f"{self.status.get()} file playlist.m3u was not found.")
        

        # TODO: First clear the search_input Entry widget via self.inputVar

    def saveplaylist(self):
        """TODO: Save the current playlist to the playlist file in the music
        folder. All exception messages are appended to the status in their
        default string form.
        Make sure the first line of the file is only:
        #EXTM3U
        """
        filename = "../playlist.m3u"
        playlist_songs = self.playlist.get(0, END)
        with open(filename, "w") as file:
            file.write("#EXTM3U\n")
            file.write("\n".join(playlist_songs))

    def refresh(self):
        """
        TODO:
        Clears the current playlist and fills it with all valid sound files
        from the music folder. All exception messages are appended to the
        status in their default string form.
        See the .pdf reference files for how to insert items into a tkinter
        Listbox."""
        self.inputVar.set("")
        self.playlist.delete(0, END)
        self.inputVar.set("")

        allowed_extensions = (".mp3", ".ogg", ".wav")
        playlist_files = [filename for filename in os.listdir(".") 
                          if not filename.startswith(".") and
                          filename.endswith(allowed_extensions)]

        for idx, filename in enumerate(playlist_files):
            self.playlist.insert(idx, filename)

        # First clear the search_input Entry widget via self.inputVar


def main():
    """Create main window and start a MusicPlayer application on it."""
    # Creating TK root window
    root = Tk()
    # Passing root to the MusicPlayer constructor
    app = MusicPlayer(root)
    # Start the main GUI loop
    root.mainloop()


if __name__ == "__main__":
    main()
