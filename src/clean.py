import pandas as pd
import missingno as msno

  def getPts(value, level) :
    valret = -1
    for i, x in enumerate(level) :
        if int(value) <= int(x) :
            valret = i
            break
    valret = 10 if valret == -1
    return valret

def getNutriScore(df, code) :
    currentRow = df.loc[df.code == code]
    ptsKJ = getPts(currentRow.energy_100g, [335, 670, 1005, 1340, 1675, 2010, 2345, 2680, 3015, 3350])
    ptsGlus = getPts(currentRow.sugars_100g, [4.5, 9, 13.5, 18, 22.5, 27, 31, 36, 40, 45])
    ptsAgs = getPts(currentRow["saturated-fat_100g"], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    ptsNA = getPts(currentRow.sodium_100g, [90, 180, 270, 360, 450, 540, 630, 720, 810, 900])
    ptsProt = getPts(currentRow.proteins_100g, [1.6, 3.2, 4.8, 6.4, 8])
    ptsFib = getPts(currentRow.fiber_100g, [0.9, 1.9, 2.8, 3.7, 4.7])
    ptsFLN = getPts(currentRow["fruits-vegetables-nuts_100g"], [40, 60, 80, 80, 80])

    ptsA = ptsKJ + ptsGlus + ptsAgs + ptsNA
    score = ptsA - (ptsProt + ptsFib + ptsFLN)

    currentRow["nutrition-score-fr_100g"] = score

    if score <= -1 :
        currentRow.nutrition_grade_fr = 'a'
    elif score <= 2 :
        currentRow.nutrition_grade_fr = 'b'
    elif score <= 10 :
        currentRow.nutrition_grade_fr = 'c'
    elif score <= 18 :
        currentRow.nutrition_grade_fr = 'd'
    else :
        currentRow.nutrition_grade_fr = 'e'
    df.loc[df.code == code] = currentRow
    return df

def removeEmpty(df) :
    df = df.dropna(subset=[
        "product_name", 
        "countries", 
        "energy_100g", 
        "salt_100g", 
        "sodium_100g"])
    df = df.fillna(value={
        'fruits-vegetables-nuts_100g':0, 
        'fat_100g': 0, 
        'saturated-fat_100g': 0, 
        'sugars_100g' : 0, 
        'fiber_100g' : 0, 
        'proteins_100g' : 0})
    
    df = df.loc[df.fat_100g <= 100]
    df = df.loc[df['fruits-vegetables-nuts_100g'] <= 100]
    df = df.loc[df["saturated-fat_100g"] <= 100]
    df = df.loc[df.sugars_100g <= 100]
    df = df.loc[df.fiber_100g <= 100]
    df = df.loc[df.proteins_100g <= 100]

    df = df.drop(df.countries.loc[~df.countries.str.contains("France")].index)
    return df
