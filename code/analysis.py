# Import Libraries
import numpy as np
import pandas as pd
import streamlit as st
from datetime import timedelta, date
from bondDescriptions import categorize_bonds
import bondCalculator
from tablesGraphsFunctions import riskMetricsGraphs, combinedraphs, sectorARGraphs, pieGraph, descriptiveStats, descriptiveTimeSeriesStats
from tablesGraphsFunctions import create_dynamic_table, create_combined_table, bondOutput, correlationGraph, dkePlot, add_total_row

st.set_page_config(layout="wide")
pd.set_option('mode.chained_assignment', None)


# NinetyOne Colour Scheme
ninety1Heading = '#104140'
ninety1Light = '#f8ac96'
ninety1Dark = '#c0756d'
ninety1Total = "#ca7f21"


# Time Series Sheet
timeSeriesSheetName='Risk Metrics (Time Series)'

# Read Data File
@st.cache_data
def readData(file):
    df = pd.read_excel(file,sheet_name=None)
    return df


#### Upload File - Side Bar #########################
#####################################################
st.sidebar.image('ninety1Pink.png', width=125)
st.sidebar.header('Drop File Here')
data = st.sidebar.file_uploader("Choose a file", type='xlsx')


#### Bond Calcs - Side Bar #############################
########################################################
today = date.today()
ninety_days_ago = today - timedelta(days=90)
ninety_days_fwd = today + timedelta(days=90)
mature = today + timedelta(days=3650) 

bondCalcs = st.sidebar.toggle('Bond Calcs')

if bondCalcs:

    st.sidebar.subheader('Bond Inputs')

    yieldNum = st.sidebar.number_input('YTM', min_value=0.00, max_value=20.00, format='%0.5f', step=0.25, value=8.00)
    couponNum = st.sidebar.number_input('Coupon', min_value=0.00, max_value=20.00, format='%0.5f', step=0.25, value=8.00)

    ytm = yieldNum/100
    coupon = couponNum/100

    lcd = st.sidebar.date_input('Last Coupon Date',ninety_days_ago)
    ncd = st.sidebar.date_input('Next Coupon Date',ninety_days_fwd )
    settle = st.sidebar.date_input('Settlement Date',today)
    maturity = st.sidebar.date_input('Maturity Date',mature)
    bcd = ncd - timedelta(days=10)

    nPeriods = bondCalculator.nperiods(ncd, maturity)
    cumex = bondCalculator.cumex(settle, bcd)
    daysAcc = bondCalculator.daysacc(settle, lcd, ncd, cumex)
    couponPay = bondCalculator.couponPay(coupon, cumex)
    factor = bondCalculator.factor(ytm)
    brokenPeriod = bondCalculator.brokenPeriod(settle, lcd, ncd, maturity)
    accInt = bondCalculator.accint(daysAcc, coupon)
    accIntRound = bondCalculator.accintRound(daysAcc, coupon)
    brokenPeriodDF = bondCalculator.brokenPeriodDF(factor, brokenPeriod, ncd, maturity)
    aip0 = bondCalculator.aip(nPeriods, brokenPeriodDF, couponPay, coupon, factor, 1)
    clean = bondCalculator.clean(aip0, accInt)
    cleanround = bondCalculator.cleanRound(aip0, accInt)
    aip0Round = bondCalculator.aipRound(cleanround, accIntRound)

    dirtyPrice = round(aip0Round*100,5)
    cleanPrice = round(cleanround*100,5)
    accrual = round(accIntRound*100,5)
    duration = round(bondCalculator.durationfinal(settle, lcd, ncd, bcd, maturity, coupon, ytm),5)
    mdDuration = round(bondCalculator.modfinal(settle, lcd, ncd, bcd, maturity, coupon, ytm),5)
    delta = round(bondCalculator.deltafinal(settle, lcd, ncd, bcd, maturity, coupon, ytm),5)
    rpbp = round(bondCalculator.rpbpfinal(settle, lcd, ncd, bcd, maturity, coupon, ytm),5)
    convexity = round(bondCalculator.convexityfinal(settle, lcd, ncd, bcd, maturity, coupon, ytm),5)

    headerVals = ['<b>Metric</b>', '<b>Value</b>']
    outputMetrics = ['Dirty Price', 'Clean Price', 'Accrual', 'Duration', 'Modified Dur', 'Delta', 'RPBP', 'Convexity']
    output = [dirtyPrice, cleanPrice, accrual, duration, mdDuration, delta, rpbp, convexity]

    vals = [outputMetrics, output]

    bondOutputs = bondOutput(headerVals, vals)

    st.sidebar.subheader('Bond Outputs')
    st.sidebar.plotly_chart(bondOutputs)

    st.sidebar.markdown("<i style='text-align: left; color: charcoal; padding-left: 0px; font-size: 15px'><b>JSE Bond Pricer Link - https://bondcalculator.jse.co.za/BondSingle.aspx?calc=Spot<b></i>", unsafe_allow_html=True)

###############################################
################################################

###### Fund Overview ############################
#################################################  

colImg, colHeader = st.columns([1,7])

