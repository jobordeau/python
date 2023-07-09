import statistics


class Series:
    def __init__(self, nom: str, data: list):
        self.nom = nom
        self.data = data

    @property
    def iloc(self):
        return IlocSeries(self)

    def max(self):
        return max(self.data)

    def min(self):
        return min(self.data)

    def mean(self):
        return statistics.mean(self.data)

    def std(self):
        if len(self.data) <= 1:
            return 0

        return statistics.stdev(self.data)

    def count(self):
        return len(self.data)

    def __str__(self):
        toString = f"Etiquette: {self.nom} \n Donnée: {str(self.data)} \n Statistiques: \n ------------------- \n " \
                   f"max: {self.max()} \n min: {self.min()} \n mean: {self.mean()} \n std: {self.std()} \n " \
                   f"count: {self.count()} \n"
        return toString


class IlocSeries:
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
            self.data = [(series.nom, series) for series in data]
        elif isinstance(data, list) and isinstance(columns, list):
            self.data = [(columns[i], Series(columns[i], col_data)) for i, col_data in enumerate(data)]
        else:
            self.data = {}

    @property
    def iloc(self):
        return IlocDataFrame(self)

    def max(self):
        return DataFrame([Series(serie[0], [serie[1].max()]) for serie in self.data])

    def min(self):
        return DataFrame([Series(serie[0], [serie[1].min()]) for serie in self.data])

    def mean(self):
        return DataFrame([Series(serie[0], [serie[1].mean()]) for serie in self.data])

    def std(self):
        return DataFrame([Series(serie[0], [serie[1].std()]) for serie in self.data])

    def count(self):
        return DataFrame([Series(serie[0], [serie[1].count()]) for serie in self.data])

    def __str__(self):
        toString = ""
        for serie in self.data:
            toString += f"{str(serie[1])} \n####################\n"
        return toString


class IlocDataFrame:
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame

    def __getitem__(self, index):
        if isinstance(index[0], int) and isinstance(index[1], int):
            return self.dataFrame.data[index[1]][1].data[index[0]]
        elif isinstance(index[0], slice) and isinstance(index[1], int):
            return Series(self.dataFrame.data[index[1]][0], self.dataFrame.data[index[1]][1].data[index[0]])
        elif isinstance(index[0], int) and isinstance(index[1], slice):
            return DataFrame([Series(serie[0], [serie[1].data[index[0]]]) for serie in self.dataFrame.data[index[1]]])
        else:
            return DataFrame([Series(serie[0], serie[1].data[index[0]]) for serie in self.dataFrame.data[index[1]]])
