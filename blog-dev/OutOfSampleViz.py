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

# Prepare frames for animation
frames = []
for tritile in ['Low', 'Mid', 'High']:
    mask = df['tritile'] == tritile
    x_tritile = df.loc[mask, 'x']
    y_tritile = df.loc[mask, 'y']
    x_line = np.linspace(x_tritile.min(), x_tritile.max(), 200)
    y_line = ols_fits[tritile].predict(pd.DataFrame({'x': x_line}))
    # Axis range for zoom
    x_margin = (x_tritile.max() - x_tritile.min()) * 0.1
    y_margin = (y_tritile.max() - y_tritile.min()) * 0.1
    frames.append(go.Frame(
        name=tritile,
        data=[
            go.Scatter(
                x=x_tritile, y=y_tritile, mode='markers',
                marker=dict(color=color_map[tritile], size=8, line=dict(color='white', width=1)),
                name=f'{tritile} Points'
            ),
            go.Scatter(
                x=x_line, y=y_line, mode='lines',
                line=dict(color=color_map[tritile], width=3, dash='dash'),
                name=f'{tritile} OLS'
            )
        ],
        layout=go.Layout(
            xaxis=dict(range=[x_tritile.min()-x_margin, x_tritile.max()+x_margin]),
            yaxis=dict(range=[y_tritile.min()-y_margin, y_tritile.max()+y_margin])
        )
    ))

# Final frame: all points, all fits, and true logistic
final_data = []

# Combine all points from all tritiles
final_data.append(go.Scatter(
    x=df['x'], y=df['y'], mode='markers',
    marker=dict(
        color=df['tritile'].map(color_map),
        size=8,
        line=dict(color='white', width=1)
    ),
    name='All Points',
    showlegend=True
))

# Add true logistic curve
x_curve = np.linspace(df['x'].min(), df['x'].max(), 500)
y_curve = 10 / (1 + np.exp(-((x_curve - 6) / 4)))
final_data.append(go.Scatter(
    x=x_curve, y=y_curve, mode='lines',
    name='True Relationship',
    line=dict(color='white', width=3),
    showlegend=True
))

x_full = np.linspace(df['x'].min(), df['x'].max(), 200)

# now append each OLS trendline
for tritile, model in ols_fits.items():
    y_pred = model.predict(pd.DataFrame({'x': x_full}))
    final_data.append(go.Scatter(
        x=x_full,
        y=y_pred,
        mode='lines',
        line=dict(color=color_map[tritile], width=3, dash='dash'),
        name=f'{tritile} OLS',
        showlegend=True,
        legendgroup=tritile
    ))

# finally, push your “All” frame with everything in it
frames.append(go.Frame(
    name='All',
    data=final_data,
    layout=go.Layout(
        xaxis=dict(range=[df['x'].min(), df['x'].max()]),
        yaxis=dict(range=[df['y'].min(), df['y'].max()])
    )
))


# Initial figure (first tritile)
fig = go.Figure(
    data=frames[0].data,
    layout=go.Layout(
        xaxis=dict(showgrid=False, color="#A3A3A3", ticks='outside', tickcolor="#A3A3A3"),
        yaxis=dict(showgrid=False, color="#A3A3A3", ticks='outside', tickcolor="#A3A3A3"),
        plot_bgcolor="#282726",
        paper_bgcolor="#282726",
        font=dict(color='white'),
        updatemenus=[{
            "type": "buttons",
            "showactive": True,
            "buttons": [
                {"label": tritile, "method": "animate", "args": [[tritile], {"frame": {"duration": 500, "redraw": True}, "mode": "immediate"}]} for tritile in ['Low', 'Mid', 'High']
            ] + [
                {"label": "All + Logistic", "method": "animate", "args": [["All"], {"frame": {"duration": 500, "redraw": True}, "mode": "immediate"}]}
            ],
            "direction": "right",
            "x": 0.5,
            "y": 1.15
        }]
    ),
    frames=frames
)

fig.show()
fig.write_html("out_of_sample_viz.html", include_plotlyjs='cdn', full_html=False)
