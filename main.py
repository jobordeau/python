import myBear as mb

if __name__ == '__main__':
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
