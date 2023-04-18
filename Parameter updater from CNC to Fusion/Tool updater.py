import csv
import tkinter as tk
from tkinter import filedialog
import csv

# Create a tkinter window
root = tk.Tk()
root.title("Tool Updater")

# Function to select the original file
def select_original_file():
    global original_file_path
    original_file_path = filedialog.askopenfilename(title="Select Original File", filetypes=(("Text Files", "*.t"), ("All Files", "*.*")))
    console.configure(state='normal')
    console.insert('end', original_file_path + '\n')
    console.configure(state='disabled')

# Function to select the csv file
def select_csv_file():
    global csv_file_path
    csv_file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))
    console.configure(state='normal')
    console.insert('end', csv_file_path + '\n')
    console.configure(state='disabled')
# Function to start the process
def start_process():
    # ANSI escape codes for color formatting
    GREEN = '\033[32m'
    RED = '\033[31m'
    RESET = '\033[0m'

    # Open the CSV file
    with open(csv_file_path) as csvfile:
        # Create a csv reader object
        reader = csv.reader(csvfile)

        # Skip the header row
        next(reader)

        # Convert column letter to column number
        column_letter = 'F'
        column_number = ord(column_letter) - ord('A') + 1

        # Extract the values in the sixth column (column F) and their corresponding row numbers
        column_values = {}
        for i, row in enumerate(reader):
            column_values[row[column_number-1]] = i + 2  # add 2 to account for header row and 0-based indexing

    # Open the original file
    with open(original_file_path, "r+") as fo:
        # discard the first three lines
        fo.readline()
        fo.readline()
        fo.readline()

        # loop through the remaining lines and process them
        for line in fo:
            values = line.split()
            tool_number = values[0]
            tool_length = values[2]
            tool_radius = values[3]
            console.configure(state='normal')
            console.insert(tk.END, "Tool number: " + tool_number + "\nTool length: " + tool_length + "\nTool radius: " + tool_radius + "\n")
            console.configure(state='disabled')
            # Check if the value exists in the column
            if tool_number in column_values:
                console.configure(state='normal')
                console.insert(tk.END, GREEN + tool_number + " exists in the csv file" + RESET + "\n")
                console.configure(state='disabled')
                # Update the corresponding cell in column H with the tool length
                row_number = column_values[tool_number]
                with open(csv_file_path, 'r+', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    writer = csv.writer(csvfile)
                    rows = list(reader)
                    radius_letter = 'E'
                    rows[row_number-1][ord(radius_letter)-ord('A')] = tool_radius
                    csvfile.seek(0)
                    writer.writerows(rows)
                    csvfile.truncate()
                    length_letter = 'CE'
                    column_number = (ord(length_letter[0]) - ord('A') + 1) * 26 + (ord(length_letter[1]) - ord('A') + 1)
                    # Update the corresponding cell in column CE with the tool length
                    rows[row_number-1][column_number-1] = tool_length
                    csvfile.seek(0)
                    writer.writerows(rows)
                    csvfile.truncate()
            else:
                console.configure(state='normal')
                console.insert(tk.END, RED + tool_number + " does not exist in the column" + RESET + "\n")
                console.configure(state='disabled')
# Create the buttons
original_file_button = tk.Button(root, text="Select Original File", command=select_original_file)
csv_file_button = tk.Button(root, text="Select CSV File", command=select_csv_file)

start_button = tk.Button(root, text="Start Process", command=start_process)

console = tk.Text(root, height=20, width=80)
console.configure(state='normal')

original_file_button.grid(row=0, column=0, padx=10, pady=10)
csv_file_button.grid(row=0, column=1, padx=10, pady=10)
start_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
console.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
