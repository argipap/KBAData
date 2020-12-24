import csv


class CsvWriter:
    def __init__(self, filename, delimeter=";",
                 new_line="",
                 quote_char='|',
                 quoting=csv.QUOTE_MINIMAL):
        self.filename = filename
        self.delimeter = delimeter
        self.new_line = new_line
        self.quote_char = quote_char
        self.quoting = quoting

    def write(self, data):
        with open(self.filename, "w", newline=self.new_line) as csv_file:
            writer = csv.writer(
                csv_file, delimiter=self.delimeter,
                quotechar=self.quote_char,
                quoting=self.quoting)
            for row in data:
                writer.writerow(row)
