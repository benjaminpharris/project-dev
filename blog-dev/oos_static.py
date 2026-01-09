import numpy as np
import pandas as pd
import plotly.graph_objects as go
import statsmodels.formula.api as smf

color_map = {
    'Low': "#748fa4",
    'Mid': 'goldenrod',
    'High': 'tomato'
}

x = np.random.uniform(-10, 40, 1000)
y = 10 / (1 + np.exp(-((x - 6) / 4)))
y += np.random.normal(0, .4, size=1000)
df = pd.DataFrame({'x': x, 'y': y})
df['tritile'] = pd.qcut(df['x'], 3, labels=['Low', 'Mid', 'High'])

# Fit OLS for each tritile
ols_fits = {}
for tritile in ['Low', 'Mid', 'High']:
    mask = df['tritile'] == tritile
    model = smf.ols("y ~ x", data=df[mask]).fit()
    ols_fits[tritile] = model

# Create figure and add all points
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['x'], y=df['y'], mode='markers',
    marker=dict(
        color=df['tritile'].map(color_map),
        size=8,
        line=dict(color='white', width=1)
    ),
    name='All Points'
))

# Add OLS trendlines for each tritile
x_curve = np.linspace(df['x'].min(), df['x'].max(), 500)
for tritile, model in ols_fits.items():
    y_line = model.predict(pd.DataFrame({'x': x_curve}))
    fig.add_trace(go.Scatter(
        x=x_curve, y=y_line, mode='lines',
        line=dict(color=color_map[tritile], width=3, dash='dash'),
        name=f'{tritile} OLS'
    ))

# Add true logistic curve
y_curve = 10 / (1 + np.exp(-((x_curve - 6) / 4)))
fig.add_trace(go.Scatter(
    x=x_curve, y=y_curve, mode='lines',
    name='True Relationship',
    line=dict(color='white', width=3)
))

fig.update_layout(
    xaxis=dict(showgrid=False, color="#A3A3A3", ticks='outside', tickcolor="#A3A3A3"),
    yaxis=dict(showgrid=False, color="#A3A3A3", ticks='outside', tickcolor="#A3A3A3"),
    plot_bgcolor="#282726",
    paper_bgcolor="#282726",
    font=dict(color='white')
)

fig.show()
fig.write_html("out_of_sample_viz_static.html", include_plotlyjs='cdn', full_html=False)