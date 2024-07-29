import csv

class CSVExport:
    @staticmethod
    def csv_export(data, filename):
        with open(f"{filename}.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Regional Association", "Score"])
            for region, score in data.items():
                writer.writerow([region, score])

csv_c = CSVExport()