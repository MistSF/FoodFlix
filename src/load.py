import pandas as pd
import src.clean as cl

def removeNonValuableData(path, newFile, toKeep, tsv=False) :
    """
        Create new file with only the columns in toKeep
    """
    if tsv :
        df = pd.read_csv(path, sep="\t")
    else :
        df = pd.read_csv(path)
    df = df[toKeep]
    df = cl.removeEmpty(df)
    listEmptyNutritionGradeFr = df.loc[df.nutrition_grade_fr.isnull()]
    for x in listEmptyNutritionGradeFr.code :
        df = cl.getNutriScore(df, x)
    df.to_csv(newFile)
    return df