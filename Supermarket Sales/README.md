# Project 1: Supermarket sales.

This project aims to analyze supermarket sales data to gain insights into sales trends and customer behavior using SQL. SQL (Structured Query Language) is a powerful tool for managing and querying large datasets, making it an ideal method for analyzing data.

The analysis will involve extracting the relevant data from the supermarket sales CSV file, and querying it to identify key metrics such as sales volume, revenue, and customer demographics. We will then use SQL queries and aggregation functions to identify trends over time, identify patterns in customer behavior, and understand the factors that influence sales.

By using SQL, we can efficiently query and analyze large datasets, which is essential for gaining meaningful insights into sales trends and customer behavior. Additionally, using SQL allows for easy replication of the analysis, making it a valuable tool for businesses of all sizes.

The project will be documented in a clear and concise manner, with detailed explanations of the SQL queries used and the insights gained. This will allow for easy replication of the analysis and help others to understand the value of using SQL for analyzing sales data.

## Objective: Analyzing the sales data to understand sales trends and customer behavior!
[Data Used](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales)

**Data Exploration:** First, explore the data to understand its structure and relationships. Use SQL queries to extract basic information such as number of records, unique values, and data types.

SELECT * <br />
FROM sales <br />
LIMIT 5;

|InvoiceID|Branch|City|Customertype|Gender|Productline|Unitprice|Quantity|Tax5%|Total|Date|Time|Payment|Cogs|grossmarginpercentage|Grossincome|Rating


SELECT COUNT(*) as total_records,<br />
       COUNT(DISTINCT city) as unique_cities,<br />
       COUNT(DISTINCT customertype) as unique_customers,<br />
       COUNT(DISTINCT gender) as unique_genders,<br />
       MIN(date) as min_date,<br />
       MAX(date) as max_date<br />
FROM sales;




