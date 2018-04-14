import csv

from retailstore.cli.commands.base import Base
from retailstore.cli.curry import (
    location_srv,
    department_srv,
    category_srv,
    sub_category_srv,
)


class StoreData:
    def __init__(self, row):
        self.data = row

    def run(self):
        tmp = sub_category_srv(
            category_srv(
                department_srv(
                    location_srv(
                        self.data))))
        return tmp


class CsvImport(Base):
    """Parses csv file and store in DB."""

    def run(self):
        csv_file_path = self.options['<csv_file_path>']

        try:
            with open(csv_file_path, newline='', encoding='latin-1') as f:
                data = [
                    StoreData(row).run()
                    for row in csv.DictReader(f)
                ]
        except FileNotFoundError:
            raise ValueError("Please provide a valid csv file path")

        return data
