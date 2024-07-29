import os
import file_read as fr
import scoring
import csv_export

points_reference = {
    "1": 8, "2": 7, "3": 6, "4": 5, "5": 4, "6": 3, "7": 2, "8": 1, ">": 1,
}

def get_valid_input(prompt, validation_func=None):
    while True:
        user_input = input(prompt)
        if validation_func is None or validation_func(user_input):
            return user_input
        print("Invalid input. Please try again.")

def is_numeric(s):
    return s.isnumeric()

def process_files(target_year_path, filtered_files_list):
    files_regional_association_score_list = []
    for filename in filtered_files_list:
        try:
            filepath = os.path.join(target_year_path, filename)
            file_contents = fr.file_read_c.return_content(filepath)
            formatted_file_contents = fr.file_read_c.format_content(file_contents, filename)
            
            if isinstance(formatted_file_contents, str):  # Assuming error messages are returned as strings
                print(formatted_file_contents)
                continue

            file_regional_association_scores = scoring.scoring_c.return_scores(formatted_file_contents, points_reference)
            files_regional_association_score_list.append(file_regional_association_scores)
        except Exception as e:
            print(f"ERROR | {filename} | {e}")
    return files_regional_association_score_list

def main():
    # Get parent folder
    parent_path = get_valid_input("Type your folder name: ")
    if not os.path.exists(parent_path):
        print(f"Folder '{parent_path}' does not exist.")
        return
    years = fr.file_read_c.return_years(parent_path)
    if not years:
        print(f"No valid year folders found in '{parent_path}'.")
        return
    print("Available years:", years)

    # Get year and files
    ask_year = int(get_valid_input("Type your year: ", is_numeric))
    target_year_path = fr.file_read_c.find_year_path(parent_path, ask_year, "WakaNats")
    if not os.path.exists(target_year_path):
        print(f"Year folder for {ask_year} not found.")
        return
    files_list = fr.file_read_c.return_files(target_year_path)
    if not files_list:
        print(f"No files found in the year folder for {ask_year}.")
        return

    # Filter files
    ask_keyword = input("Filter keyword: ").lower()
    filtered_files_list = [file for file in files_list if ask_keyword in file.lower()]
    print(f"{len(filtered_files_list)} {ask_keyword} found")

    # Process files
    files_regional_association_score_list = process_files(target_year_path, filtered_files_list)

    # Calculate and sort scores
    year_regional_association_scores = scoring.scoring_c.return_year_sum_score(files_regional_association_score_list)
    year_regional_association_scores = scoring.scoring_c.sort_score(year_regional_association_scores)

    # Export to CSV if requested
    if input("Do you wish to save as CSV? (Y/N) >> ").upper() == "Y":
        csv_filename = input("Type filename >> ")
        csv_export.csv_c.csv_export(year_regional_association_scores, csv_filename)

if __name__ == "__main__":
    main()