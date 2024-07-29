import os

class FileRead:
    @staticmethod
    def return_years(parent_path):
        return [d for d in os.listdir(parent_path) if os.path.isdir(os.path.join(parent_path, d))]

    @staticmethod
    def find_year_path(parent_path, year, folder_name):
        return os.path.join(parent_path, f"{folder_name}{year}")

    @staticmethod
    def return_files(target_year_path):
        return [f for f in os.listdir(target_year_path) if os.path.isfile(os.path.join(target_year_path, f))]

    @staticmethod
    def return_content(filepath):
        with open(filepath, 'r') as file:
            return file.readlines()

    @staticmethod
    def format_content(file_contents, filename):
        header = file_contents.pop(0).strip().split(',')
        if len([item for item in header if item]) != 6:
            return f"{filename} has an error in race information: {header}."

        lif_teams = []
        for line in file_contents:
            if any(status in line for status in ["DQ", "DNS", "Disqualified"]):
                continue

            cleaned_line = [item for item in line.strip().split(',') if item]
            if len(cleaned_line) != 11:
                return f"{filename} has an error on team line: {line}."

            team_id = cleaned_line[0]
            team_place = cleaned_line[1]
            team_name = cleaned_line[4]
            team_regional_association = cleaned_line[5]

            if not team_place.isdigit() or team_name.isdigit() or team_regional_association.isdigit():
                return f"{filename} has an error on team line: {line}."

            lif_teams.append([team_id, team_place, team_name, team_regional_association])

        return lif_teams

file_read_c = FileRead()