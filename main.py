import myBear as mb

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
