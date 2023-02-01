class CSVFileReader:
    @staticmethod
    def read(file_name, header=True):
        with open(file_name, 'r', encoding='utf-8-sig') as file:
            if header:
                next(file)
            return file.readlines()

