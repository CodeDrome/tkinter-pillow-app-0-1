from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import PIL.ImageTk

import pillowappengine


class ApplicationWindow(Frame):

    """
    Create and configure a Tkinter window.
    Also creates a pillowappengine.PillowAppEngine
    object which this application provides
    a front end for.
    """

    def __init__(self, master=None):

        self.pae = pillowappengine.PillowAppEngine()

        self.tkinter_image = None

        self.window_title = "Tkinter Pillow App 0.1"

        self.window = Tk()
        self.window.title(self.window_title)
        self.window.geometry("800x600")
        self.window.attributes('-zoomed', True)
        self.window.grid_propagate(False)

        self.window.update()
        self.width = self.window.winfo_width()
        self.height = self.window.winfo_height()

        self.create_menu()

        self.create_widgets()

        self.window.mainloop()

    def set_image_label_size(self):

        """
        Resizes the label containing the image
        to the window.
        """

        if self.image_label.image is not None:

            self.image_label.config(width=self.width - 6, height=self.height - 6 - self.toolbar.winfo_height())

    def on_resize(self, event):

        """
        Handles the window's Configure event
        for the case when the window is
        being resized.
        """

        self.window.update()

        if self.window.winfo_width() != self.width or self.window.winfo_height() != self.height:

            self.width = self.window.winfo_width()
            self.height = self.window.winfo_height()

            self.set_image_label_size()

    def create_menu(self):

        """
        Create a menu and add items and functions
        to handle item selections.
        """

        menu = Menu(self.window)

        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open...", command=self.open)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_command(label="Save as...", command=self.save_as)
        filemenu.add_command(label="Close", command=self.close)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.window.quit)

        imagemenu = Menu(menu)
        menu.add_cascade(label="Image", menu=imagemenu)
        imagemenu.add_command(label="Info", command=self.image_info)

        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=self.about)

        self.window.config(menu=menu)

    def create_widgets(self):

        """
        Add toolbar, image window and all other
        non-menu items.
        """

        self.toolbar = Frame(self.window, borderwidth=1, relief="raised")
        self.toolbar.grid(row=0, column=0, padx=0, pady=0, sticky=W)

        self.open_button = Button(self.toolbar, text="Open", command=self.open)
        self.open_button.grid(row=0, column=0, padx=2, pady=2, sticky=W)

        self.save_button = Button(self.toolbar, text="Save", command=self.save)
        self.save_button.grid(row=0, column=1, padx=2, pady=2, sticky=W)

        self.save_as_button = Button(self.toolbar, text="Save as", command=self.save_as)
        self.save_as_button.grid(row=0, column=2, padx=2, pady=2, sticky=W)

        self.image_label = Label(self.window, borderwidth=1, bg="white", relief="sunken", image=None)
        self.image_label.image = None

        self.window.bind("<Configure>", self.on_resize)

    def about(self):

        """
        Currently displays the Pillow version.
        Needs to be expanded.
        """

        messagebox.showinfo('Pillow Version', pillowappengine.PillowAppEngine.PILLOW_VERSION)

    def image_info(self):

        """
        Shows information about the current image.
        Will possibly be replaced with widgets
        in the main window.
        """

        messagebox.showinfo('Image Info', self.pae.get_properties_text())

    def open(self):

        """
        Shows an Open File dialog and opens/displays
        the selected image.
        """

        try:

            filepath = filedialog.askopenfilename(title="Open image", filetypes=(("JPEG files", "*.jpg"),))

            # Clicking Cancel returns an empty tuple.
            if filepath != ():

                self.pae.open(filepath)
                self.tkinter_image = PIL.ImageTk.PhotoImage(self.pae.image)

                self.image_label.configure(image=self.tkinter_image)
                self.image_label.image = self.tkinter_image
                self.image_label.grid(row=1, column=0, padx=2, pady=2)

                self.set_image_label_size()

                self.window.title(self.window_title + ": " + self.pae.get_properties()["filename"])

        except Exception as e:

            self.show_error_message(e)

    def save(self):

        """
        Saves the image to the filename
        it was opened from.
        """

        try:
            self.pae.save()
        except Exception as e:
            self.show_error_message(e)

    def save_as(self):

        """
        Shows a Save As dialog and saves the image
        to the selected filename.
        """

        try:

            filepath = filedialog.asksaveasfile(title="Save image as", filetypes=(("JPEG files", "*.jpg"),))

            print(filepath)
            print(type(filepath))

            # Clicking Cancel returns None.
            if filepath is not None:

                self.pae.save_as(filepath)

                self.window.title(self.window_title + ": " + self.pae.get_properties()["filename"])

        except Exception as e:

            self.show_error_message(e)

    def close(self):

        """
        Closes the current image, removes the image label
        and resets the window title.
        """

        self.pae.close()
        self.image_label.grid_forget()
        self.window.title(self.window_title)

    def show_error_message(self, e):

        messagebox.showerror("Error", e)


def main():

    appwin = ApplicationWindow()


main()
