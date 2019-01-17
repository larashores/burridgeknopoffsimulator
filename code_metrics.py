import sys
import os


class Stats:
    def __init__(self):
        self._file_types = {}
        self._lines_of_code = {}
        self._blank_lines = {}

    def add_file(self, path):
        extension = os.path.splitext(path)[-1]
        if extension not in self._file_types:
            self._file_types[extension] = 0
        self._file_types[extension] += 1
        if extension in ('.py', '.h', '.cpp'):
            try:
                with open(path, 'r') as file:
                    if extension not in self._lines_of_code:
                        self._lines_of_code[extension] = 0
                    lines = file.readlines()
                    self._lines_of_code[extension] += len(lines)
                    for line in lines:
                        if line == '\n':
                            if extension not in self._blank_lines:
                                self._blank_lines[extension] = 0
                            self._blank_lines[extension] += 1
            except Exception as err:
                pass

    def file_types(self):
        return self._file_types

    def lines_of_code(self):
        return self._lines_of_code

    def lines_of_code_per_file(self):
        lines_per_file = {}
        for extension in self._lines_of_code:
            lines_per_file[extension] = round(self._lines_of_code[extension] / self._file_types[extension], 2)
        return lines_per_file

    def percent_blank(self):
        blank_per_file = {}
        for extension in self._lines_of_code:
            blank_per_file[extension] = '{:.2%}'.format(self._blank_lines[extension] / self._lines_of_code[extension])
        return blank_per_file


def metrics(paths):
    stats = Stats()
    for root_path in paths:
        for root, directories, files in os.walk(root_path):
            if 'venv' in root:
                continue
            for file in files:
                stats.add_file(os.path.join(root, file))
    print(stats.file_types())
    print('Lines of code: ', stats.lines_of_code())
    print('Lines of code per file', stats.lines_of_code_per_file())
    print('Percent blank lines: ', stats.percent_blank())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: code_metrics directory')
    else:
        directories = sys.argv[1:]
        metrics(directories)