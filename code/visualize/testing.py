import plotly.graph_objects as go
import pandas as pd
import seaborn as sns

mdf = sns.load_dataset('mpg')

def filt_df(df:pd.DataFrame, cyl:int, ogn:str) -> pd.DataFrame:
    odf = df[df['origin'] == ogn]
    return odf[odf['cylinders'] == cyl].drop(['origin', 'name'], axis=1).groupby('model_year').mean().reset_index()

fig = go.Figure()
countries = {'usa':1, 'japan':2, 'europe':3}
cylinder_colors = {'4':'red', '6':'green', '8':'blue'}

for country in mdf['origin'].unique():
    tdf = filt_df(mdf, 4, country)
    fig.add_trace(go.Scatter(x=tdf['model_year'], y=tdf['mpg'],
                             name=f'4 cyls ({country})',
                             legendgroup=countries[country],
                             marker=dict(color=cylinder_colors['4'])))
    tdf = filt_df(mdf, 6, country)
    fig.add_trace(go.Scatter(x=tdf['model_year'], y=tdf['mpg'],
                             name=f'6 cyls ({country})',
                             legendgroup=countries[country],
                             marker=dict(color=cylinder_colors['6'])))
    tdf = filt_df(mdf, 8, country)
    fig.add_trace(go.Scatter(x=tdf['model_year'], y=tdf['mpg'],
                             name=f'8 cyls ({country})',
                             legendgroup=countries[country],
                             marker=dict(color=cylinder_colors['8'])))

fig.update_traces(mode='lines+markers', marker=dict(size=8), line=dict(width=0.5))
fig.update_layout(title='MPG by model year', xaxis_title='Model year', yaxis_title='MPG', legend_title='Cylinders',
                  xaxis=dict(
                      autorange=True,
                      range=[70, 82],
                      rangeslider=dict(
                            autorange=True,
                            range=[70, 82]
                        ),
                        type='linear'
                  ))

fig.write_html('mpg.html')