if data:
    colImg.image('ninety1Orange.png')
    colHeader.header('Fixed Income Fund Analysis')
    st.markdown(' ')
    st.markdown(' ')
else:
    colImg.image('ninety1Orange.png')
    colHeader.header('Please Upload File')
    st.markdown(' ')
    st.markdown(' ')

if data is not None:
    try:
        st.subheader('Overview')
        df = readData(data)
        all_sheet = pd.ExcelFile(data)   
        sheetNames = all_sheet.sheet_names
        sheetNames.remove(timeSeriesSheetName)



        for i in sheetNames:
            df[i] = df[i].fillna(1)
            df[i]['Active Total Risk'] = np.where(df[i]['Active Total Risk'] > 100, df[i]['Active Spread Duration'], df[i]['Active Total Risk'])
            df[i]['Active Effective Duration (MAC)'] = np.where(df[i]['Active Effective Duration (MAC)'] > 100, df[i]['Active Spread Duration'], df[i]['Active Effective Duration (MAC)'])
            df[i]['Active Effective Duration (MAC)'] = np.where(df[i]['Active Effective Duration (MAC)'] < -100, df[i]['Active Spread Duration'], df[i]['Active Effective Duration (MAC)'])
        
       
        col1, a, col2 = st.columns([1,0.1, 1])
        col3, b, col4 = st.columns([1,0.1, 1])
        col5, c, col6 = st.columns([1,0.1, 1])
       
        portfolio1 = col1.selectbox('Select timeperiod',sheetNames)
       
        df_categorized = categorize_bonds(df[portfolio1])

        # Get a list of all numeric columns
        numeric_columns = df_categorized.select_dtypes(include=['number']).columns.tolist()
        numeric_columns.remove('Maturity_Year')
        numeric_columns.remove('Dirty Price')
        numeric_columns.remove('Price')

        percentageColumns = ['Weight (%)','Bmk Weight (%)', 'Active Weight (%)']

        selectedCols = col2.multiselect('Choose Attributes', numeric_columns,['Weight (%)', 'Bmk Weight (%)', 'Active Weight (%)', 'Active Total Risk'])

        df_groupedSector = df_categorized.groupby('Sector')[selectedCols].sum()

        selected_option = col4.radio("Select an option:", selectedCols, horizontal=True)

        figSectorGraph=sectorARGraphs(df_groupedSector, selected_option,percentageColumns, portfolio=portfolio1)

        col4.plotly_chart(figSectorGraph)

        df_groupedSector = add_total_row(df_groupedSector)

        indexOrderSector = ['Cash', 'Corp Bond', 'Banking', 'Credit', 'Insurance', 'Municipal', 'Real Estate', 'SOE', 'Sovereign', 'Total']

        df_groupedSector= df_groupedSector.reindex(indexOrderSector)

        sector_table = create_dynamic_table(df_groupedSector, 'Sector', portfolio1, None, 1200, 450)
        
        col3.plotly_chart(sector_table)

        df_groupedBucket= df_categorized.groupby('Bucket')[selectedCols].sum()

        figBucketGraph=sectorARGraphs(df_groupedBucket, selected_option,percentageColumns, portfolio=portfolio1)

        col4.plotly_chart(figBucketGraph)

        df_pieBucket = df_categorized.groupby('Bucket')['Active Total Risk'].sum().round(2)

        df_groupedBucket = add_total_row(df_groupedBucket)

        indexOrderBucket = ['0-3 years', '3-7 years', '7-12 years', '12+ years', 'Total']

        df_groupedBucket= df_groupedBucket.reindex(indexOrderBucket)

        bucket_table = create_dynamic_table(df_groupedBucket, 'Bucket', portfolio1, None, 1200, 300)
        
        col3.plotly_chart(bucket_table)

        descriptiveDF = df_categorized[selectedCols]
        check = descriptiveStats(descriptiveDF, portfolio1)
        col5.plotly_chart(check)

        figBucketPie=pieGraph(df_pieBucket)
        col6.plotly_chart(figBucketPie)

        col7, col8 = st.columns([2,13])
        showTable = col7.radio('Show Data Table', ['No', 'Yes'], horizontal=True, index=0)

        if showTable == 'Yes':

            filterTable = col8.toggle('Fiter Assets')

            col9, col10 = st.columns([1,1])
            if filterTable:
                with col9:
                    col11, col12 = st.columns([1,1])
                    metric = col11.radio('Metric to Filter', ['Bucket', 'Issuer', 'Sector'], index=0, horizontal=True)

                    if metric == 'Bucket':
                        target = col12.selectbox('Bucket: ',df_categorized['Bucket'].unique().tolist(),index=0)
                        df_filtered = df_categorized[df_categorized['Bucket'] == target]
                    elif metric == 'Issuer':
                        target = col12.selectbox('Issuer: ',df_categorized['Issuer'].unique().tolist(),index=0)
                        df_filtered = df_categorized[df_categorized['Issuer'] == target]
                    else:
                        target = col12.selectbox('Sector: ',df_categorized['Sector'].unique().tolist(),index=0)
                        df_filtered = df_categorized[df_categorized['Sector'] == target]
            else:
                df_filtered = df_categorized

            table = create_dynamic_table(df_filtered, None, portfolio1, None, 1200, 450)

            st.plotly_chart(table)


