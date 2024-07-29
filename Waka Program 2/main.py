import os
import customtkinter as ct
from tkinter import messagebox, filedialog
import csv
import tkinter as tk
from datetime import datetime

class ProgramFunctions:
    def __init__(self):
        self.main_folder = ""
        self.year_select = ""
        self.keyword = ""

    def check_inputs_is_valid(self):
        if self.check_parent_folder_is_valid() == True:
            return self.check_year_select_is_valid() if self.check_year_select_is_valid() != True else True
        return self.check_parent_folder_is_valid()

    def check_parent_folder_is_valid(self):
        try:
            parent_folder_items = os.listdir(self.main_folder)
        except:
            return "Select a folder"
        if not parent_folder_items:
            return f"No items inside {self.main_folder}"
        return True if any("WakaNats" in item for item in parent_folder_items) else f"No WakaNats inside {self.main_folder}"

    def check_year_select_is_valid(self):
        if not self.year_select.isdigit():
            return f"{self.year_select} is not a year"
        all_available_years = [folder[-4:] for folder in self.get_all_wakanats()]
        return True if self.year_select in all_available_years else f"The year {self.year_select} is not available"

    def get_all_wakanats(self):
        return [item for item in os.listdir(self.main_folder) if "WakaNats" in item]

    def get_year_select_files(self):
        year_path = os.path.join(self.main_folder, f"WakaNats{self.year_select}")
        year_files = os.listdir(year_path)
        return year_files if year_files else f"{self.year_select} has no files inside"

    def find_lif_files(self, year_files):
        lif_files = [file for file in year_files if file.endswith('.lif')]
        if not lif_files:
            return f"No lif files are found in {self.year_select}"
        if self.keyword:
            lif_files_with_keyword = [file for file in lif_files if self.keyword.lower() in file.lower()]
            return lif_files_with_keyword if lif_files_with_keyword else f"There are no lif files with the keyword {self.keyword}"
        return lif_files

    def read_n_categorize_file(self, lif_file):
        file_path = os.path.join(self.main_folder, f"WakaNats{self.year_select}", lif_file)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            header = lines.pop(0).strip().split(',')

            if len(header) < 5:
                return f"{lif_file} has an error in race information: {header}."

            lif_teams = []
            for line in lines:
                if any(status in line for status in ["DQ", "DNS", "Disqualified"]):
                    continue
                
                cleaned_line = [item.strip() for item in line.strip().split(',') if item.strip()]
                if len(cleaned_line) < 6:
                    return f"{lif_file} has an error on team line: {line.strip()}."

                team_id, team_place, team_name, team_regional_association = cleaned_line[0], cleaned_line[1], cleaned_line[4], cleaned_line[5]
                if not team_place.isdigit() or team_name.isdigit() or team_regional_association.isdigit():
                    return f"{lif_file} has an error on team line: {line.strip()}."

                lif_teams.append([team_id, team_place, team_name, team_regional_association])

        return lif_teams

    def get_all_scores(self, lif_files_contents_dir):
        regional_association_scores = {}
        for teams_list in lif_files_contents_dir.values():
            for team in teams_list:
                team_place, team_regional_association = int(team[1]), team[3]
                team_score = 9 - team_place if team_place < 8 else 1
                regional_association_scores[team_regional_association] = regional_association_scores.get(team_regional_association, 0) + team_score
        return regional_association_scores

    def sort_descending(self, regional_association_results):
        return dict(sorted(regional_association_results.items(), key=lambda item: item[1], reverse=True))

