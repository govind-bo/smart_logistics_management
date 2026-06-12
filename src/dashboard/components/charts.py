import plotly.express as px
from plotly.graph_objects import Figure
import pandas as pd

l_margin, r_margin, t_margin, b_margin = 20, 20, 50, 20

# BAR CHART --------------------------------------------------------
def create_bar_chart(df: pd.DataFrame, x: str, y: str, 
                     title: str | None = "",
                     xaxis_title: str | None = None,
                     yaxis_title: str | None = None,
                     height: int = 350,
                     text: str | None = None,
                     orientation: str = 'v') -> Figure:
    '''
    Create a bar chart and return it.
    '''
    if df.empty:
        fig = px.bar(title=title, height=height)
        fig.add_annotation(text="No data available", showarrow=False)
        return fig
    
    fig = px.bar(df, x=x, y=y, text=text, orientation=orientation)
    fig.update_layout(title=title, height=height, margin=dict(l=l_margin, r=r_margin, t=t_margin, b=b_margin))
    return fig

# LINE CHART -------------------------------------------------------
def create_line_chart(df: pd.DataFrame, x: str, y: str,
                      title: str | None = None,
                      xaxis_title: str | None = None,
                      yaxis_title: str | None = None,
                      height: int = 350,
                      text: str | None = None) -> Figure:
    '''
    Create a line chart with markers and return it.
    '''
    if df.empty:
        fig = px.line(title=title, height=height)
        fig.add_annotation(text="No data available", showarrow=False)
        return fig
    
    
    fig = px.line(df, x=x, y=y, markers=True, text=text)
    fig.update_layout(title=title, height=height, margin=dict(l=l_margin, r=r_margin, t=t_margin, b=b_margin))
    return fig