import os

import polars as pl

import githubver as gh

"""
conda env = base
The program consists of two parts 
1. CALCULATE PFIZER's SCORES
2. CALCULATE MERCK's SCORES BASED ON thisgithub code for the functionality described in: Gunaydin, Hakan. Probabilistic Approach to Generating MPOs and Its Application as a Scoring Function for CNS Drugs.
ACS Med Chem Lett 7, 89-93 (2016) https://github.com/Merck/pmpo
the program returns Pfizer's CNS MPO and Merck probabilistic MPO based on an xlsx from ACD Percepta
outpot .xlx\sx file
########################################################################################################################
to get this to work cohesievely, githuver.py file was modifed by adding this function
def score_pmpo(molecule: dict[str, float]) -> float:
    score = model(**molecule)
    return score
"""


def MPO_tpsa(tpsa: float) -> float:
    """
    calculate partial  Pfizer's  score based on TPSA
    :param tpsa: 
    :return: partial score:  float
    """
    if tpsa <= 20 or tpsa >= 120:
        return 0
    if tpsa > 20 and tpsa < 40:
        return (tpsa - 20) / 20.0
    if tpsa > 90 and tpsa < 120:
        return (tpsa - 90) / 30.0
    return 1.0


def MPO_hbd(hbd: float) -> float:
    """
       calculate partial  Pfizer's score based on HBD
       :param tpsa: 
       :return: partial score:  float
       """
    if hbd >= 3.5:
        return 0.5
    return (3.5 - hbd) / 3.0


def MPO_pka(pka: float) -> float:
    """
       calculate partial  Pfizer's score based on pKa
       :param tpsa: 
       :return: partial score:  float
       """
    if pka <= 8.0:
        return 1
    if pka >= 10.0:
        return 0
    return (10 - pka) / 2.0


def MPO_mw(mw: float) -> float:
    """
       calculate partial  Pfizer's score based on MW
       :param tpsa: 
       :return: partial score:  float
       """
    if mw <= 360.0:
        return 1.0
    if mw >= 500.0:
        return 0
    return (500 - mw) / (500.0 - 360)


def MPO_clogd(clogd: float) -> float:
    """
       calculate partial  Pfizer's score based on clogD
       :param tpsa: 
       :return: partial score:  float
       """
    if clogd <= 2.0:
        return 1.0
    if clogd >= 4.0:
        return 0.0
    return (clogd - 2.0) / 2.0


def MPO_clogp(clogp: float) -> float:
    """
       calculate partial  Pfizer's score based on ACD clogP Classic
       :param tpsa: 
       :return: partial score:  float
       """
    if clogp <= 3.0:
        return 1
    if clogp >= 5.0:
        return 0
    return (5.0 - clogp) / 2.0


def get_pmpo_scores(dfpl):
    """
    calculate Merck pMPO scores using gh  
    :param  polars dfl: 
    :return: polars df
    """
    # need to werk from this dir to get merck code to run
    os.chdir(r"Y:\private\RadekLaufer_Y\coding\all_python\CNS_MPO\CNS_MPO\Merck_pMPO\pmpo-master")
    pmpo_scores: list[float] = []
    for row in dfpl.iter_rows(named=True):
        # for indx in row:
        mol = {
            'TPSA': row['TPSA'],
            'HBA': row['No. of Hydrogen Bond Acceptors'],
            'HBD': row['No. of Hydrogen Bond Donors'],
            'MW': row['Molecular Weight'],
            'cLogD_ACD_v15': row['LogD (pH = 7.40)'],  # ACD logD based on both pKa and logP classic
            'mbpKa': row['1st strongest base pKa'],  # ACD pKa classic
            'cLogP_ACD_v15': row['LogP (1)']  # ACD logP Classic
        }
        score = gh.score_pmpo(mol)
        pmpo_scores.append(score)

    return dfpl.with_columns(pl.Series('Merck_pmpo', pmpo_scores))


def main():
    # read ACD labs file with calculated properites
    csv_file = r"Y:\public\Students_Contracts_Volunteers\Smriti Srivastava\Eurofins\CNS_MPO\Compounds Submitted (Eurofins)_pkr_selection_acd_fixed.csv"  # r"C:\Users\rlaufer\Documents\yumanity\yumanity_acd3.csv"
    df3pl = pl.read_csv(csv_file)
    # df3pl.columns
    """'LogP|RI', 'LogD (pH = 7.40)', '1st strongest base pKa', 'LogS (pH = 1.80)', 'LogS (pH = 4.00)', 'LogS (pH = 7.40)', 'TPSA', 'Molecular Weight', 'No. of Hydrogen Bond Donors',
     'No. of Hydrogen Bond Acceptors', 'LogP (1)',"""

    # CALCULATE PFIZER's SCORE
    for col, col_new, fun in zip(
            ["LogP (1)", 'LogD (pH = 7.40)', 'Molecular Weight', 'No. of Hydrogen Bond Donors', 'TPSA',
             '1st strongest base pKa'],
            ["mpo_clogp", "mpo_clogd", "mpo_mw", "mpo_hbd", "mpo_tpsa", "mpo_pka"],
            ["MPO_clogp", "MPO_clogd", "MPO_mw", "MPO_hbd", "MPO_tpsa", "MPO_pka"]):
        df3pl = df3pl.with_columns(pl.col(col).map_elements(globals()[fun], return_dtype=pl.Float64).alias(col_new))
    df3pl = df3pl.with_columns(
        (pl.col('mpo_clogp') + pl.col('mpo_clogd') + pl.col('mpo_mw') + pl.col('mpo_hbd') + pl.col(
            'mpo_tpsa') + pl.col('mpo_pka')).alias('CNS MPO'))
    df3pl = df3pl.with_columns(pl.col("CNS MPO").round(1))
    # CALCULATE MERCK SCORES
    new_df = get_pmpo_scores(df3pl)
    new_df.write_excel(csv_file[:-4] + '_calc_mpo.xlsx')


main()
