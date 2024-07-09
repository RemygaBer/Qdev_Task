from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askquestion
from tkinter import Tk
import sys


class Color:  # Defines a color object to store its parameters
    def __init__(self, name):
        self.name = name
        self.count = 0
        self.total_time = 0
        self.activation_times = []


def read_file():  # GUI for getting data file location
    filename = None
    Tk().withdraw()
    try:
        filename = askopenfilename(title="Select data file")
    except Exception as e:
        print(f"Error: {e}")
    return filename


def ask_export():  # GUI for getting exported file location
    filename = None
    Tk().withdraw()
    answer = askquestion("Save results to file?", "Save results to a separate file?")
    if answer == "yes":
        try:
            filename = asksaveasfilename(defaultextension=".txt",
                                         filetypes=(("txt files", "*.txt"), ("all files", "*.*")),
                                         initialfile="Results")
        except Exception as e:
            print(f"Error: {e}")
    return filename


def read_first_line(file_path):  # Reading the first column and extracting color names and positions
    colours = []
    try:
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
            titles = first_line.split(',')
            if len(titles) == 5:
                for i in range(3):
                    colours.append(Color(titles[i]))
                return colours
            else:
                raise ValueError("Wrong data provided!")
    except Exception as e:
        raise e


class CalculatorTools:  #  Class for storing calculation tools

    def __init__(self, colors):
        self.colors = colors
        self.streak_order = [0, 1, 2, 1, 0]  # Sequence logic
        self.streak_pos = 0
        self.streak_total = 0

    def streak_manager(self, line):  # A given line is checked and compared to the current sequence position
        for i in range(3):
            if int(line[i]) == 1:
                if i == self.streak_order[self.streak_pos]:
                    self.streak_pos += 1
                    break
                else:
                    self.streak_pos = 0
                    break
            else:
                continue
        if self.streak_pos == 5:
            self.streak_pos = 1
            self.streak_total += 1
        return

    def plus_count(self, line):  # adding count, total time and appearance time to the color objects
        for i in range(3):
            if int(line[i]) == 1:
                self.colors[i].count += 1
                self.colors[i].total_time += int(line[3])
                self.colors[i].activation_times.append(line[4])
            else:
                continue

    @staticmethod
    def error_check(line):  # Checking for errors in line, if the sum of first 3 values is not 1 - error is counted
        data = line[0:3]
        data = [int(x) for x in data]
        if sum(data) == 1:
            return False
        else:
            return True


def calculate(file, colors) -> tuple[list, int, int]:  # main process for running calculation tools
    errors = 0
    tools = CalculatorTools(colors)
    with open(file, "r") as text_file:  # Opening data file
        data = text_file.readlines()  # Reading all lines
        data.pop(0)  # Removing header line
    for i in range(len(data)):
        line = data[i].rstrip()  # Removing "/n"
        line_data = line.split(',')  # Splitting into a list
        if tools.error_check(line_data):  # skipping lines if more or less than 1 color is on
            errors += 1
            continue
        tools.plus_count(line_data)  # Counting color data
        tools.streak_manager(line_data)  # Counting streaks
    new_colors = tools.colors  # Getting altered color objects
    streaks = tools.streak_total  # Getting counted streaks
    return new_colors, errors, streaks


def print_results(results, errors, streaks):  # Printing results to command window and a file if needed
    original_stdout = None
    filename = ask_export()
    if filename:
        original_stdout = sys.stdout
        try:
            sys.stdout = open(filename, 'w')
        except Exception as e:
            print(f"Error: {e}")

    print("1. LIGHT OCCURANCES:\n")
    for i in range(3):
        print(f"{results[i].name} light appears {results[i].count} time(s)")
    print("\n2. TIME ACTIVE:\n")
    for i in range(3):
        print(f"{results[i].name} light was active for {results[i].total_time} second(s))")
    print("\n3. GREEN ACTIVATION:\n")
    for i in range(3):
        if results[i].name == "Green":
            print(f"The color green was activated at these times:\n")
            for time in results[i].activation_times:
                print(f"{time}, ", end='')
            break
    print("\n\n4. FULL CYCLES:\n")
    print(f"The total number of full light cycles is - {streaks}")
    print("\n5. ERROR LINES:\n")
    print(f"The total number of lines with mistakes is - {errors}")
    if filename:
        sys.stdout = original_stdout
        with open(filename, "r") as log:
            print(log.read())
        log.close()


def main():
    full_cycles = 0
    data_file = read_file()
    if data_file:
        try:
            colors = read_first_line(data_file)
        except Exception as e:
            print(f"Wrong file selected.\nError: {e}")
            return
    else:
        print("No file was selected")
        return
    print_results(*calculate(data_file, colors))


if __name__ == "__main__":
    main()
    print("\nPress any key to quit")
    input()
