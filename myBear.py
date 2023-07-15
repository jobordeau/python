import statistics
import csv
import json
from typing import List, Dict, Callable, Any, Union
from collections import defaultdict


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

    def describe(self):
        stats = {
            "max": self.max(),
            "min": self.min(),
            "mean": self.mean(),
            "std": self.std(),
            "count": self.count()
        }
        return stats

    def __str__(self):
        toString = f"Etiquette: {self.nom}\nDonnée: {str(self.data)}\n"

        if isinstance(self.data[0], (int, float)):
            # Handle numerical data
            if self.describe():
                stats = self.describe()
                toString += "Statistiques:\n"
                for stat, value in stats.items():
                    toString += f"- {stat}: {value}\n"
        else:
            # Handle non-numerical data
            unique_values = set(self.data)
            num_unique = len(unique_values)
            toString += f"Valeurs uniques: {', '.join(str(val) for val in unique_values)}\n"
            toString += f"Nombre de valeurs uniques: {num_unique}\n"

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

    @classmethod
    def from_records(cls, records: List[Dict[str, Any]]) -> 'DataFrame':
        columns = {key: [] for key in records[0].keys()}  # Initialize empty lists for each column

        for record in records:
            for key, value in record.items():
                columns[key].append(value)  # Append the value to the appropriate column

        # Convert the columns dictionary to a list of Series
        data = [Series(key, values) for key, values in columns.items()]

        return cls(data)  # Return a new DataFrame instance

    def groupby(self, by: Union[List[str], str], agg: Dict[str, Callable[[List[Any]], Any]]) -> 'DataFrame':
        if isinstance(by, str):
            by = [by]
        agg_keys = list(agg.keys())

        # Initialize a single defaultdict for the groups
        groups = defaultdict(lambda: defaultdict(list))

        data_dict = {key: serie.data for key, serie in self.data}  # Convert self.data to dictionary

        for i in range(len(data_dict[by[0]])):
            # Create a tuple for each row by combining all 'by' column values
            by_vals = tuple(data_dict[by_key][i] for by_key in by)

            # Append all non 'by' column values to the corresponding group
            for key, serie in data_dict.items():
                if key not in by:
                    groups[by_vals][key].append(serie[i])

        aggregated_data = []

        # Perform the aggregation operations
        for by_vals, agg_dict in groups.items():
            for agg_key, agg_func in agg.items():
                if agg_key in agg_dict:  # Only perform aggregation if the key is in the dict
                    agg_dict[agg_key] = agg_func(agg_dict[agg_key])
            # Add the 'by' values to the aggregated data
            agg_dict.update({by[i]: by_val for i, by_val in enumerate(by_vals)})
            aggregated_data.append(agg_dict)

        return DataFrame.from_records(aggregated_data)


    def join(
            self,
            other: 'DataFrame',
            left_on: Union[List[str], str],
            right_on: Union[List[str], str],
            how: str = "left"
    ) -> 'DataFrame':
        if isinstance(left_on, str):
            left_on = [left_on]

        if isinstance(right_on, str):
            right_on = [right_on]

        left_data_dict = {key: serie.data for key, serie in self.data}  # Convert self.data to dictionary
        right_data_dict = {key: serie.data for key, serie in other.data}  # Convert other.data to dictionary

        left_rows = [
            {key: left_data_dict[key][i] for key in left_data_dict.keys()}
            for i in range(len(left_data_dict[left_on[0]]))
        ]

        right_rows = [
            {key: right_data_dict[key][i] for key in right_data_dict.keys()}
            for i in range(len(right_data_dict[right_on[0]]))
        ]

        # Perform join operation
        joined_rows = []
        for left_row in left_rows:
            left_keys = tuple(left_row[key] for key in left_on)
            for right_row in right_rows:
                right_keys = tuple(right_row[key] for key in right_on)
                if left_keys == right_keys:
                    joined_row = {**left_row, **right_row}  # Merge two dictionaries
                    joined_rows.append(joined_row)
                    if how == 'left' or how == 'inner':
                        break  # In case of left or inner join, stop after finding the first match
            else:
                if how == 'left' or how == 'outer':
                    joined_rows.append(
                        left_row)  # In case of left or outer join, add the left row even if no match was found

        if how == 'right' or how == 'outer':
            # In case of right or outer join, add all right rows that do not match any left row
            for right_row in right_rows:
                right_keys = tuple(right_row[key] for key in right_on)
                for joined_row in joined_rows:
                    joined_keys = tuple(joined_row[key] for key in left_on)
                    if right_keys == joined_keys:
                        break
                else:
                    joined_rows.append(right_row)

        # Convert joined rows back to DataFrame
        return DataFrame.from_records(joined_rows)
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
        for serie in self.data:
            toString += f"Column: {serie[0]}\nData: {str(serie[1].data)}\n"

            if isinstance(serie[1].data[0], (int, float)):
                # Handle numerical data
                if serie[1].describe():
                    stats = serie[1].describe()
                    toString += "Statistics:\n"
                    for stat, value in stats.items():
                        toString += f"- {stat}: {value}\n"
            else:
                # Handle non-numerical data
                unique_values = set(serie[1].data)
                num_unique = len(unique_values)
                toString += f"Unique values: {', '.join(str(val) for val in unique_values)}\n"
                toString += f"Number of unique values: {num_unique}\n"

            toString += "\n"

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
