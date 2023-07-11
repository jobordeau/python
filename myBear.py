import statistics
import csv
import json


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
        if len(self.data) <= 0 or isinstance(self.data[0], str):
            return 0
        return statistics.mean(self.data)

    def std(self):
        if len(self.data) <= 1 or isinstance(self.data[0], str):
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
    def __init__(self, series: Series):
        self.series = series

    def __getitem__(self, index):
        if isinstance(index, slice):
            return Series(self.series.nom, self.series.data[
                index])  # pk on cree une serie lorsque c'est un slice, parce que c'est dit dans l'enoncé
        else:
            return self.series.data[index]


class DataFrame:
    def __init__(self, data=None, columns=None):  # en fonction des données entrées on crées une liste de tuple,
        # pk avoir choisit d'utiliser une liste de tuple?
        if isinstance(data, list) and isinstance(data[0], Series):
            self.data = [(series.nom, series) for series in data]  # ici quand je fait series.data pk sa m'affiche
            # uniquement l'addresse de la serie? pk ne pas mettre series.data au lieu de series?
        elif isinstance(data, list) and isinstance(columns, list):
            self.data = [(columns[i], Series(columns[i], col_data)) for i, col_data in
                         enumerate(data)]  # pk on boucle sur data et pas sur columns?
        else:
            self.data = []

    @property
    def iloc(self):
        return IlocDataFrame(self)

    def max(self):
        return DataFrame([Series(serie[0], [serie[1].max()]) for serie in self.data])  # JE SUIS ICI

    def min(self):
        return DataFrame([Series(serie[0], [serie[1].min()]) for serie in self.data])

    def mean(self):
        return DataFrame([Series(serie[0], [serie[1].mean()]) for serie in self.data])

    def std(self):
        return DataFrame([Series(serie[0], [serie[1].std()]) for serie in self.data])

    def count(self):
        return DataFrame([Series(serie[0], [serie[1].count()]) for serie in self.data])

    @staticmethod
    def read_csv(path: str, delimiter: str = ","):
        with open("test.csv", "r") as csvFile:
            reader = csv.reader(csvFile, delimiter=delimiter)
            columns = zip(*reader)
            series = []
            for column in columns:
                series.append(Series(column[0], list(column)[1:]))
            return DataFrame(series)

    @staticmethod
    def read_json(path: str, orient: str = "records"):
        with open(path, "r") as json_file:
            data = json.load(json_file)

            if orient == "records":
                series = []
                for series_data in data:
                    for key, value in series_data.items():
                        series.append(Series(key, value))
                return DataFrame(series)
            elif orient == "columns":
                series = []
                for key, value in data.items():
                    series.append(Series(key, value))
                return DataFrame(series)
            else:
                return None

    def __str__(self):
        toString = ""
        for serie in self.data:  # data est une list de tuple, dans le tuple il n'ya que deux eleement genre le nom
            # de la serie à l'index 0 et la serie elle meme à l'index 1
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
