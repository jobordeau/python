import statistics


class Series:
    def __init__(self, nom, data):
        self.nom = nom
        self.data = data

    @property
    def iloc(self):
        return Iloc(self)

    def max(self):
        return max(self.data)

    def min(self):
        return min(self.data)

    def mean(self):
        return statistics.mean(self.data)

    def std(self):
        return statistics.stdev(self.data)

    def count(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)


class Iloc:
    def __init__(self, series):
        self.series = series

    def __getitem__(self, index):
        if isinstance(index, slice):
            return Series(self.series.nom, self.series.data[index])
        else:
            return self.series.data[index]


class DataFrame:
    def __init__(self, data=None, columns=None):
        if isinstance(data, list) and isinstance(data[0], Series):
            self.data = {series.nom: series.data for series in data}
        elif isinstance(data, list) and isinstance(columns, list):
            self.data = {columns[i]: col_data for i, col_data in enumerate(data)}
        else:
            self.data = {}
