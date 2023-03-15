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

### **Data Exploration:**<br /> 
First, I explored the data to understand it's structure and relationships. I used SQL queries to extract basic information such as number of records, unique values, and data types.

SELECT * <br />
FROM sales <br />
LIMIT 5;

| InvoiceID   | Branch| City    | Customertype | Gender | Productline | Unitprice | Quantity | Total  | Date    | Time | Payment | Grossincome | Rating|
| ----------- | ------| ------- | ------------ | ------ | ----------- | --------- | -------- | -----  | ------- | ---- | ------- | ----------- | ------|
| 750-67-8427 | A     | Yangon   | Member       | Female | Health      | 74.69     | 7        | 548.97 | 1/5/2019|13:08 | Ewallet | 26.1415     | 9.1   |
| 226-31-3081 | C     | Naypyitaw| Normal       | Female | Electronics | 15.28     | 5        | 80.22  | 3/8/2019|10:29 | Cash    | 3.82        | 9.6   |
| 631-41-3108 | A     | Yangon   | Normal       | Male   | Home        | 46.33     | 7        | 340.53 | 3/3/2019|13:23 | Credit  | 16.2155     | 7.4   |
| 123-19-1176 | A     | Yangon   | Member       | Male   | Health      | 58.22     | 8        | 489.05 | 1/8/2019|20:33 | Ewallet | 23.288      | 8.4   |
| 373-73-7910 | A     | Yangon   | Member       | Male   | Sports      | 86.31     | 7        | 634.38 | 2/8/2019|10:37 | Ewallet | 30.2085     | 5.3   |

SELECT COUNT(*) as total_records,<br />
       COUNT(DISTINCT city) as unique_cities,<br />
       COUNT(DISTINCT customertype) as unique_customers,<br />
       COUNT(DISTINCT gender) as unique_genders,<br />
       MIN(date) as min_date,<br />
       MAX(date) as max_date<br />
FROM sales;

| total_records | unique_cities | unique_customers | unique_genders | min_date | max_date|
| ------------- | ------------- | ---------------- | -------------- | -------- | ------- |
| 1000          | 3             | 2                | 2              | 1/1/2019 | 3/9/2019|

**Sales Analysis:** <br />
I used SQL queries to analyze the sales data and understand sales trends. For example, I could analyze the sales by city, customer type, gender, and date to identify which factors have the most impact on sales.

**Total sales by city**<br />
SELECT city, SUM(total) as total_sales<br />
FROM sales<br />
GROUP BY city<br />
ORDER BY total_sales DESC;

| City          | Total_sales   | 
| ------------- | ------------- | 
| Naypyitaw     | 110568.7065   |
| Yangon        | 106200.3705   |
| Mandalay      | 106197.672    |
 
**Average sales by customer type and gender**<br />
SELECT customertype, gender, AVG(total) as avg_sales<br />
FROM sales<br />
GROUP BY customertype, gender;

| Customertype  | Gender   | Avg_sales |
| ------------- | -------- | --------- |
| Memeber       | Female   | 337.728   |
| Memeber       | Male     | 316.985   |
| Normal        | Female   | 332.233   |
| Normal        | Male     | 305.048   |
 
**Total sales by date**<br />
SELECT date, SUM(total) as total_sales<br />
FROM sales<br />
GROUP BY date<br />
LIMIT 5;

| Date          | Total_sales   | 
| ------------- | ------------- | 
| 1/1/2019      | 4745.181      |
| 1/10/2019     | 3560.949      |
| 1/11/2019     | 2114.963      |
| 1/12/2019     | 5184.764      |
| 1/13/2019     | 2451.204      |

**Customer Analysis:** <br />
I used SQL queries to analyze customer behavior and preferences. For example, I analyzed the sales by customer type, gender, and rating to understand which factors influence customer behavior.

**Total sales by customer type and gender**<br />
SELECT customertype, gender, SUM(total) as total_sales<br />
FROM sales<br />
GROUP BY customertype, gender;

| Customertype  | Gender   | Total_sales |
| ------------- | -------- | ----------- |
| Memeber       | Female   | 88146.9436  |
| Memeber       | Male     | 76076.5005  |
| Normal        | Female   | 79735.9815  |
| Normal        | Male     | 79007.3235  |

**Average rating by customer type and gender**<br />
SELECT customertype, gender, AVG(rating) as avg_rating<br />
FROM sales<br />
GROUP BY customertype, gender;

| Customertype  | Gender   | Avg_rating  |
| ------------- | -------- | ----------- |
| Memeber       | Female   | 6.94        |
| Memeber       | Male     | 6.94        |
| Normal        | Female   | 6.99        |
| Normal        | Male     | 7.02        |

**Gross Income Analysis:** <br />
I used SQL queries to analyze the gross income from sales. For example, I can analyze the gross income by date, payment method, and customer type to understand which factors have the most impact on gross income.

**Total gross income by date**<br />
SELECT date, SUM(grossincome) as total_gross_income<br />
FROM sales<br />
GROUP BY date<br />
LIMIT 5;

| Date          | Total_gross_income | 
| ------------- | ------------------ | 
| 1/1/2019      | 225.961            |
| 1/10/2019     | 169.569            |
| 1/11/2019     | 100.712            |
| 1/12/2019     | 246.894            |
| 1/13/2019     | 116.724            |

**Total gross income by payment method**<br />
SELECT payment, SUM(grossincome) as total_gross_income<br />
FROM sales<br />
GROUP BY payment;

| Payment     | total_gross_income | 
| ----------- | ------------------ | 
| Cash        | 5343.17            | 
| Credit Card | 4798.43            | 
| Ewallet     | 5237.77            | 

**Total gross income by customer type**<br />
SELECT customertype, SUM(grossincome) as total_gross_income<br />
FROM sales<br />
GROUP BY customertype;

| Customertype | total_gross_income | 
| ------------ | ------------------ | 
| Member       | 7820.164           | 
| Normal       | 7559.205           | 

Overall, this project aims to showcase my SQL skills and ability to analyze and interpret data. I could use these queries to create interactive dashboards or visualizations to present my findings.

[Queries used](https://github.com/NickZward/Personal-Projects/blob/main/Supermarket%20Sales/Queries.txt)


