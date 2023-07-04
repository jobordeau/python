import myBear as mb

if __name__ == '__main__':
    # Series
    # Implémentation de la classe
    d = [35, 67, 3]
    s = mb.Series("Ma série", d)

    # Propriété iloc
    print(s.iloc[1])
    print(s.iloc[0:2])

    # Fonctions statistiques max, min, mean, std et count
    print(f"max: {s.max()}")
    print(f"min: {s.min()}")
    print(f"mean: {s.mean()}")
    print(f"std: {s.std()}")
    print(f"count: {s.count()}")

    # Dataframe
    # version où l'on peut charger une liste de Series en tant que DataFrame.
    slist = [mb.Series("Serie 1", [45, -5, 9]), mb.Series("Serie 2", [78, 9, 10])]
    df1 = mb.DataFrame(slist)
    print(df1.data)

    # Une version où l'on peut directement les colonnes dans un paramètre, et les listes de valeurs dans un second paramètre.
    df2 = mb.DataFrame([[45, -5, 9], [78, 9, 10]], ["Serie 1", "Serie 2"])
    print(df2.data)
