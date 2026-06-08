import plotly.express as px
from plotly.graph_objects import Figure
import pandas as pd

l_margin, r_margin, t_margin, b_margin = 20, 20, 50, 20
# BAR CHART --------------------------------------------------------
def create_bar_chart(df: pd.DataFrame,
                       x: str, y: str, 
                       title: str | None = "",
                       xaxis_title: str | None = None,
                       yaxis_title: str | None = None,
                       height: int = 350,
                       text: str | None = None) -> Figure:
    '''
    Creates a bar chart and returns it
    '''
    
    fig = px.bar(df, x = x, y = y, text = text)
    fig.update_layout(title = title,
                      height = height,
                      xaxis_title = xaxis_title,
                      yaxis_title = yaxis_title,
                      margin = dict(l=l_margin, r=r_margin, t=t_margin, b=b_margin))
    return fig

# LINE CHART -------------------------------------------------------
def create_line_chart(df: pd.DataFrame,
                      x: str, y: str,
                      title: str | None = None,
                      xaxis_title: str | None = None,
                      yaxis_title: str | None = None,
                      height: int = 350,
                      text: str | None = None) -> Figure:
    '''
    Creates a line chart and returns it
    '''
    
    fig = px.line(df, x = x, y = y, marker = True, text = text)
    fig.update_layout(title = title,
                      height = height,
                      xaxis_title = xaxis_title,
                      yaxis_title = yaxis_title,
                      margin = dict(l=l_margin, r=r_margin, t=t_margin, b=b_margin))
    return fig