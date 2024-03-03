import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_style('whitegrid')

def get_total_count_by_hour_df(hour_df):
  hour_count_df =  hour_df.groupby(by="hour").agg({"count": ["sum"]})
  return hour_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query(str('date >= "2011-01-01" and date < "2012-12-31"'))
    return day_df_count_2011

def total_registered_df(day_df):
   reg_df =  day_df.groupby(by="date").agg({
      "registered": "sum"
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_df

def total_casual_df(day_df):
   cas_df =  day_df.groupby(by="date").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

def sum_order (hour_df):
    sum_order_items_df = hour_df.groupby("hour")["count"].sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season (day_df): 
    season_df = day_df.groupby(by="season")["count"].sum().reset_index() 
    return season_df

days_df = pd.read_csv("day_df.csv")
hours_df = pd.read_csv("hour_df.csv")

datetime_columns = ["date"]
days_df.sort_values(by="date", inplace=True)
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="date", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["date"].min()
max_date_days = days_df["date"].max()

min_date_hour = hours_df["date"].min()
max_date_hour = hours_df["date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("bikesharing.jpg")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Range',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
    
main_df_days = days_df[(days_df["date"] >= str(start_date)) & 
                       (days_df["date"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["date"] >= str(start_date)) & 
                        (hours_df["date"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)
  

##Visualization
"""
Sultan Fahd Muhammad Bahruddin Yusuf  
Bangkit Academy Cohort 2024
"""
st.image("bangkit.png",width=400)


st.header(':sparkles: Bike Sharing :sparkles:')
st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011["count"].sum()
    st.metric("Total Bike Sharing", value=total_orders)

with col2:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual Users", value=total_sum)
    

with col3:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered Users", value=total_sum)


st.subheader("What times are bike sharing activity levels highest and lowest?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15),sharey=True)

sns.barplot(x="hour", y="count", data=sum_order_items_df.head(5), palette=["#2a9df4","#2a9df4","#2a9df4","#2a9df4","#2a9df4"], ax=ax[0])
ax[0].set_xlabel("Hours (PM)", fontsize=35)
ax[0].set_ylabel("Count",  fontsize=35)
ax[0].set_title("Hours with highest number of bike sharing", loc="center", fontsize=35)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="hour", y="count", data=sum_order_items_df.sort_values(by="hour", ascending=True).head(5), palette=["#2a9df4","#2a9df4","#2a9df4","#2a9df4","#2a9df4"], ax=ax[1])
ax[1].set_xlabel("Hours (AM)",  fontsize=35)
ax[1].set_title("Hours with lowest number of bike sharing", loc="center", fontsize=35)
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)


st.pyplot(fig)
st.subheader("What season do users rent the most?")

colors = ["#2a9df4","#2a9df4","#2a9df4","#2a9df4"]
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
        y="count", 
        x="season",
        data=season_df.sort_values(by="season", ascending=False),
        palette=colors,
        ax=ax
    )

ax.set_title("Graph the Numbers of Seasons", loc="center", fontsize=30)
ax.set_xlabel("Season",  fontsize=35)
ax.set_ylabel("Count",  fontsize=35)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader("Comparison of User Type Percentages")
labels = 'Casual Users', 'Registered Users'
sizes = [18.8, 81.2]
explode = (0, 0.1)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=["#c9dae6","#2a9df4"])
ax1.axis('equal')  

st.pyplot(fig1)

st.subheader("Performance of Rentals been in Recent Years")

fig2, ax = plt.subplots(figsize=(16, 8),sharey=True)
ax.plot(
    days_df["date"],
    days_df["count"],
    marker='o', 
    linewidth=2,
    color="#2a9df4"
)
ax.tick_params(axis='y', labelsize=25)
ax.tick_params(axis='x', labelsize=15)
ax.set_title("Number of Users Per Month",fontsize=30)
ax.set_xlabel("Date",  fontsize=20)
ax.set_ylabel("User Count", fontsize=20)
st.pyplot(fig2)

st.subheader("Conclusion")

"""
1 Conclusion of Question 1: At what times are bike sharing activity levels highest and lowest?
- Based on the graph above, we can observe that the time with the highest number of bike sharing users is at **17pm**, with a total of 336,860 users. Meanwhile, the time with the lowest number of bike sharing users occurs at **4am**, with only 4,428 users.

2 Conclusion of Question 2: Which season records the highest and lowest levels of bike sharing activity?
- From the graph above, the highest occurrence of bike sharing users is in the **fall season**. The number of users in the fall season is 1061129.

3 Conclusion of Question 3: How does the number of registered users compare to that of casual users?
- The percentage of registered users is **81.17%**, meanwhile for casual users it is **18.83%**.

4 Conclusion of Question 4: How has the performance of rentals been in recent years?
- The resulting graph is highly fluctuating. Upon examination, the highest number of bike sharing users in 2012 occurred in September. However, the data also shows a significant decrease in October of the same year.
"""