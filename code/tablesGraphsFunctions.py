# Import Libraries
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go

pd.set_option('mode.chained_assignment', None)


# NinetyOne Colour Scheme
ninety1Heading = '#104140'
ninety1Light = '#f8ac96'
ninety1Dark = '#c0756d'
ninety1Total = "#ca7f21"

# Time Series Sheet
timeSeriesSheetName='Risk Metrics (Time Series)'

#riskMetrics - Time Series
def riskMetricsGraphs(df,height, width):
    figRiskMetrics = go.Figure()

    figRiskMetrics.add_trace(
    go.Scatter(
        x=df[timeSeriesSheetName]['ReferenceDate'],
        y=df[timeSeriesSheetName]['BetaP'],
        name='BetaP',
        line_color=ninety1Light,
        showlegend=True,
    ))

    figRiskMetrics.add_trace(
    go.Scatter(
        x=df[timeSeriesSheetName]['ReferenceDate'],
        y=df[timeSeriesSheetName]['Tracking Error (Ex Ante)'],
        name='TE',
        line_color="#fbac28",
        showlegend=True,
    ))

    figRiskMetrics.add_trace(
    go.Scatter(
        x=df[timeSeriesSheetName]['ReferenceDate'],
        y=df[timeSeriesSheetName]['SpreadDuration (Active)'],
        name='Spread',
        line_color=ninety1Dark,
        showlegend=True,
    ))

    figRiskMetrics.add_trace(
    go.Scatter(
        x=df[timeSeriesSheetName]['ReferenceDate'],
        y=df[timeSeriesSheetName]['CreditSpreadDur (Active)'],
        name='Credit',
        line_color=ninety1Total,
        showlegend=True,
    ))

    figRiskMetrics.update_layout(title_text='Risk Metrics',
                                height=height,
                                width=width,
                                legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=-0.2,
                                xanchor="center",
                                x=0.45
                                )
                                #  margin=dict(t=0, b=0, l=0, r=0))
                            )

    return figRiskMetrics


# Combined Graphs - Overview
def combinedraphs(df, attribute, type, height, width):

    selected_columns = df.columns.tolist()

    percentageColumns = ['Weight (%)','Bmk Weight (%)', 'Active Weight (%)']

    if attribute in percentageColumns:
        template = '%{y:.2%}'
    else:
        template='%{y:,.2f}'

    if type == 'Bucket':
        hoverName="Risk: "+template+'<br>'+'Bucket: '+'%{x}'
    elif type == 'Sector':
        hoverName="Risk: "+template+'<br>'+'Sector: '+'%{x}'    
    else:
        hoverName="Risk: "+template

    figGraph = go.Figure()
    
    figGraph.add_trace(go.Bar(x=df.index, y=df[selected_columns[0]],
                hovertext=df.index,text=df[selected_columns[0]],
                marker_color="#f8ac96",
                name=selected_columns[0]))
    
    figGraph.add_trace(go.Bar(x=df.index, y=df[selected_columns[1]],
                hovertext=df.index,text=df[selected_columns[1]],
                marker_color='#c0756d',
                name=selected_columns[1]))
    # Customize aspect
    figGraph.update_traces(
                    marker_line_width=1.5,
                    texttemplate=template,
                    hovertemplate=hoverName
                    )
    figGraph.update_layout(title_text=attribute+' - Comparison',
                                height=height,
                                width=width,
                                legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=-0.35,
                                xanchor="center",
                                x=0.45
                                )
                            )
    return figGraph


# Sector Graphs - Overview
def sectorARGraphs(df, attribute, percentageColumns, portfolio):

    if attribute in percentageColumns:
        template = '%{y:.2%}'
    else:
        template='%{y:,.2f}'

    figSectorGraph = go.Figure()
    
    figSectorGraph.add_trace(go.Bar(x=df.index, y=df[attribute],
                hovertext=df.index,text=df[attribute],
                name=portfolio))
    # Customize aspect
    figSectorGraph.update_traces(marker_color='#f8ac96', marker_line_color='#c0756d',
                    marker_line_width=1.5,
                    texttemplate=template,
                    hovertemplate="Risk: "+template+'<br>'+'Sector: '+'%{x}',
                    )
    figSectorGraph.update_layout(title_text=portfolio+" - "+attribute,
                                 height=350,
                                 width=600,
                                 font=dict(color='white')
                            )

    return figSectorGraph


