from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
import collage_color_sort as ccs

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

def get_input_path():
    path = askdirectory(title="Select Folder")
    return path

def generate_output(col_amt, border_width, transparent):
    selected_path = get_input_path()
    if col_amt > 0 and border_width > -1:
        ccs.generate_collage(int(col_amt), int(border_width), transparent, selected_path)
    else:
        print("Error")


# Create main tkinter window
root = Tk()
app = Window(root)
root.wm_title("Collage Color Sort")
root.geometry("400x120")
root.resizable(False, False)
#root.tk.call('lappend', 'auto_path', '/full/path/to/awthemes-9.3.1')
#root.tk.call('package', 'require', 'awdark')

# Configure label style
ttk.Style().configure("BW.TLabel", fontforeground="black", font=("Segoe UI", "11"))
ttk.Style().configure("BW.TButton", font=("Segoe UI", "9"))
ttk.Style().configure("BW.TCheckbutton", font=("Segoe UI", "10"))

# Create main frame to contain widgets
mainframe = ttk.Frame(root, padding="8")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

# Configure columns
root.grid_columnconfigure(0, weight=1)
mainframe.grid_columnconfigure(0, weight=4, uniform="col_group")
mainframe.grid_columnconfigure(1, weight=6, uniform="col_group")

# Add columns amount label + text entry
ttk.Label(mainframe, text="Columns: ", anchor="e", style="BW.TLabel").grid(column=0, row=0, sticky=(W, E))
col_amt = StringVar()
col_amt_entry = ttk.Entry(mainframe, textvariable=col_amt)
col_amt_entry.grid(column=1, row=0, sticky=(W, E))

# Add border width label + text entry
ttk.Label(mainframe, text="Border width: ", anchor="e", style="BW.TLabel").grid(column=0, row=1, sticky=(W, E))
border_width = StringVar()
border_width_entry = ttk.Entry(mainframe, textvariable=border_width)
border_width_entry.grid(column=1, row=1, sticky=(W, E), pady="12")

# Add transparent option checkbox
transparent_output = IntVar(value=0)
chkbtn_transparent = ttk.Checkbutton(mainframe, text="Transparent", style="BW.TCheckbutton", variable=transparent_output)
chkbtn_transparent.grid(column=1, row=2, sticky=(W))

# Add generate button
btn_generate = ttk.Button(mainframe, text="Generate", width="20", command=lambda: generate_output(int(col_amt.get()), int(border_width.get()), transparent_output))
btn_generate.grid(column=1, row=2, sticky=(S, E))

# Show window
root.mainloop()