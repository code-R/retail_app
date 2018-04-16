import csv

from retailstore.cli.commands.base import Base


class FindSkus(Base):
    """Parses csv file and store in DB."""

    def run(self):
        csv_file_path = self.options['<csv_file_path>']
        input_meta = self.options['<input_meta>']

        try:
            with open(csv_file_path, newline='', encoding='latin-1') as f:
                res = csv.DictReader(f)
        except FileNotFoundError:
            raise ValueError("Please provide a valid csv file path")

        return res, input_meta
