import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

SIG_DIGIT = 1 # number of digits after the decimal point

def MPO_clogp(clogp: float) -> float:
    if clogp <= 3.0:
        return 1
    if clogp >= 5.0:
        return 0
    return (5.0 - clogp)/2.0
 

def MPO_clogd(clogd:float) -> float:
    if clogd <= 2.0:
        return 1.0
    if clogd >= 4.0:
        return 0.0
    return (clogd - 2.0)/2.0  

def MPO_mw(mw: float) -> float:
    if mw <= 360.0:
        return 1.0
    if mw >= 500.0:
        return 0
    return (500- mw)/(500.0 - 360)

def MPO_pka(pka: float) -> float:
    if pka <= 8.0:
        return 1.0
    if pka >= 10.0:
        return 0.0
    return (10 - pka)/2.0  

def MPO_hbd(hbd:int ) -> float:
    if hbd == 0:
        return 1.0
    if hbd >= 3.5:
        return 0.0
    return (3.5 - hbd )/3.0


def MPO_tpsa(tpsa: float) -> float:
    if tpsa <= 20 or tpsa >= 120:
        return 0.0
    if tpsa > 20 and tpsa < 40:
        return (tpsa -20)/20.0
    if tpsa > 90 and tpsa < 120:
        return (tpsa -90)/30.0
    return 1.0
st.markdown("#### Central nervous system multiparameter optimization (CNS MPO) calculator")
st.sidebar.markdown("#### define physchem properties")
st.markdown('##### :green[CNS MPO contributions]')

pka = st.sidebar.number_input('pKa',min_value=0,max_value=14, value = 2, label_visibility="visible")
mw = st.sidebar.number_input('MolMass',min_value=0,max_value=1500, value = 300, step=10)
hbd = st.sidebar.number_input('hbd',min_value=0,max_value=20, value = 2)
clogp = st.sidebar.number_input('clogP',min_value=0,max_value=7, value = 2)
clogd = st.sidebar.number_input('clogD',min_value=0,max_value=7, value = 2)
tpsa = st.sidebar.number_input("TPSA", 0, 300, value=50, step=10)

pka = MPO_pka(pka)
mw = MPO_mw(mw) 
hbd = MPO_hbd(hbd) 
clogp = MPO_clogp(clogp)
clogd = MPO_clogd(clogd)
tpsa = MPO_tpsa(tpsa)

#setting up the dataframe
chart_data = pd.DataFrame(dict(
    group = ['pKa', 'MW', 'HBD', 'clogP', 'clogD', 'TPSA'],
    value = [pka, mw, hbd, clogp, clogd, tpsa]))
chart_data = chart_data.round(SIG_DIGIT)

fig = px.bar(chart_data, x= "group", y = "value", color="group", text_auto=True)
fig.update_traces(textfont_size=14, textangle=0, textposition = "outside")
fig.update_layout(yaxis_title="contribution")
fig.update_layout(xaxis_title="property")
fig.update_layout(showlegend=False)
st.plotly_chart(fig)
# the total of all MPO contributions
st.markdown("##### :green[the sum of contributions = ] " + str(chart_data.sum(axis=0).value))
st.markdown("""####
for more detail on CNS MPO see e.g. *ACS Chem. Neurosci.* **2016**, *7*, 767−775
""")