import myBear as mb
import numpy as np
if __name__ == '__main__':
    # Series
    # Implémentation de la classe
    d = [35, 67, 3]
    s = mb.Series("Ma série", d)
    # Fonctions statistiques max, min, mean, std et count pour Series
    # print(s)

    # Propriété iloc
    # print(s.iloc[1])
    # print(s.iloc[0:2])

    # Dataframe
    # version où l'on peut charger une liste de Series en tant que DataFrame.
    slist = [mb.Series("Serie 1", [45, -5, 9]), mb.Series("Serie 2", [78, 9, 10])]
    df1 = mb.DataFrame(slist)
    # print(df1)

    # Une version où l'on peut directement charger les colonnes dans un paramètre, et les listes de valeurs dans un
    # second paramètre.
    df2 = mb.DataFrame([[45, -5, 40], [78, 9, 10, 900]], ["Serie 1", "Serie 2"])
    # print(df2)  # pk es que lorsque je fait df1.data ca maffiche une liste de tuple comme il faut mais ca
    # m'affiche plutot l'address des series correspondant

    # iloc[n, n]
    # print(df2.iloc[0, 1])

    # iloc[a:b, n]
    # print(df2.iloc[0:2, 1])

    # iloc[n, a:b]
    # print(df2.iloc[2, 0:2])

    # iloc[x:y, a:b]
    # print(df2.iloc[0:2, 0:2])

    # Fonctions statistiques max, min, mean, std et count pour DataFrame

    # max
    # print(df2.max())

    # min
    # print(df2.min())

    # mean
    # print(df2.mean())

    # std
    # print(df2.std())

    # count
    # print(df2.count())

    # test read_csv
    dataframe = mb.DataFrame.read_csv("test.csv")
    print(dataframe)

    # test read_json
    # records
    dataframe = mb.DataFrame.read_json('records.json')
    print(dataframe)

    # Columns
    dataframe = mb.DataFrame.read_json('columns.json', "columns")
    print(dataframe)

    data1 = [
        mb.Series("Animal", ["Dog", "Cat", "Dog", "Dog", "Cat", "Cat"]),
        mb.Series("Color", ["Black", "White", "Black", "White", "White", "Black"]),
        mb.Series("Weight", [25, 10, 30, 28, 11, 12]),
        mb.Series("Age", [5, 2, 6, 3, 4, 2])
    ]

    data2 = [
        mb.Series("Breed", ["Labrador", "Persian", "Bulldog", "Poodle", "Siamese", "Persian"]),
        mb.Series("Color", ["Black", "White", "Black", "White", "White", "Black"]),
        mb.Series("Popularity", [5, 3, 4, 2, 3, 5])
    ]

    df1 = mb.DataFrame(data1)
    df2 = mb.DataFrame(data2)

    # groupby example
    grouped_df = df1.groupby(by=["Animal", "Color"], agg={"Weight": max, "Age": np.mean})
    print(grouped_df)