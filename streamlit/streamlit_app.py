import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment")
st.write("##### Hawkins Jean 3/31/2025")

st.write("### Input Data and Example")
df = pd.read_csv("./streamlit/Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Assignment")
st.write("(1) Add a drop down for Category")
option = st.selectbox(
    "Please Select a Category",
    ("Furniture","Office Supplies","Technology"),
)
# # Group by Category and create a dictionary
# categories = df.groupby("Category")["Sub_Category"].unique().to_dict()
#
# # Display the extracted subcategories
# st.write(categories)
#****************
st.write("(2) Add a multi-select for Sub_Category *in the selected Category")
# Define categories and subcategories
categories = {
    "Furniture":['Bookcases', 'Chairs', 'Tables', 'Furnishings'],
    "Office Supplies":['Labels', 'Storage', 'Art', 'Binders', 'Appliances', 'Paper',
       'Envelopes', 'Fasteners', 'Supplies'],
    "Technology": ['Phones', 'Accessories', 'Machines', 'Copiers']
}
# Dropdown for main category
selected_category = st.selectbox("Select a category", list(categories.keys()))

# Dropdown for subcategories based on selected category
if selected_category:
    df["Profit Margin"] = (df["Profit"] / df["Sales"]) * 100
    overall_avg_profit_margin = df["Profit Margin"].mean()
    selected_subcategory = st.multiselect("Select a subcategory", categories[selected_category])
    filtered_df = df[df["Sub_Category"].isin(selected_subcategory)]
    st.write(f"You selected: {selected_category} > {selected_subcategory}")
    filtered_df = filtered_df.groupby("Order_Date").sum().reset_index()
    st.write("(3) Show a line chart of sales for the selected items in Sub_Category")
    st.line_chart(filtered_df, y="Sales")
    total_Sales_k = round(filtered_df["Sales"].sum() / 1_000, 1)
    formatted_Sales = f"${total_Sales_k}K"
    total_Profit_k = round(filtered_df["Profit"].sum() / 1_000, 1)
    formatted_Profit= f"${total_Profit_k}K"
    total_OP_k = (total_Sales_k / total_Profit_k) * 100
    overall_profit_k = round(total_OP_k / 1_000, 1)
    formatted_PO_K = f"{round(overall_profit_k, 2)}%"
    st.write("(4) show three metrics for the selected items in Sub_Category: total sales, total profit, and overall profit margin (%)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", formatted_Sales)
    col2.metric("Total Profit", formatted_Profit)
    col3.metric("Overall Profit", formatted_PO_K)

    # Calculate the profit margin for the selected subcategories
    filtered_df["Profit Margin"] = (filtered_df["Profit"] / filtered_df["Sales"]) * 100
    selected_avg_profit_margin = filtered_df["Profit Margin"].mean()

    # Calculate the delta (difference) between the selected margin and the overall average
    margin_delta = selected_avg_profit_margin - overall_avg_profit_margin

    st.write("(5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
    # Display the profit margin with delta
    st.metric(
        label=f"Profit Margin for Selected Sub-Categories",
        value=f"{selected_avg_profit_margin:.2f}%",
        delta=f"{margin_delta:.2f}%" if margin_delta >= 0 else f"-{-margin_delta:.2f}%",
        # Show positive or negative delta
        delta_color="normal" if margin_delta >= 0 else "inverse"
    )

