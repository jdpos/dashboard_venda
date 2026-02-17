import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

format_infinity = lambda s: "0" if np.isinf(s) else '{:,.2f}%'.format(s)

st.write(st.__version__)

def grafico_carteira():
    
    #st.write(table)

    dict_pivot = {'Data': table.iloc[:, :i].columns[:i], 
                  'Montante': table.iloc[:, :i].loc['Total']
                  }
    pivot_table_changed = pd.DataFrame(dict_pivot)
    #grouped = grouped.astype({'Year': float, 'Year': int})
    #grouped = grouped.astype({'Month': float, 'Month': int})
    #st.write(grouped)
    # grouped = grouped.reset_index(drop=True)
    #r = i+2
    #st.write(filtered)
    fig = px.line(pivot_table_changed, x='Data', y='Montante', title=f'Evolução da carteira até dia {date}')
    st.plotly_chart(fig)

if 'data' not in st.session_state:
    st.session_state.data = None

uploaded_file = st.file_uploader("Upload your Excel file xlsx", type=["xlsx"])

if uploaded_file:
    st.session_state.data = pd.read_excel(uploaded_file, sheet_name="Planilha1")
    df = st.session_state.data.copy()
    format_string = "%d/%m/%Y"
    df['Data_Formatada'] = df['Data'].dt.strftime(format_string)
    df = df.astype({'Papel': str, 'C_V': str})
    
if st.session_state.data is not None:
    dates = df['Data_Formatada'].unique()
    lista_dates = list(dates)
    lista_dates_time = sorted(list(df['Data'].unique()))
    date = st.sidebar.selectbox("Selecione a data:", dates)
    #styled_df = df.style.format({0: format_string, 2: '{:.0f}', 4:'{:.2f}', 5:'{:.2%}', 6:'{:.2f}'})

    #config = {
    #"Data": st.column_config.DateColumn("Data", format="DD.MM.YYYY"),
    #"Quantidade": st.column_config.NumberColumn("Quantidade", format='%.0f'),
    #"Cotacao": st.column_config.NumberColumn("Cotação", format='%.2f'),
    #"Variacao": st.column_config.NumberColumn("Variação", format='%.2f%%'),
    #"Montante": st.column_config.NumberColumn("Montante", format='%.2f')
    #}

    config = {
    "Data": st.column_config.DateColumn("Data", format="DD.MM.YYYY"),
    "Cotacao": st.column_config.NumberColumn("Cotação"),
    "Variacao": st.column_config.NumberColumn("Variação"),
    "Data_Formatada": None
    }
    if date:
        i = lista_dates.index(date)
        #st.write(date)
        #st.dataframe(df.head())
        filtered_df = df.loc[df['Data_Formatada']==date]
        filtered_df.loc['Total'] = filtered_df.sum(numeric_only=True)
        filtered_df.loc[filtered_df.index[-1], 'Quantidade'] = ''
        filtered_df.loc[filtered_df.index[-1], 'Cotacao'] = ''
        filtered_df.loc[filtered_df.index[-1], 'Variacao'] = ''
       

        filtered_df_style = filtered_df.style.format(
        {
            "Quantidade": lambda x : '{:,.0f}'.format(x) if x is not '' else '',
            "Cotacao": lambda x : '{:,.2f}'.format(x) if x is not '' else '',
            "Variacao": lambda x : '{:,.2f}%'.format(x) if x is not '' else '',
            "Montante": lambda x : '{:,.2f}'.format(x) if x is not '' else '',
            "C_V": lambda x: x if x=="C" or x=="V" else ''
        },
        thousands='.',
        decimal=',',
        )
    
        st.dataframe(filtered_df_style, hide_index=False, placeholder="", 
                 column_config=config)
        
        table = pd.pivot_table(
            df, values="Montante", index=["Papel"], columns=["Data"],
            aggfunc=np.sum, fill_value=0, margins=True, margins_name='Total')
        
        date_string = '2023-10-30 12:00:00'
        format_string1 = '%Y-%m-%d %H:%M:%S'
        # st.write(table.columns[0].to_pydatetime().strftime(format_string))
        i = i+1
        #st.write(table.iloc[:,0])
        # table.reindex(index=order, columns=order)
        #table.reindex(columns=lista_dates_time)
        #sorted_table = table["Data_Formatada"]
        #table.columns
        lista = []
        try:
            for j in range(len(table.columns)):
                lista.append(table.columns[j].to_pydatetime().strftime(format_string))
        except:
            #st.write(lista)
            pass

        lista.append('Total')
        table.columns = lista.copy()
        s_to_df = pd.DataFrame(table.iloc[:, :i])
        table_diff_change = s_to_df.diff(axis=1)
        table_diff_change_style = table_diff_change.style.format(
        precision=2,
        thousands='.',
        decimal=',',
        )
        
        st.dataframe(table_diff_change_style, placeholder="")
        table_diff_change_cumsum = table_diff_change.cumsum(axis=1) 
        table_diff_change_style_cumsum = table_diff_change_cumsum.style.format(
        precision=2,
        thousands='.',
        decimal=',',
        )
        st.dataframe(table_diff_change_style_cumsum, placeholder="")
        #table_pct_change = table.iloc[:, :-1].pct_change(axis="columns", periods=1) * 100 
        table_pct_change = s_to_df.pct_change(axis="columns", periods=1) * 100 
        table_pct_change_style = table_pct_change.style.format(
            #formatter='{:,.2f}%',
            formatter=format_infinity,
            thousands='.',
            decimal=',',
        )
        st.dataframe(table_pct_change_style, placeholder="")
        s_index = table.iloc[:,0]
        table_diff_change_pct_cum_sum = table_diff_change.cumsum(axis=1).div(s_index, axis=0)*100
        table_diff_change_pct_cum_sum = table_diff_change_pct_cum_sum.set_index(table_diff_change.index)
        table_diff_change_pct_cum_sum_style = table_diff_change_pct_cum_sum.style.format(
            #formatter='{:,.2f}%',
            formatter=format_infinity,
            thousands='.',
            decimal=',',
        )
        st.dataframe(table_diff_change_pct_cum_sum_style, placeholder="")
        grafico_carteira()