class GUIComponent:
    def __init__(self):
        self.root = ct.CTk()
        self.root.geometry("700x600")
        self.setup_constants()
        self.setup_root()
        self.program_functions = ProgramFunctions()
        self.home_screen()

    def setup_constants(self):
        self.SCALE_CONSTANT = 1.5
        self.FONT_BASE_CONSTANT = 20 / self.SCALE_CONSTANT
        self.title_font = ct.CTkFont(size=int(self.FONT_BASE_CONSTANT * self.SCALE_CONSTANT), weight="bold")

    def setup_root(self):
        ct.set_window_scaling(self.SCALE_CONSTANT * 0.4)
        ct.set_widget_scaling(self.SCALE_CONSTANT * 0.9)
        ct.set_appearance_mode("light")
        ct.set_default_color_theme("green")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

    def home_screen(self):
        self.remove_current_screen()
        homepage_frame = self.create_homepage_frame()
        self.create_title(homepage_frame)
        inner_frame = self.create_inner_frame(homepage_frame)
        self.create_input_fields(inner_frame)

    def create_homepage_frame(self):
        homepage_frame = ct.CTkFrame(self.root)
        homepage_frame.grid(row=0, column=0, sticky="NSEW")
        homepage_frame.rowconfigure(0, weight=1)
        homepage_frame.rowconfigure(1, weight=1)
        homepage_frame.columnconfigure(0, weight=1)
        return homepage_frame

    def create_title(self, parent):
        title_label = ct.CTkLabel(parent, text="Waka Ama leaderboard system", font=self.title_font)
        title_label.grid(row=0, column=0, sticky="nsew")

    def create_inner_frame(self, parent):
        inner_frame = ct.CTkFrame(parent)
        inner_frame.grid(row=1, column=0, sticky="nsew")
        for i in range(3):
            inner_frame.rowconfigure(i, weight=1)
            inner_frame.columnconfigure(i, weight=1)
        return inner_frame

    def create_input_fields(self, parent):
        self.parent_folder_button = ct.CTkButton(parent, text="Open folder", command=self.pick_folder)
        self.parent_folder_button.grid(row=0, column=0)
        self.keyword_input = ct.CTkEntry(parent, placeholder_text="Type keyword")
        self.keyword_input.grid(row=1, column=0)
        self.year_input = ct.CTkEntry(parent, placeholder_text="Type year")
        self.year_input.grid(row=2, column=0)
        self.save_to_csv_var = tk.BooleanVar(value=True)
        self.save_to_csv_switch = ct.CTkSwitch(parent, text="Save to CSV", variable=self.save_to_csv_var)
        self.save_to_csv_switch.grid(row=1, column=1)
        proceed_button = ct.CTkButton(parent, text="Proceed", command=self.loading_screen)
        proceed_button.grid(row=2, column=1)

    def loading_screen(self):
        year = self.year_input.get()
        keyword = self.keyword_input.get()
        self.remove_current_screen()
        loading_frame = ct.CTkFrame(self.root)
        loading_frame.grid()
        loading_title_label = ct.CTkLabel(loading_frame, text=f"Loading {year} {keyword}")
        loading_title_label.grid()
        self.loading_file_label = ct.CTkLabel(loading_frame, text="Processing...")
        self.loading_file_label.grid()
        self.loading_progressbar = ct.CTkProgressBar(loading_frame)
        self.loading_progressbar.grid()
        self.loading_progressbar.start()
        self.root.after(100, lambda: self.loading_process(year, keyword))

    def error(self, title, message):
        messagebox.showerror(title=title, message=message)

    def success(self, title, message):
        messagebox.showinfo(title=title, message=message)

    def loading_process(self, year, keyword):
        try:
            self.program_functions.year_select = year
            self.program_functions.keyword = keyword
            validation_result = self.program_functions.check_inputs_is_valid()
            if validation_result is not True:
                self.error("Input Error", validation_result)
                self.home_screen()
                return

            year_files = self.program_functions.get_year_select_files()
            if isinstance(year_files, str):
                self.error("Year Files Error", year_files)
                self.home_screen()
                return

            lif_files = self.program_functions.find_lif_files(year_files)
            if isinstance(lif_files, str):
                self.error("LIF Files Error", lif_files)
                self.home_screen()
                return

            lif_files_contents = {}
            for lif_file in lif_files:
                self.loading_file_label.configure(text=f"Processing {lif_file}...")
                self.root.update_idletasks()
                lif_file_content = self.program_functions.read_n_categorize_file(lif_file)
                if isinstance(lif_file_content, str):
                    self.error("File Error", lif_file_content)
                    self.home_screen()
                    return
                lif_files_contents[lif_file] = lif_file_content

            scores = self.program_functions.get_all_scores(lif_files_contents)
            sorted_scores = self.program_functions.sort_descending(scores)

            if self.save_to_csv_var.get():
                csv_path = self.save_to_csv(sorted_scores, year, keyword)
                self.success("CSV Exported", f"Results saved to {csv_path}")

            self.success("Success", "Processing completed successfully!")

        except Exception as e:
            self.error("Processing Error", str(e))

        finally:
            self.home_screen()

    def remove_current_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def pick_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.program_functions.main_folder = folder_path
            self.parent_folder_button.configure(text=f"Selected: {os.path.basename(folder_path)}")

    def save_to_csv(self, sorted_scores, year, keyword):
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"WakaNats_{year}_{keyword}_{current_time}.csv"
        if not os.path.exists('exports'):
            os.makedirs('exports')
        filepath = os.path.join('exports', filename)
        with open(filepath, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Regional Association', 'Score'])
            for association, score in sorted_scores.items():
                csv_writer.writerow([association, score])
        return filepath

if __name__ == "__main__":
    app = GUIComponent()
    app.root.mainloop()