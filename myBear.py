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


class Iloc:
    def __init__(self, series):
        self.series = series

    def __getitem__(self, index):
        if isinstance(index, slice):
            return Series(self.series.nom, self.series.data[index])
        else:
            return self.series.data[index]

