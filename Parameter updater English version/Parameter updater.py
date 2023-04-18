import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import filedialog, messagebox
from tkinter import filedialog, messagebox, Toplevel
import configparser
import webbrowser

config = configparser.ConfigParser()
config.read('config_eng.ini')

# Create a tkinter window
root = tk.Tk()
root.title("Tool Updater")
root.geometry("610x620")

measurement_file = None
csv_fusion_file_path = None
global body_length_letter
global flute_length_letter
body_length_letter = 'P'
flute_length_letter = 'BD'


# Function to select the measurement file
def select_measurement_file():
    global measurement_file
    if measurement_file:
        answer = messagebox.askyesno("Warning", "You have already selected a csv file. Do you want to overwrite it and select another file?")
        if answer:
                measurement_file = filedialog.askopenfilename(title="Select CSV File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
                console.configure(state='normal')
                console.insert('end',"\nMeasurement file: " + measurement_file + '\n')
                console.configure(state='disabled')
    else:
        measurement_file = filedialog.askopenfilename(title="Select Original File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
        console.configure(state='normal')
        console.insert('end', "\nMeasurement to be read: " + measurement_file + '\n')
        console.configure(state='disabled')

# Function to select the csv file
def select_csv_to_fusion_file():
    global csv_fusion_file_path
    if csv_fusion_file_path:
        answer = messagebox.askyesno("Warning", "You have already selected a csv file. Do you want to overwrite it and select another file?")
        if answer:
                csv_fusion_file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
                console.configure(state='normal')
                console.insert('end',"\nFusion file: " + csv_fusion_file_path + '\n')
                console.configure(state='disabled')
    else:
        csv_fusion_file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
        console.configure(state='normal')
        console.insert('end',"\nFusion file to be updated: " + csv_fusion_file_path + '\n')
        console.configure(state='disabled')

# Function to start the process
# Function to start the process
def tool_data_updater():
    console.tag_configure("green", foreground="green")
    console.tag_configure("red", foreground="red")
    tool_number_from_fusion_file = config.get('DEFAULT', 'tool_number_from_fusion_file')
    radius_letter = config.get('DEFAULT', 'radius_letter')
    length_letter = config.get('DEFAULT', 'length_letter')
    tool_number_measurement = config.get('DEFAULT', 'tool_number_measurement')
    tool_length_measurement = config.get('DEFAULT', 'tool_length_measurement')
    tool_radius_measurement = config.get('DEFAULT', 'tool_radius_measurement')

    # Open the CSV file
    with open(csv_fusion_file_path, newline='') as csvfile:
        # Create a csv reader object
        reader = csv.reader(csvfile)
        # Skip the header row
        next(reader)
        default_tool_number_from_fusion_file = "F"
        # Check if the tool_number_from_fusion_file variable has been updated in the settings window
        if tool_number_from_fusion_file != default_tool_number_from_fusion_file:
            column_number = ord(tool_number_from_fusion_file) - ord('A') + 1
        elif tool_number_from_fusion_file == default_tool_number_from_fusion_file:
            column_number = ord(default_tool_number_from_fusion_file) - ord('A') + 1


        # Extract the values in the sixth column (column F) and their corresponding row numbers
        column_values = {}
        for i, row in enumerate(reader):
            column_values.setdefault(row[column_number-1], []).append(i + 2)
        # Open the original file
    with open(measurement_file, "r+") as fo:
        default_tool_number_measurement = "A"
        default_tool_length_measurement = "C"
        default_tool_radius_measurement = "D"
        #column_number123123 = ord(tool_number_measurement) - ord('A') + 1
        fo.readline()

        # loop through the remaining lines and process them
        for line in fo:
            values = line.split(',')
            if tool_number_measurement != default_tool_length_measurement:
                tool_number = values[ord(tool_number_measurement) - ord('A')]
            elif tool_number_measurement == default_tool_length_measurement:
                tool_number = values[ord(default_tool_number_measurement) - ord('A')]
            if tool_length_measurement != default_tool_length_measurement:
                tool_length = values[ord(tool_length_measurement) - ord('A')]
            elif tool_length_measurement == default_tool_length_measurement:
                tool_length = values[ord(default_tool_length_measurement) - ord('A')]
            if tool_radius_measurement != default_tool_radius_measurement:
                tool_radius = values[ord(tool_radius_measurement) - ord('A')]
            elif tool_radius_measurement == default_tool_radius_measurement:
                tool_radius = values[ord(default_tool_radius_measurement) - ord('A')]
            console.configure(state='normal')
            console.insert(tk.END, "Tool number: " + tool_number + "\nTool length: " + tool_length + "\nTool radius: " + tool_radius + "\n")
            console.configure(state='disabled')
            # Check if the value exists in the column
            if tool_number in column_values:
                console.configure(state='normal')
                console.insert(tk.END, tool_number + " exists in the fusion file\n", "green")
                console.configure(state='disabled')
                row_numbers = column_values[tool_number]
                with open(csv_fusion_file_path, 'r+', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    rows = list(reader)
                    default_radius_letter = "E"
                    if radius_letter != default_radius_letter:
                        column_number_radius = ord(radius_letter) - ord('A')
                    elif radius_letter == default_radius_letter:
                        column_number_radius = ord(default_radius_letter) - ord('A')
                    default_length_letter = "CE"
                    if length_letter != default_length_letter:
                        column_number_length = (ord(length_letter[0]) - ord('A') + 1) * 26 + (ord(length_letter[1]) - ord('A') + 1)
                    elif length_letter == default_length_letter:
                        column_number_length = (ord(length_letter[0]) - ord('A') + 1) * 26 + (ord(default_length_letter[1]) - ord('A') + 1)
                    column_number_body_length = ord(body_length_letter) - ord('A')
                    column_number_flute_length = (ord(flute_length_letter[0]) - ord('A') + 1) * 26 + (ord(flute_length_letter[1]) - ord('A'))
                    for row_number in row_numbers:
                        rows[row_number-1][column_number_radius] = float(tool_radius)* 2
                        rows[row_number-1][column_number_length-1] = tool_length
                        rows[row_number-1][column_number_body_length] = None # 15 is the column number for P
                        rows[row_number-1][column_number_flute_length] = None # 54 is the column number for BD
                    csvfile.seek(0)
                    writer =csv.writer(csvfile)
                    writer.writerows(rows)
                    csvfile.truncate() 
            else:
                console.configure(state='normal')
                console.insert(tk.END, tool_number + " does not exist in the fusion file\n", "red")
                console.configure(state='disabled')
                # Ask the user if they want to continue
                answer = messagebox.askyesno("Tool Missing ", "Tool " + tool_number + " is missing in the Fusion file. Do you want to continue?\n")
                if not answer:
                    console.configure(state='normal')
                    console.insert(tk.END, "Process terminated by user.\n")
                    console.configure(state='disabled')
                    return
     
        console.configure(state='normal')
        console.insert(tk.END, "Process complete!")
        console.configure(state='disabled')

def settings_window():

    def manual_letter_change():
        global tool_number_from_fusion_file
        global radius_letter
        global length_letter
        global tool_number_measurement
        global tool_length_measurement
        global tool_radius_measurement
        tool_number_from_fusion_file = tool_number_fusion_entry.get()
        radius_letter =  radius_letter_entry.get()
        length_letter = length_letter_entry.get()
        tool_number_measurement = tool_number_measurement_letter_entry.get()
        tool_length_measurement = length_measurement_letter_entry.get()
        tool_radius_measurement = radius_measurement_letter_entry.get()
        # Save the values to a configuration file or a database for persistence
        with open("config_eng.ini", "w") as f:
            f.write(f"tool_number_from_fusion_file={tool_number_from_fusion_file}\n")
            f.write(f"radius_letter={radius_letter}\n")
            f.write(f"length_letter={length_letter}\n")
            f.write(f"tool_number_measurement={tool_number_measurement}\n")
            f.write(f"tool_length_measurement={tool_length_measurement}\n")
            f.write(f"tool_radius_measurement={tool_radius_measurement}\n")
            
        settings_window.destroy()

    # Create a new settings window
    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("500x425")

    # Create a label and an input field for tool_number_from_fusion_file
    tool_number_fusion_entry_text = tk.StringVar()
    tool_number_fusion_label = tk.Label(settings_window, text="Column of the tool number in the fusion file (Default: F):")
    tool_number_fusion_label.grid(row=0, column=0)
    tool_number_fusion_entry = tk.Entry(settings_window, width=10, textvariable=tool_number_fusion_entry_text)
    tool_number_fusion_entry.grid(row=1, column=0, sticky="w", padx=10, pady=10)

    def update_tool_number_from_fusion_file():
        new_value = tool_number_fusion_entry_text.get()
        config['DEFAULT']['tool_number_from_fusion_file'] = new_value
        with open('config_eng.ini', 'w') as config_file:
            config.write(config_file)
        tool_number_fusion_entry.delete(0, tk.END)
        tool_number_fusion_entry.insert(0, new_value)  

    tool_number_fusion_entry.insert(0, config['DEFAULT']['tool_number_from_fusion_file'])
    # Create a button to update the tool_number_from_fusion_file
    update_button = tk.Button(settings_window, text="Change letter", command=update_tool_number_from_fusion_file)
    update_button.grid(row=1, column=0, sticky="w", padx=80, pady=10)


    # Create a label and an input field for radius_letter
    radius_letter_entry_text = tk.StringVar()
    radius_letter_label = tk.Label(settings_window, text="Column of the diameter letter (Default: E):")
    radius_letter_label.grid(row=2, column=0, sticky="w")
    radius_letter_entry = tk.Entry(settings_window, width=10, textvariable=radius_letter_entry_text)
    radius_letter_entry.grid(row=3, column=0,sticky="w", padx=10,pady=10)

    def update_radius_letter():
        new_value = radius_letter_entry_text.get()
        config['DEFAULT']['radius_letter'] = new_value
        with open('config_eng.ini', 'w') as config_file:
            config.write(config_file)
        radius_letter_entry.delete(0, tk.END)
        radius_letter_entry.insert(0, new_value)

    radius_letter_entry.insert(0, config['DEFAULT']['radius_letter'])
    # Create a button to update the radius_letter
    update_button = tk.Button(settings_window, text="Change letter", command=update_radius_letter)
    update_button.grid(row=3, column=0,sticky="w", padx=80,pady=10)


    # Create a label and an input field for length_letter
    length_letter_entry_text = tk.StringVar()
    length_letter_label = tk.Label(settings_window, text="Column of the tool length letter (Default: CE):")
    length_letter_label.grid(row=4, column=0, sticky="w")
    length_letter_entry = tk.Entry(settings_window, width=10, textvariable=length_letter_entry_text)
    length_letter_entry.grid(row=5, column=0,sticky="w", padx=10,pady=10)
    def update_length_letter():
        new_value = length_letter_entry_text.get()
        config['DEFAULT']['length_letter'] = new_value
        with open('config_eng.ini', 'w') as config_file:
            config.write(config_file)
        length_letter_entry.delete(0, tk.END)
        length_letter_entry.insert(0, new_value)

    length_letter_entry.insert(0, config['DEFAULT']['length_letter'])
    # Create a button to update the length_letter
    update_button = tk.Button(settings_window, text="Change letter", command=update_length_letter)
    update_button.grid(row=5, column=0,sticky="w", padx=80,pady=10)

    # Create a label and an input field for tool number from the measurement file
    tool_number_measurement_letter_entry_text = tk.StringVar()
    tool_number_measurement_letter_label = tk.Label(settings_window, text="Column of the tool number in the Tooltable file (default: A)")
    tool_number_measurement_letter_label.grid(row=6, column=0, sticky="w")
    tool_number_measurement_letter_entry = tk.Entry(settings_window, width=10, textvariable=tool_number_measurement_letter_entry_text)
    tool_number_measurement_letter_entry.grid(row=7, column=0,sticky="w", padx=10,pady=10)

    def update_tool_number_measurement():
        new_value = tool_number_measurement_letter_entry_text.get()
        config['DEFAULT']['tool_number_measurement'] = new_value
        with open('config_eng.ini', 'w') as config_file:
            config.write(config_file)
        tool_number_measurement_letter_entry.delete(0, tk.END)
        tool_number_measurement_letter_entry.insert(0, new_value)

    tool_number_measurement_letter_entry.insert(0, config['DEFAULT']['tool_number_measurement'])

    # Create a button to update the tool number from the measurement file
    update_button = tk.Button(settings_window, text="Change letter", command=update_tool_number_measurement)
    update_button.grid(row=7, column=0,sticky="w", padx=80,pady=10)


    # Create a label and an input field for tool length from the measurement file
    length_measurement_letter_entry_text = tk.StringVar()
    length_measurement_letter_label = tk.Label(settings_window, text="Column of the tool length in the Tooltable file (default: C)")
    length_measurement_letter_label.grid(row=8, column=0, sticky="w")
    length_measurement_letter_entry = tk.Entry(settings_window, width=10, textvariable=length_measurement_letter_entry_text)
    length_measurement_letter_entry.grid(row=9, column=0,sticky="w", padx=10,pady=10)

    def update_length_measurement_letter():
        new_value = length_measurement_letter_entry_text.get()
        config['DEFAULT']['tool_length_measurement'] = new_value
        with open('config_eng.ini', 'w') as config_file:
            config.write(config_file)
        length_measurement_letter_entry.delete(0, tk.END)
        length_measurement_letter_entry.insert(0, new_value)

    # Set the initial value of the input field
    length_measurement_letter_entry.insert(0, config['DEFAULT']['tool_length_measurement'])

    # Create a button to update the tool length from the measurement file
    update_button = tk.Button(settings_window, text="Change letter", command=update_length_measurement_letter)
    update_button.grid(row=9, column=0,sticky="w", padx=80,pady=10)

    # Create a label and an input field for tool radius from the measurement file
    radius_measurement_letter_entry_text = tk.StringVar()
    radius_measurement_letter_label = tk.Label(settings_window, text="Column of the tool radius in the Tooltable file (default: D)")
    radius_measurement_letter_label.grid(row=10, column=0, sticky="w")
    radius_measurement_letter_entry = tk.Entry(settings_window, width=10, textvariable=radius_measurement_letter_entry_text)
    radius_measurement_letter_entry.grid(row=11, column=0,sticky="w", padx=10,pady=10)

    def update_radius_measurement_letter():
        new_value = radius_measurement_letter_entry_text.get()
        config['DEFAULT']['tool_radius_measurement'] = new_value
        with open('config_eng.ini', 'w') as config_file:
            config.write(config_file)
        radius_measurement_letter_entry.delete(0, tk.END)
        radius_measurement_letter_entry.insert(0, new_value)

    # Set the initial value of the input field
    radius_measurement_letter_entry.insert(0, config['DEFAULT']['tool_radius_measurement'])

    # Create a button to update the tool radius from the measurement file
    update_button = tk.Button(settings_window, text="Change letter", command=update_radius_measurement_letter)
    update_button.grid(row=11, column=0,sticky="w", padx=80,pady=10)

    def info_window():
        # Create a new window
        info_window = tk.Toplevel(root)
        info_window.geometry("200x150")
        info_window.title("Info")
        made_by_label = tk.Label(info_window, text="Made by: IINS21, 2023")
        made_by_label.grid(row=1, column=0, sticky="w", pady=30, padx=20)
        link_label = tk.Label(info_window, text="Source code", fg="blue", cursor="hand2")
        link_label.grid(row=2, column=0, sticky="w", pady=5,padx=20)
        def callback(url):
            webbrowser.open_new_tab(url)
        link_label.bind("<Button-1>", lambda e:
        callback("https://github.com/eetuhenri/Tool-parameter-updater-for-Fusion-360"))




    reminder_label = tk.Label(settings_window, text="Remember to input capital letters", font=("Arial",8))
    reminder_label.grid(row=13, column=0, sticky="w", pady=0, padx=(0,0))

    
    info_button = tk.Button(settings_window, text="Info", command=info_window)
    info_button.grid(row=13, column=2, sticky="e", pady=2, padx=(140,0))


original_file_button = tk.Button(root, text="Select measurement file", command=select_measurement_file)
original_file_button.grid(row=0, column=0, padx=5, pady=(1,10), sticky="w")

csv_file_button = tk.Button(root, text="Select Fusion File", command=select_csv_to_fusion_file)
csv_file_button.grid(row=1, column=0, padx=5, pady=1, sticky="w", ipadx=16)


process_button = tk.Button(root, text="Start updating", command=tool_data_updater)
process_button.grid(row=6, column=0, pady=20,padx=(200,0), sticky="e")

settings_button = tk.Button(root, text="Settings", command=settings_window)
settings_button.grid(row=7, column=1, pady=20, padx=(0, 80), sticky="e")


console = tk.Text(root, height=30, width=45)
console.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")
console.configure(state='normal')
console.insert('end',"Remember to close any excel files that are open that are needed for this process" + '\n')
console.configure(state='disabled')

root.iconbitmap("kuvake.ico")

root.mainloop()