###### Fund Comparison ############################
################################################### 

        dataComparison = st.toggle('Fund Comparison')

        if dataComparison:

            st.subheader('Fund Comparison')
            st.markdown(" ")
            st.markdown(" ")
            
            aCOL, bCOL = st.columns([2,2])

            with aCOL:
                colA, colB, colC = st.columns([1,1,1])

                portfolioA = colA.selectbox('Select timeperiod 1',sheetNames, index=0)
                portfolioB = colB.selectbox('Select timeperiod 2',sheetNames, index=1)
                graphMetric = colC.selectbox('Metric to Compare', numeric_columns,index=0)

        
            df_categorized_A = categorize_bonds(df[portfolioA])
            df_categorized_B = categorize_bonds(df[portfolioB])

    
            df_Sector_A = df_categorized_A.groupby('Sector')[numeric_columns].sum()
            df_Sector_B = df_categorized_B.groupby('Sector')[numeric_columns].sum()

            indexOrderSector = ['Cash', 'Corp Bond', 'Banking', 'Credit', 'Insurance', 'Municipal', 'Real Estate', 'SOE', 'Sovereign']

            df_Sector_A= df_Sector_A.reindex(indexOrderSector)
            df_Sector_B= df_Sector_B.reindex(indexOrderSector)


            df_Sector_A = add_total_row(df_Sector_A)
            df_Sector_B = add_total_row(df_Sector_B)

            df_Sector_A = df_Sector_A[graphMetric]
            df_Sector_B = df_Sector_B[graphMetric]

            sector_df = pd.DataFrame({
                portfolioA+'-T1': df_Sector_A,
                portfolioB+'-T2': df_Sector_B
            })


            df_Bucket_A= df_categorized_A.groupby('Bucket')[numeric_columns].sum(2)
            df_Bucket_B= df_categorized_B.groupby('Bucket')[numeric_columns].sum(2)


            indexOrder = ['0-3 years', '3-7 years', '7-12 years', '12+ years']

            df_Bucket_A= df_Bucket_A.reindex(indexOrder)
            df_Bucket_B= df_Bucket_B.reindex(indexOrder)

            df_Bucket_A = add_total_row(df_Bucket_A)
            df_Bucket_B = add_total_row(df_Bucket_B)

            df_Bucket_A = df_Bucket_A[graphMetric]
            df_Bucket_B = df_Bucket_B[graphMetric]
            
            # Create a new DataFrame with these Series as columns
            bucket_df = pd.DataFrame({
                portfolioA+'-T1': df_Bucket_A,
                portfolioB+'-T2': df_Bucket_B
            })

            col13, e, col14 = st.columns([1,0.1,1])

            combined_sector = create_combined_table(sector_df, "Sector", graphMetric, 600, 500)

            col14.markdown(" ")
            col14.markdown(" ")
            col14.plotly_chart(combined_sector)

            combined_bucket = create_combined_table(bucket_df, "Bucket", graphMetric, 600, 300)

            col14.plotly_chart(combined_bucket)


            combSectorGraphs = combinedraphs(sector_df, graphMetric, "Sector",475,600)

            col13.plotly_chart(combSectorGraphs)


            combBucketGraphs = combinedraphs(bucket_df, graphMetric, "Bucket",335,600)

            col13.markdown(" ")
            col13.markdown(" ")
            col13.plotly_chart(combBucketGraphs)

###################################################
################################################### 


###### Time Series ################################
################################################### 
        timeSeriesAnalysis = st.toggle('Time Series Analysis')

        if timeSeriesAnalysis:

            st.header('Time Series Analysis')

            riskTimeSeries = riskMetricsGraphs(df, 500, 1200)
            timeSeriesStats = descriptiveTimeSeriesStats(df)
            correlationMatrix = correlationGraph(df)

            st.plotly_chart(riskTimeSeries)

            col20, col21 = st.columns([1,1])
            
            col20.plotly_chart(correlationMatrix)
            col21.markdown(" ")
            col21.markdown(" ")
            col21.plotly_chart(timeSeriesStats)

            col14, col15, col16 = st.columns([1,1,1])

            attribute = col14.selectbox("Select Attribute", ['BetaP', 'Tracking Error (Ex Ante)', 'SpreadDuration (Active)', 'CreditSpreadDur (Active)'], index=1)
            percentile = col15.number_input('Percentile', min_value=0.00, max_value=1.00, format='%0.2f', step=0.05, value=0.95)
            pVal = round(df[timeSeriesSheetName][attribute].quantile(percentile),5)
            col16.markdown(f"<h1 style='text-align: left; color: #f8ac96; padding-left: 20px; font-size: 40px'><b>{pVal}<b></h1>", unsafe_allow_html=True)


            kdeDist = dkePlot(df, attribute)

            st.plotly_chart(kdeDist)
#############################################
#############################################
    except Exception as e:
        st.markdown(e)
