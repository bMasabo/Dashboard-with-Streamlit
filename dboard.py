#Turning an excel sheet into an interactive dashboard using python (streamlit)
#coding is fun
#https://www.youtube.com/watch?v=Sb0A9i6d320

import pandas as pd

import plotly.express as px

import streamlit as st

st.set_page_config(page_title="SALES DASHBOARD",
                    page_icon=":bar_chart:",
                    layout="wide"
        )

st.title("SALES DATA")
st.markdown("##")


#creating a function to get data from excel
#storing the function as cache to optimize functionality
#no need to get data everytime we run code

@st.cache
def get_data_from_excel():
    df=pd.read_excel(
                io="SALES.xlsx",
                 engine="openpyxl",
                 sheet_name="Sales",
                 skiprows=3,
                 usecols="B:R",
                 nrows=1000
   )
   
    #------ADD HOUR COLUMN TO DATAFRAME-----
    df["hour"] = pd.to_datetime(df["Time"],format="%H:%M:%S").dt.hour
    #st.dataframe(df)
    return df
    
df = get_data_from_excel()

#________SIDEBAR_________

st.sidebar.header("Filter by City:")
city = st.sidebar.multiselect(
"Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
"Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
"Select the Customer Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection=df.query(
    "City==@city&Customer_type==@customer_type&Gender==@gender"
    )
    
st.dataframe(df_selection)


#________________MAIN PAGE_____________
st.title(":bar_chart: DashBoard")
st.markdown("##")


#TOP KPIs
total_sales = int(df_selection["Total"].sum())
average_rating=round(df_selection["Rating"].mean(),0)
star_rating = ":star:"*int(round(average_rating,0))
average_sale_by_transaction = round(df_selection["Total"].mean(),2)


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"${total_sales:,}") 
    
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{star_rating}")
    
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"$ {average_sale_by_transaction}")
    
st.markdown("---")
   
   
#_____SALES BY PRODUCT LINE______
sales_by_product_line=df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"]*len(sales_by_product_line),
    template="plotly_white",
    )
    
fig_product_sales.update_layout(
    plot_bgcolor="rgb(0,0,2)",
    xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False))
    )
#st.plotly_chart(fig_hourly_sales)  
    




#___________SALES BY HOUR[BAR CHART]________________

sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    #orientation="h",
    title="<b>Hourly Sales</b>",
    color_discrete_sequence=["#0038b8"]*len(sales_by_hour),
    template="plotly_white",
    )

fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0)",
    yaxis=(dict(showgrid=False)),
    )
#st.plotly_chart(fig_hourly_sales)



 
#-------Placing the bar charts side by side
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales,use_container_width=True) 
right_column.plotly_chart(fig_product_sales, use_container_width=True)

