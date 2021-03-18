import streamlit as st
#import sim_pseudo_code as spc
#import Team_Class as tc
import pandas as pd 
import plotly.graph_objects as go
import numpy as np

#add in seed

@st.cache
def load_data():
    win_probs = pd.read_csv('dash_data4.csv')
    return win_probs

df = load_data()
data = df.reindex(columns=['sim_prob','rf_model','nn_model','elo_pred','seed_pred','Pred'])
df_t_seed = df.reindex(columns=['Team_Name_1','Team_Name_2','Seed1','Seed2'])
df_t_seed['Team_Name_1'] = df_t_seed.apply(lambda x: str(x.Team_Name_1) + ' ('+str(x.Seed1)+')', axis=1)
df_t_seed['Team_Name_2'] = df_t_seed.apply(lambda x: str(x.Team_Name_2) + ' ('+str(x.Seed2)+')', axis=1)
teams = df_t_seed.reindex(columns= ['Team_Name_1','Team_Name_2'])

data_inverse = 1- data.copy() 
data['Team1'] = teams.Team_Name_1
data['Team2'] = teams.Team_Name_2
data_inverse['Team1'] = teams.Team_Name_2
data_inverse['Team2'] = teams.Team_Name_1

df_fin = pd.concat([data,data_inverse])

st.title('Win Probability By Model 2021')
t1 = st.selectbox('Team 1:', df_fin.Team1.unique())
t2 = st.selectbox('Team 2:', df_fin.Team2.unique())

d_out = df_fin[(df_fin['Team1']== t1) & (df_fin['Team2'] == t2)].round(2)
values = [d_out.iloc[0]['Pred'],d_out.iloc[0]['elo_pred'], d_out.iloc[0]['seed_pred'], d_out.iloc[0]['sim_prob'], d_out.iloc[0]['rf_model'], d_out.iloc[0]['nn_model']]
values2 = [1-d_out.iloc[0]['Pred'],1-d_out.iloc[0]['elo_pred'],1- d_out.iloc[0]['seed_pred'],1- d_out.iloc[0]['sim_prob'], 1-d_out.iloc[0]['rf_model'], 1-d_out.iloc[0]['nn_model']]

#st.dataframe(d_out)

def create_fig(d_out,values):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=['AGGREGATE', 'elo', 'seed','sim','rf_model','nn_model'],
        #x=[d_out['aggregate'][0],d_out['elo_pred'][0], d_out['seed_pred'][0], d_out['sim_prob'][0], d_out['rf_model'][0], d_out['nn_model'][0]],
        x =values,
        name=d_out.iloc[0]['Team1'],
        orientation='h',
        text=values,
        textposition='auto',
        marker=dict(
            color='rgba(246, 78, 139, 0.6)',
            line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        )
    ))

    fig.add_trace(go.Bar(
        y=['AGGREGATE', 'elo', 'seed','sim','rf_model','nn_model'],
        x=values2,
        name=d_out.iloc[0]['Team2'],
        orientation='h',
        marker=dict(
            color='rgba(58, 71, 80, 0.6)',
            line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
        )
    ))
    fig.update_layout(barmode='stack')
    return fig
f_out = create_fig(d_out,values)
st.plotly_chart(f_out)
#st.dataframe(d_out)