import os
import shutil
import tkinter
import customtkinter as ctk
import tkinter as tk
import fitz
from pytube import YouTube
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image

# system settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# app frame (main Window)
app = ctk.CTk()
app.geometry('500x500')
app.resizable(False, False)
app.title('AppHub')
color = app.cget("bg")


# switch indicator for button click function(to indicate the button the user is clicking
def switch(indicator_lb, page):
    for child in options.winfo_children():
        if isinstance(child, tk.Label):
            child['bg'] = color

    indicator_lb['bg'] = '#FFFFFF'

    for fm in main_fm.winfo_children():
        fm.destroy()
        app.update()

    page()


# create the top frame that houses the buttons


options = ctk.CTkFrame(app, fg_color="transparent")

YT_btn = tk.Button(options, text='YTDownloader', font=('Times New Romans', 13),
                   bd=0, fg='#FFFFFF', activeforeground='#0097e8', bg=color,
                   command=lambda: switch(indicator_lb=YT_indicator_lb,
                                          page=yt_page))
YT_btn.place(x=0, y=0, width=125)

YT_indicator_lb = tk.Label(options, bg=color)
YT_indicator_lb.place(x=22, y=30, width=80, height=2)

organizer_btn = tk.Button(options, text='File Organizer', font=('Times New Romans', 13),
                          bd=0, fg='#FFFFFF', activeforeground='#0097e8', bg=color,
                          command=lambda: switch(indicator_lb=organizer_indicator_lb,
                                                 page=file_page))
organizer_btn.place(x=125, y=0, width=125)

organizer_indicator_lb = tk.Label(options)
organizer_indicator_lb.place(x=137, y=30, width=100, height=2)

extractor_btn = tk.Button(options, text='Text Extractor', font=('Times New Romans', 13),
                          bd=0, fg='#FFFFFF', activeforeground='#0097e8', bg=color,
                          command=lambda: switch(indicator_lb=extractor_indicator_lb,
                                                 page=extractor_page))
extractor_btn.place(x=250, y=0, width=125)

extractor_indicator_lb = tk.Label(options)
extractor_indicator_lb.place(x=262, y=30, width=100, height=2)

options.pack(pady=5)
options.pack_propagate(False)
options.configure(width=500, height=35)


# create a function to switch between frames

