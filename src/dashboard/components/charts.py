import plotly.express as px
from plotly.graph_objects import Figure
import pandas as pd
import streamlit as st

l_margin, r_margin, t_margin, b_margin = 20, 20, 50, 20

# region BAR CHART --------------------------------------------------------
def create_bar_chart(df: pd.DataFrame, x: str, y: str, 
                     title: str | None = "",
                     xaxis_title: str | None = None,
                     yaxis_title: str | None = None,
                     height: int = 350,
                     text: str | None = None,
                     orientation: str = 'v',
                     color: str|None = None,
                     barmode:str = 'relative',
                     hover_data: list | dict | None = None,
                     labels: dict | None = None,
                     texttemplate: str|None = None) -> Figure:
    '''
    Create a bar chart and return it.
    '''
    if df.empty:
        fig = px.bar(title=title, height=height)
        fig.add_annotation(text="No data available", showarrow=False)
        return fig
    
    fig = px.bar(df, x=x, y=y, 
                 text=text,
                 barmode = barmode, 
                 color = color,
                 orientation=orientation, 
                 hover_data=hover_data,
                 labels = labels)
    fig.update_layout(
        title=title,
        xaxis_title = xaxis_title,
        yaxis_title = yaxis_title,
        height=height, 
        margin=dict(l=l_margin, r=r_margin, t=t_margin, b=b_margin)
        )
    fig.update_traces(textposition = 'auto', texttemplate=texttemplate)
    return fig

# region LINE CHART -------------------------------------------------------
def create_line_chart(df: pd.DataFrame, x: str, y: str,
                      title: str | None = None,
                      xaxis_title: str | None = None,
                      yaxis_title: str | None = None,
                      height: int = 350,
                      text: str | None = None,
                      hover_data: list | None = None) -> Figure:
    '''
    Create a line chart with markers and return it.
    '''
    if df.empty:
        fig = px.line(title=title, height=height)
        fig.add_annotation(text="No data available", showarrow=False)
        return fig
    
    fig = px.line(df, x=x, y=y, markers=True, text=text, hover_data=hover_data)
    fig.update_layout(
        title=title,
        xaxis_title = xaxis_title,
        yaxis_title = yaxis_title,
        height=height, 
        margin=dict(l=l_margin, r=r_margin, t=t_margin, b=b_margin)
        )
    return fig

# region PIE CHART -------------------------------------------------------
def create_pie_chart(df: pd.DataFrame, 
                       names:str,
                       values:str,
                       title:str,
                       height: int = 350,
                       hover_data: list | None = None,
                       hole:float = 0.0,
                       texttemplate: str|None = None) -> Figure:
    '''
    Create a donut chart and return it.
    '''

    if df.empty:
        fig = px.pie(title = title, height = height)
        fig.add_annotation(text="No data available", showarrow=False)
        return fig
    
    fig = px.pie(df,names = names, values=values, hover_data=hover_data,  hole = hole)
    fig.update_layout(
        title=title,
        height=height,
        margin=dict(l=l_margin, r=r_margin, t=t_margin, b=b_margin)
    )
   
    fig.update_traces(textposition='inside', texttemplate=texttemplate, insidetextorientation = 'horizontal')

    return fig

# region SCATTER CHART ------------------------------------------------------------
def create_scatter_chart(df: pd.DataFrame, x: str, y: str, 
                         size: str | None = None,
                         color: str | None = None, 
                         title: str | None = None, 
                         xaxis_title: str | None = None, 
                         yaxis_title: str | None = None,
                         opacity: float = 0.8,
                         size_max: float = 15,
                         height: int = 350, 
                         hover_data: list | dict | None = None,
                         labels: dict | None = None,
                         showlegend: bool = False
                         ) -> Figure:
    '''
    Create a scatter chart and return it.
    '''
    if df.empty:
        fig = px.scatter(title = title, height = height)
        fig.add_annotation(text = 'No data available', showarrow=False)
        return fig
    else:
        fig = px.scatter(df,
                         x=x, y=y,
                         color=color,
                         size = size,
                         hover_data=hover_data,
                         labels=labels,
                         opacity = opacity,
                         size_max = size_max
                         )
        fig.update_layout(title=title,
                        xaxis_title=xaxis_title,
                        yaxis_title=yaxis_title,
                        height=height,
                        showlegend=showlegend,
                        margin = dict(l=l_margin, r=r_margin, t=t_margin, b=b_margin)
                         )
        return fig

# region HEATMAP ------------------------------------------------------------------
def create_heatmap(df: pd.DataFrame, x: str, y: str, z: str, 
                   title: str | None = None,
                   xaxis_title: str | None = None, 
                   yaxis_title: str | None = None,
                   color_scale: str = "Blues", 
                   height: int = 350) -> Figure:
    '''
    Create an origin-destination density heatmap and return it.
    '''
    if df.empty:
        fig = px.density_heatmap(title=title, height=height)
        fig.add_annotation(text="No data available", showarrow=False)
        return fig

    fig = px.density_heatmap(
        df,
        x=x,
        y=y,
        z=z,
        histfunc="sum",
        title=title,
        height=height,
        color_continuous_scale=color_scale
    )
    
    fig.update_layout(
        xaxis_title=xaxis_title if xaxis_title else x,
        yaxis_title=yaxis_title if yaxis_title else y,
        margin=dict(l=l_margin, r=r_margin, t=t_margin, b=b_margin)
    )
    return fig

# region DATA TABLE ---------------------------------------------------------------
def display_data_table(df: pd.DataFrame, height: int = 350) -> None:
    '''
    Renders a standardized streamlit dataframe with the index hidden.
    '''
    if df.empty:
        st.info("No data available to display in the table.")
        return

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        height=height
    )