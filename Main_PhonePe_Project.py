import pandas as pd
import mysql.connector as sql
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from git.repo.base import Repo
import json
import os

#Initialising streamlit page
st.set_page_config(
    page_title = "PhonePe Pulse Data Visualization",
    layout = "wide",
    initial_sidebar_state = "auto"
)
    
with st.sidebar:
    st.title("Dashboard")
#initialising SQL connection
mydb = sql.connect(
        host = "localhost",
        user = "root",
        password = "9524320874")
mycursor = mydb.cursor(buffered=True)
mycursor.execute("USE PhonePe_Project2")


#Creating Options Menu
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                menu_icon= "menu-button-wide",
                default_index=0,
    )


#Creating Home Page
if selected == "Home":
    st.markdown("<h1 style='text-align: center; font-size: 40px; color: red;' >Data Visualization and Exploration </h1>", unsafe_allow_html=True)
    st.markdown("## :blue[A User-Friendly Tool Using Streamlit and Plotly]")
    st.markdown("### :blue[Domain :] Fintech")
    st.markdown("### :blue[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
    st.markdown("### :blue[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")

#Creating Top Charts Page
if selected == "Top Charts":
    st.markdown("## :red[Top Charts]")
    Type = st.sidebar.selectbox("Type", ("Transactions", "Users"))
    column1,column2= st.columns([1,1.5],gap="large")
    with column1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

        with column2:
            st.info(
                    """
                    In the "Top Charts" menu, users can extract valuable insights, including:

                    Overall Ranking: Users can obtain an overall ranking for a specific year and quarter, providing a comprehensive view of performance during that period.

                    Top 10 Regions: The application identifies and ranks the top 10 states, districts, and pincodes based on two significant metrics: total transaction count and the total amount spent via PhonePe. This information is crucial for understanding where PhonePe is most actively used.

                    User Activity: Users can delve into user-related insights by discovering the top 10 states, districts, and pincodes with the highest number of PhonePe users and the frequency with which they open the app. This information sheds light on user engagement patterns.

                    Mobile Brand Usage: The application also highlights the top 10 mobile brands used by PhonePe users. This analysis includes the percentage of users associated with each brand, offering insights into the device preferences of PhonePe's user base.
                    """
                    )
        
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        with col1:
            st.markdown("## :red[State]")
            mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            #Creating a pie chart
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10 States',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("### :red[District]")
            mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])
            #Creating a pie chart
            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10 Districts',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col3:
            st.markdown("### :red[Pincode]")
            mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            #Creating a pie chart
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10 Pin Codes',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :red[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            elif Year == 2023 and Quarter in [1,2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2023 Qtr 1,2,3,4")
            else:
                mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                #Creating a bar chart
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   

        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            #Creating a bar chart
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
              
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select Pincode, sum(RegisteredUsers) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            #Creating a pie chart
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            #Creating a pie chart
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)

    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.State = df2
            #Taking india map data from Geojson file and getting the State names after converting geojson file into csv and cleaning the data to get only the State Names.
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='Reds')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)


        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='Reds')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)

        
        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)

# BAR CHART TRANSACTIONS - DISTRICT WISE DATA
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :red[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)



# EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :red[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select state, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale='Reds')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :red[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select State,year,quarter,District,sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

# MENU 4 - ABOUT
if selected == "About":
    st.markdown("<h1 style='text-align: center; font-size: 40px; color: red;' > Project Completed By </h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 40px; color: red;' > Ashwin Rajh </h1>", unsafe_allow_html=True)
    linkedin_url = "https://www.linkedin.com/in/ashwin-rajh"
    st.markdown(f"<h1 style='text-align: center; font-size: 30px; color: white;'>LinkedIn Profile: <a href='{linkedin_url}'>{linkedin_url}</a></h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 30px; color: white;' > This project was completed to develop skills in data extraction, Data transformation,  Database insertion, Dashboard creation, Data retrieval, Deployment </h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 20px; color: white;' > This Streamlit application serves as a powerful tool for gaining insights into PhonePe Pulse data and is designed to be user-friendly and informative. Users can select from various options to explore and visualize data, making it a valuable resource for data analysis and reporting. The application allows users to interact with the data, select parameters, and generate dynamic visualizations, making it a versatile tool for data exploration and reporting in the Fintech domain. </h1>", unsafe_allow_html=True)