def yt_page():
    yt_page_fm = ctk.CTkFrame(main_fm, fg_color="transparent")

    # set the download folder to Downloads rather than project folder
    def download_folder():
        if os.name == 'nt':
            return os.path.join(os.environ['USERPROFILE'], 'Downloads')
        else:
            return os.path.join(os.path.expanduser('~'), 'Downloads')

    # get the list of resolutions available
    def video_details():
        try:
            ytLink = link.get()
            ytObject = YouTube(ytLink)
            title.configure(text=ytObject.title)

            # filter stream with progressive download
            streams = ytObject.streams.filter(progressive=True)

            # get unique resolutions available
            resolutions = list(set(stream.resolution for stream in streams))
            resolutions.sort(reverse=True)  # sort resolution in descending order
            rCombobox.configure(values=resolutions)
            if resolutions:
                rCombobox.set("Select resolutions")
                download.configure(state="normal")
            else:
                resLabel.configure(text="No resolution available for Download")
                rCombobox.set("none")
                download.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"cannot fetch video details: {e}")

    def startDownload():
        try:
            ytLink = link.get()
            ytObject = YouTube(ytLink, on_progress_callback=on_progress)
            video_resolution = rCombobox.get()
            if video_resolution == "Select resolutions" or video_resolution == "none":
                messagebox.showwarning("Warning", "Please select a valid resolution")
                return
            stream = ytObject.streams.filter(res=video_resolution, progressive=True).first()

            if stream:
                download_location = download_folder()
                stream.download(output_path=download_location)
                finishLabel.configure(text="Downloaded")
            else:
                finishLabel.configure(text="Download error", text_color="red")

            title.configure(text=ytObject.title, text_color="white")
            finishLabel.configure(text="No download")

        except Exception as e:
            messagebox.showerror("Error", "cannot fetch video details")

    def on_progress(stream, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_completed = bytes_downloaded / total_size * 100
        per = str(int(percentage_completed))
        pPercentage.configure(text=per + '%')
        pPercentage.update()

        # update progress bar
        progressBar.set(float(percentage_completed) / 100)

    # adding ui element
    title = ctk.CTkLabel(yt_page_fm, text="INSERT A YOUTUBE LINK")
    title.pack(padx=10, pady=10)

    # thumbnail label
    thumbnail_label = ctk.CTkLabel(yt_page_fm, text="")
    thumbnail_label.pack()

    # link input
    url_var = tkinter.StringVar()
    link = ctk.CTkEntry(yt_page_fm, width=350, height=40, textvariable=url_var)
    link.pack()

    # choose resolution
    resLabel = ctk.CTkLabel(yt_page_fm, text="CHOOSE A RESOLUTION")
    resLabel.pack(padx=10, pady=10)
    rCombobox = ctk.CTkComboBox(yt_page_fm, state="readonly", width=200)
    rCombobox.set("None")
    rCombobox.pack()

    # finished Downloading label
    finishLabel = ctk.CTkLabel(yt_page_fm, text="")
    finishLabel.pack()

    # progress percentage
    pPercentage = ctk.CTkLabel(yt_page_fm, text="0%")
    pPercentage.pack()

    progressBar = ctk.CTkProgressBar(yt_page_fm, width=400)
    progressBar.set(0)
    progressBar.pack(padx=10, pady=10)

    # fetch button
    fetch = ctk.CTkButton(yt_page_fm, text="Fetch Detail", command=video_details)
    fetch.pack(padx=20, pady=10)

    # download button
    download = ctk.CTkButton(yt_page_fm, text="Download", command=startDownload)
    download.pack(padx=20, pady=10)
    yt_page_fm.pack(fill=tk.BOTH, expand=True)


def file_page():
    file_page_fm = ctk.CTkFrame(main_fm, fg_color="transparent")

    # function to organise the desktop

    def Organise():
        folder_name = Olink.get()

        # Get the user's desktop path
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        if folder_name.lower() == "desktop":
            folder_path = desktop_path
        else:
            # Possible folder paths
            possible_paths = [
                os.path.join(os.path.expanduser("~"), folder_name),
                os.path.join(desktop_path, folder_name),
                os.path.join(os.path.expanduser("~"), "Documents", folder_name),
                os.path.join(os.path.expanduser("~"), "Downloads", folder_name),
                os.path.join("C:\\", folder_name),
            ]

            # Find the actual folder path
            folder_path = next((path for path in possible_paths if os.path.exists(path)), None)

        if folder_path:
            try:
                # Organize files in the folder
                for filename in os.listdir(folder_path):
                    if os.path.isfile(os.path.join(folder_path, filename)):
                        file_extension = os.path.splitext(filename)[1][1:]
                        new_folder_path = os.path.join(folder_path, file_extension)

                        if not os.path.exists(new_folder_path):
                            os.makedirs(new_folder_path)

                        shutil.move(os.path.join(folder_path, filename), new_folder_path)
                        Organize_label.configure(text="Successful")
            except Exception as e:
                Organize_label.configure(text=f"{e}", wraplength=300)
        else:
            Organize_label.configure(text=f"Folder '{folder_name}' not found")

    # design the ui
    fileLABEL = ctk.CTkLabel(file_page_fm, text='ENTER FOLDER TO ORGANIZE', font=('Arial', 13))
    fileLABEL.pack(padx=20, pady=10)

    # design the entry box
    url_var = tkinter.StringVar()
    Olink = ctk.CTkEntry(file_page_fm, width=350, height=40, textvariable=url_var)
    Olink.pack()

    # organize label
    Organize_label = ctk.CTkLabel(file_page_fm, text="", font=('Arial', 13))
    Organize_label.pack()
    # organize button
    download = ctk.CTkButton(file_page_fm, text="Organise", command=Organise)
    download.pack(padx=20, pady=10)
    file_page_fm.pack(fill=tk.BOTH, expand=True)

    file_page_fm.pack(fill=tk.BOTH, expand=True)


def extractor_page():
    extractor_page_fm = ctk.CTkFrame(main_fm, fg_color="transparent")

    def select_pdf():
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            ExtractEntry.delete(0, "end")
            ExtractEntry.insert(0, file_path)

    def extract_pdf():
        file_path = ExtractEntry.get()

        if not file_path.endswith('.pdf'):
            messagebox.showerror("Extract Error", "Please select a valid PDF File.")
            return

        try:
            doc = fitz.open(file_path)
            extracted_text = ""

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                extracted_text += page.get_text("text")
                display_extracted_text(extracted_text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_extracted_text(text):
        extractOutput.delete(1.0, "end")
        extractOutput.insert("end", text)

    # define the ui
    extractLabel = ctk.CTkLabel(extractor_page_fm, text='PDF EXTRACTOR', font=('Arial', 13))
    extractLabel.pack()
    # to note the directory
    ExtractEntry = ctk.CTkEntry(extractor_page_fm, placeholder_text="SELECT A PDF", width=350,
                                height=20, border_width=0)
    ExtractEntry.pack(padx=20, pady=10)
    # textbox to house the extracted text
    extractOutput = ctk.CTkTextbox(extractor_page_fm, width=500, height=200, wrap='none')
    extractOutput.pack(padx=20, pady=10)
    # the buttons
    extractButton = ctk.CTkButton(extractor_page_fm, text="Extract PDF", command=extract_pdf)
    extractButton.pack(side="right", padx=20, pady=10)

    selectButton = ctk.CTkButton(extractor_page_fm, text="Select PDF", command=select_pdf)
    selectButton.pack(side="left", padx=20, pady=10)

    extractor_page_fm.pack(fill=tk.BOTH, expand=True)


main_fm = ctk.CTkFrame(app, fg_color="transparent")
main_fm.pack(fill=tk.BOTH, expand=True)

yt_page()
app.mainloop()
