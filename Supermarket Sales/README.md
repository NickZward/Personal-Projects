# Project 1: Supermarket sales.

This project aims to analyze supermarket sales data to gain insights into sales trends and customer behavior using SQL. SQL (Structured Query Language) is a powerful tool for managing and querying large datasets, making it an ideal method for analyzing data.

The analysis will involve extracting the relevant data from the supermarket sales CSV file, and querying it to identify key metrics such as sales volume, revenue, and customer demographics. We will then use SQL queries and aggregation functions to identify trends over time, identify patterns in customer behavior, and understand the factors that influence sales.

By using SQL, we can efficiently query and analyze large datasets, which is essential for gaining meaningful insights into sales trends and customer behavior. Additionally, using SQL allows for easy replication of the analysis, making it a valuable tool for businesses of all sizes.

The project will be documented in a clear and concise manner, with detailed explanations of the SQL queries used and the insights gained. This will allow for easy replication of the analysis and help others to understand the value of using SQL for analyzing sales data.

## About the dataset
The growth of supermarkets in most populated cities are increasing and market competitions are also high. The dataset is one of the historical sales of a supermarket company which has recorded in 3 different branches for 3 months data.

**Attribute information**<br />
Invoice id: Computer generated sales slip invoice identification number<br />
Branch: Branch of supercenter (3 branches are available identified by A, B and C)<br />
City: Location of supercenters<br />
Customer type: Type of customers, recorded by Members for customers using member card and Normal for without member card<br />
Gender: Gender type of customer<br />
Product line: General item categorization groups - Electronic accessories, Fashion accessories, Food and beverages, Health and beauty, Home and lifestyle, Sports and travel<br />
Unit price: Price of each product in $<br />
Quantity: Number of products purchased by customer<br />
Tax: 5% tax fee for customer buying<br />
Total: Total price including tax<br />
Date: Date of purchase (Record available from January 2019 to March 2019)<br />
Time: Purchase time (10am to 9pm)<br />
Payment: Payment used by customer for purchase (3 methods are available – Cash, Credit card and Ewallet)<br />
COGS: Cost of goods sold<br />
Gross margin percentage: Gross margin percentage<br />
Gross income: Gross income<br />
Rating: Customer stratification rating on their overall shopping experience (On a scale of 1 to 10)<br />

[Data Used](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales)

## Objective: Analyzing the sales data to understand sales trends and customer behavior!

**Data Exploration:** First, explore the data to understand its structure and relationships. Use SQL queries to extract basic information such as number of records, unique values, and data types.

SELECT * <br />
FROM sales <br />
LIMIT 5;

| InvoiceID | Branch | City | Customertype | Gender | Productline | Unitprice | Quantity | Total | Date | Time | Payment | Grossincome | Rating |
| --------- | ------ | ---- | ------------ | ------ | ----------- | --------- | -------- | ----- | ---- | ---- | ------- | ----------- | ------ |

SELECT COUNT(*) as total_records,<br />
       COUNT(DISTINCT city) as unique_cities,<br />
       COUNT(DISTINCT customertype) as unique_customers,<br />
       COUNT(DISTINCT gender) as unique_genders,<br />
       MIN(date) as min_date,<br />
       MAX(date) as max_date<br />
FROM sales;

[Queries used](https://github.com/NickZward/Personal-Projects/blob/main/Supermarket%20Sales/Queries.txt)




