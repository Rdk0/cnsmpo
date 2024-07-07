import streamlit as st
import numpy as np
import pandas as pd


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
        return 0.5
    return (3.5 - hbd )/3.0


def MPO_tpsa(tpsa: float) -> float:
    if tpsa <= 20 or tpsa >= 120:
        return 0.0
    if tpsa > 20 and tpsa < 40:
        return (tpsa -20)/20.0
    if tpsa > 90 and tpsa < 120:
        return (tpsa -90)/30.0
    return 1.0 

#add_selectbox = st.sidebar.selectbox(
pka = st.sidebar.number_input('pKa',min_value=0,max_value=14, value = 2),  # 👈 this is a widget
mw = st.sidebar.number_input('MolMass',min_value=0,max_value=1500, value = 300, step=10) 
hbd = st.sidebar.number_input('hbd',min_value=0,max_value=20, value = 2)
clogp = st.sidebar.number_input('clogP',min_value=0,max_value=7, value = 2)
clogd = st.sidebar.number_input('clogD',min_value=0,max_value=7, value = 2)
tpsa = st.sidebar.number_input("TPSA", 0, 300, value=50, step=10) #st.sidebar.slider('TPSA',min_value=0,max_value=300, value = 50)
#) # 👈 this is a widget

#st.write('CNS MPO contribution for pKa is', MPO_pka(pka[0]))
#st.write('CNS MPO contribution for MolMass is', MPO_mw(mw))
#st.write('CNS MPO contribution for hbd', MPO_hbd(hbd))
#st.write('CNS MPO contribution for clogP', MPO_clogp(clogp))
#st.write('CNS MPO contribution for clogD', MPO_clogd(clogd))
#st.write('CNS MPO contribution for TPSA', MPO_tpsa(tpsa))

pka = MPO_pka(pka[0]) 
mw = MPO_mw(mw) 
hbd = MPO_hbd(hbd) 
clogp = MPO_clogp(clogp)
clogd = MPO_clogd(clogd)
tpsa = MPO_tpsa(tpsa)
data = {'pKa' : [pka], 'MW': [mw], 'HBD': [hbd], 'clogP': [clogp], 'clogD': [clogd], 'TPSA': [tpsa]}
chart_data = pd.DataFrame(data)
#st.bar_chart(source, x="variety", y="yield", color="site", horizontal=True)
pd.options.plotting.backend = "plotly"
fig = chart_data.transpose().plot.bar()
fig.update_layout(yaxis_title=None)
fig.update_layout(xaxis_title=None) 
fig.update_layout(showlegend=False)

st.plotly_chart(fig)#, horizontal=False)

st.text("CNS MPO =" + str(chart_data.sum(axis=1)[0]))