# Pie Graph - Oveview
def pieGraph(df):

    figBucketPie = px.pie(df, names=df.index, values = 'Active Total Risk',
                        title="Active Risk Exposure Bucketed", hole=0.5,
                        color=df.index, 
                        color_discrete_map={'0-3 years':'rgb(251,172,40)',
                                            '3-7 years':'rgb(202,127,33)',
                                            '7-12 years':'rgb(248,172,150)',
                                            '12+ years':'rgb(192,117,109)'})
    
    figBucketPie.update_layout(title_x=0.1,
                            width=375,  # Set the width (smaller value = smaller chart)
                            height=250,
                            margin=dict(t=50, b=0, l=20, r=0), 
                            legend=dict(
                                orientation="v",
                                yanchor="bottom",
                                y=0.3,
                                xanchor="center",
                                x=1.3
                            ))
    
    return figBucketPie


# Descriptive Statistics - Overview
def descriptiveStats(df,pf):
    selected_columns = df.columns.tolist()

    even_color = ninety1Light
    odd_color=ninety1Dark

    num_rows = df.shape[0]

    alternating_colors = np.array([odd_color, even_color] * (num_rows // 2 + 1))[:num_rows]

    headerName = [f'<b>Metric</b>']

    percentColumns = ['Weight (%)','Bmk Weight (%)', 'Active Weight (%)']

    vals = [[f'<b>Max</b>', f'<b>Min</b>', f'<b>Range</b>', f'<b>Mean</b>', f'<b>Median</b>']]
    for col in selected_columns:
        if col in percentColumns:
            max = '{:.2%}'.format(df[col].max())
            min = '{:.2%}'.format(df[col].min())
            rg = '{:.2%}'.format(df[col].max() - df[col].min())
            avg = '{:.2%}'.format(df[col].mean())
            median = '{:.2%}'.format(df[col].median())
            stats = [max, min, rg, avg, median]
            vals.append(stats)
            headerName.append(f'<b>{col}</b>')
        else:
            max = '{:,.2f}'.format(df[col].max())
            min = '{:,.2f}'.format(df[col].min())
            rg = '{:,.2f}'.format(df[col].max() - df[col].min())
            avg = '{:,.2f}'.format(df[col].mean())
            median = '{:,.2f}'.format(df[col].median())
            stats = [max, min, rg, avg, median]
            vals.append(stats)
            headerName.append(f'<b>{col}</b>')

    # Create a table figure
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=headerName,
            fill_color='#ca7f21',
            line_color='darkslategray',
            align='center',
            font=dict(size=12,
                    color='white',
            ),
            height=40
            
        ),
        cells=dict(
            values=vals,
            fill_color=[alternating_colors] * len(df.columns),
            line_color='darkslategray',
            align='center',
            height=35  # Fixed height for data cells
        ),
        columnwidth=30
    )])




    # Set fixed dimensions for the entire table
    fig.update_layout(
        autosize=False,
        width=600,
        height=275,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    
    # Update layout with any specified dimensions
    layout_params = {}
    
    # Add title and adjust other layout parameters
    layout_params.update({
        'title': pf+' - Descriptive Statistics',
        'title_x': 0,  # Center the title
    })
    
    fig.update_layout(**layout_params)
    return fig


# Descriptive Statistics - Time Series
def descriptiveTimeSeriesStats(df):

    df_numeric = df[timeSeriesSheetName][['BetaP', 'Tracking Error (Ex Ante)', 'SpreadDuration (Active)', 'CreditSpreadDur (Active)']]
    selected_columns = df_numeric.columns.tolist()

    even_color = ninety1Light
    odd_color=ninety1Dark

    num_rows = 5

    alternating_colors = np.array([odd_color, even_color] * (num_rows // 2 + 1))[:num_rows]

    headerName = [f'<b>Metric</b>']

    vals = [[f'<b>Max</b>', f'<b>Min</b>', f'<b>Range</b>', f'<b>Mean</b>', f'<b>Median</b>']]
    for col in selected_columns:

        max = '{:,.2f}'.format(df_numeric[col].max())
        min = '{:,.2f}'.format(df_numeric[col].min())
        rg = '{:,.2f}'.format(df_numeric[col].max() - df_numeric[col].min())
        avg = '{:,.2f}'.format(df_numeric[col].mean())
        median = '{:,.2f}'.format(df_numeric[col].median())
        stats = [max, min, rg, avg, median]
        vals.append(stats)
        headerName.append(f'<b>{col}</b>')

    # Create a table figure
    figTime = go.Figure(data=[go.Table(
        header=dict(
            values=headerName,
            fill_color='#ca7f21',
            line_color='darkslategray',
            align='center',
            font=dict(size=12,
                    color='white',
            ),
            height=40
            
        ),
        cells=dict(
            values=vals,
            fill_color=[alternating_colors] * 4,
            line_color='darkslategray',
            align='center',
            height=35  # Fixed height for data cells
        ),
        columnwidth=30
    )])

    # Set fixed dimensions for the entire table
    figTime.update_layout(
        autosize=False,
        width=600,
        height=300,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    
    # Update layout with any specified dimensions
    layout_params = {}
    
    # Add title and adjust other layout parameters
    layout_params.update({
        'title': 'Descriptive Statistics',
        'title_x': 0.35,  # Center the title
    })
    
    figTime.update_layout(**layout_params)

    return figTime


# Dynamic Table - Overview
def create_dynamic_table(dataframe, type, pf, selected_columns=None, width=None, height=None):

    # If no columns are specified, use all columns
    if selected_columns is None:
        selected_columns = dataframe.columns.tolist()

    palette = px.colors.qualitative.Set3

    even_color = ninety1Light
    odd_color=ninety1Dark

    
    noFormat = ['Asset ID', 'Asset Name', 'Issuer', 'Sector', 'Bucket']

    percentColumns = ['Weight (%)','Bmk Weight (%)', 'Active Weight (%)']

    # Filter the dataframe to only include selected columns
    filtered_df = dataframe[selected_columns]

    num_rows = filtered_df.shape[0]

    if((type == 'Bucket') or (type == 'Sector')):
        # Create an array of alternating colors based on row count
        alternating_colors = np.array([even_color, odd_color] * (num_rows // 2 + 1))[:num_rows-1]
        # Add green color for the last row
        alternating_colors = np.append(alternating_colors, ninety1Heading)
    else:
        alternating_colors = np.array([even_color, odd_color] * (num_rows // 2 + 1))[:num_rows]

    valueList=[]

    colWidth=[]
    headerName = []

    for i in selected_columns:
        if i in noFormat:
            valueList.append(filtered_df[i].to_list())
        elif i in percentColumns:
            valueList.append(filtered_df[i].map('{:.2%}'.format).to_list())
        else:
            valueList.append(filtered_df[i].map('{:,.2f}'.format).to_list())

    for j in selected_columns:
        if j == 'Asset Name':
            colWidth.append(750)
            headerName.append(f'<b>{j}</b>')
        elif j == 'Asset ID':
            colWidth.append(400)
            headerName.append(f'<b>{j}</b>')
        elif j == 'Issuer':
            colWidth.append(400)
            headerName.append(f'<b>{j}</b>')
        elif j == 'Sector':
            colWidth.append(300)
            headerName.append(f'<b>{j}</b>')
        elif j == 'Bucket':
            colWidth.append(300)
            headerName.append(f'<b>{j}</b>')
        elif j == 'Holdings':
            colWidth.append(300)
            headerName.append(f'<b>{j}</b>')
        elif j == 'Weight (%)':
            colWidth.append(200)
            headerName.append(f'<b>Portf Weight</b>')
        elif j == 'Bmk Weight (%)':
            colWidth.append(200)
            headerName.append(f'<b>Bmk Weight</b>')
        elif j == 'Active Weight (%)':
            colWidth.append(200)
            headerName.append(f'<b>Active Weight</b>')
        elif j == 'Active Total Risk':
            colWidth.append(200)
            headerName.append(f'<b>Total Risk</b>')
        elif j == 'MC to Active Total Risk':
            colWidth.append(200)
            headerName.append(f'<b>MC</b>')
        elif j == '%CR to Active Total Risk':
            colWidth.append(200)
            headerName.append(f'<b>%CR</b>')
        elif j == '%CR to Active Total Risk':
            colWidth.append(200)
            headerName.append(f'<b>%CR</b>')
        elif j == 'Active Effective Duration (MAC)':
            colWidth.append(250)
            headerName.append(f'<b>Effective Duration</b>')
        elif j == 'Active Spread Duration':
            colWidth.append(250)
            headerName.append(f'<b>Spread Duration</b>')
        elif j == 'Maturity_Year':
            colWidth.append(200)
            headerName.append(f'<b>Years</b>')
        else:
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')

    
    tableHeading = ''

    if type == 'Bucket':
        headerName.insert(0, f'<b>Bucket</b>')
        valueList.insert(0, dataframe.index)
        tableHeading = pf+' - Time Bucket Exposure'
        spacing=0.2
    elif type == 'Sector':
        headerName.insert(0,f'<b>Sector</b>')
        valueList.insert(0, dataframe.index)
        tableHeading = pf+' - Sector Exposure'
        spacing=0.25
    else:
        tableHeading = pf+' - Asset Exposure'
        spacing=0.4

    if((type == 'Bucket') or (type == 'Sector')):
        bold_valueList = []
        for col_values in valueList:
            # Convert to a list first (which is mutable)
            modified_values = list(col_values)
            
            # Apply bold formatting to the last item
            modified_values[-1] = f"<b>{modified_values[-1]}</b>"
            
            bold_valueList.append(modified_values)
    else:
        bold_valueList=valueList

    
    # Create a table figure
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=headerName,
            fill_color="#ca7f21",
            line_color='darkslategray',
            align='center',
            font=dict(size=12,
                    color='white',

            ),
            height=40
            
        ),
        cells=dict(
            values=bold_valueList,
            fill_color=[alternating_colors] * len(filtered_df.columns),
            line_color='darkslategray',
            align='center',
            height=35  # Fixed height for data cells
        ),
        columnwidth=colWidth
    )])


    # Set fixed dimensions for the entire table
    fig.update_layout(
        autosize=False,
        width=width,
        height=height,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    
    # Update layout with any specified dimensions
    layout_params = {}
    
    # Add title and adjust other layout parameters
    layout_params.update({
        'title': tableHeading,
        'title_x': 0,
        # 'title_x': spacing,  # Center the title

    })
    
    fig.update_layout(**layout_params)
    
    return fig



# Dynamic Table - Fund Comparison 
def create_combined_table(filtered_df, type, metric, width=None, height=None):

    selected_columns=filtered_df.columns.tolist()

    even_color = ninety1Light
    odd_color=ninety1Dark

    percentColumns = ['Weight (%)','Bmk Weight (%)', 'Active Weight (%)']

    num_rows = filtered_df.shape[0]

    if((type == 'Bucket') or (type == 'Sector')):
        # Create an array of alternating colors based on row count
        alternating_colors = np.array([even_color, odd_color] * (num_rows // 2 + 1))[:num_rows-1]
        # Add green color for the last row
        alternating_colors = np.append(alternating_colors, ninety1Heading)
    else:
        alternating_colors = np.array([even_color, odd_color] * (num_rows // 2 + 1))[:num_rows]

    valueList=[]

    colWidth=[]
    headerName = []

    for i in selected_columns:
        if metric in percentColumns:
            valueList.append(filtered_df[i].map('{:.2%}'.format).to_list())
        else:
            valueList.append(filtered_df[i].map('{:,.2f}'.format).to_list())

    for j in selected_columns:
        if metric == 'Asset Name':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == 'Asset ID':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == 'Issuer':
            colWidth.append(2000)
            headerName.append(f'<b>{j}</b>')
        elif metric == 'Sector':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == 'Bucket':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == 'Holdings':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == 'Weight (%)':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == 'Bmk Weight (%)':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == 'Active Weight (%)':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == 'Active Total Risk':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == 'MC to Active Total Risk':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == '%CR to Active Total Risk':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == '%CR to Active Total Risk':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == 'Active Effective Duration (MAC)':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == 'Active Spread Duration':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        elif metric == 'Maturity_Year':
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')
        else:
            colWidth.append(200)
            headerName.append(f'<b>{j}</b>')

    tableHeading = ''

    if type == 'Bucket':
        headerName.insert(0, f'<b>Bucket</b>')
        valueList.insert(0, filtered_df.index)
        tableHeading = 'Time Bucket Comparison'
    elif type == 'Sector':
        headerName.insert(0,f'<b>Sector</b>')
        valueList.insert(0, filtered_df.index)
        tableHeading = 'Sector Comparison'
    else:
        tableHeading = 'Portfolio Comparison'

    if((type == 'Bucket') or (type == 'Sector')):
        bold_valueList = []
        for col_values in valueList:
            # Convert to a list first (which is mutable)
            modified_values = list(col_values)
            
            # Apply bold formatting to the last item
            modified_values[-1] = f"<b>{modified_values[-1]}</b>"
            
            bold_valueList.append(modified_values)
    else:
        bold_valueList=valueList

    
    # Create a table figure
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=headerName,
            fill_color='#ca7f21',
            line_color='darkslategray',
            align='center',
            font=dict(size=12,
                    color='white',
            ),
            height=40
            
        ),
        cells=dict(
            values=bold_valueList,
            fill_color=[alternating_colors] * len(filtered_df.columns),
            line_color='darkslategray',
            align='center',
            height=35  # Fixed height for data cells
        ),
        columnwidth=colWidth
    )])

    # Set fixed dimensions for the entire table
    fig.update_layout(
        autosize=False,
        width=width,
        height=height,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    
    # Update layout with any specified dimensions
    layout_params = {}
    
    # Add title and adjust other layout parameters
    layout_params.update({
        'title': tableHeading,
        'title_x': 0,
    })
    
    fig.update_layout(**layout_params)
    
    return fig


# Bond Output Table - Sidebar
def bondOutput(headerVals, vals):
    palette = px.colors.qualitative.Set3

    even_color = ninety1Light
    odd_color=ninety1Dark

    num_rows = 8

    alternating_colors = np.array([odd_color, even_color] * (num_rows // 2 + 1))[:num_rows]

    # Create a table figure
    figBond = go.Figure(data=[go.Table(
        header=dict(
            values=headerVals,
            fill_color='#ca7f21',
            line_color='darkslategray',
            align='center',
            font=dict(size=12,
                    color='white',
            ),
            height=40
            
        ),
        cells=dict(
            values=vals,
            fill_color=[alternating_colors] * 2,
            line_color='darkslategray',
            align='center',
            height=35  # Fixed height for data cells
        ),
        columnwidth=30
    )])

    # Set fixed dimensions for the entire table
    figBond.update_layout(
        autosize=False,
        width=300,
        height=350,
        margin=dict(l=0, r=0, t=10, b=0)
    )

    return figBond


# def Correlation Graph - Time Series
def correlationGraph(df):

    df_numeric = df[timeSeriesSheetName][['BetaP', 'Tracking Error (Ex Ante)', 'SpreadDuration (Active)', 'CreditSpreadDur (Active)']]

    custom_color_scale = [
        [0, '#ca7f21'],    # Dark red for negative correlations
        [0.5, '#fbac28'],  # White for zero correlation
        [1, '#c0756d']    # Dark blue for positive correlations'#ca7f21'
]


    correlation = df_numeric.corr()
    figCorr = px.imshow(correlation, 
                        color_continuous_scale=custom_color_scale, 
                        text_auto='.2f', 
                        title='Correlation Matrix')
    # Update layout to adjust title position and margins
    figCorr.update_layout(
        width=500, 
        height=500,
        title={
            'text': 'Correlation Matrix',
            'x': 0.55,  # Center title (0.5) or move right (>0.5)
            'y': 0.95,  # Move title closer to the plot (default is 0.9)
            'xanchor': 'center',
            'yanchor': 'top'
        },
        margin=dict(t=20), # Reduce top margin (default is usually around 80-100)
        coloraxis_showscale=False  
    )
    
    return figCorr

# kde Normal Density Plot - Time Series
def dkePlot(df, attribute):
    figHist = ff.create_distplot([df[timeSeriesSheetName][attribute]], group_labels=[attribute], curve_type='normal', colors=['#f8ac96'], show_hist=False)
    figHist.update_layout(title=attribute+' - KDE Plot', xaxis_title=attribute, yaxis_title='Freuency Distribution', height=500, width=850, margin=dict(l=0, r=20, b=0,t=100),
        legend=dict(
        orientation="h",  # Horizontal legend
        x=0.95,            # Center the legend horizontally
        y=0.95,           # Position it slightly below the plot
        xanchor='center',  # Align legend horizontally
        yanchor='bottom'   # Align legend vertically
    ))

    return figHist

def add_total_row(df_grouped):
    # Create a total row by summing numeric columns
    total_row = pd.DataFrame(df_grouped.sum(numeric_only=True)).T
    
    # Set the index name to 'Total' for the new row
    total_row.index = ['Total']
    
    # Concatenate the original DataFrame with the total row
    result = pd.concat([df_grouped, total_row])
    
    return result