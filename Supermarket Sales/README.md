# Project 1: Supermarket sales:

The objective of this project is to analyze the data of a supermarket's sales to obtain insights into sales trends and customer behavior by utilizing SQL (Structured Query Language). SQL is an effective tool for managing and querying large datasets, which makes it a suitable method for analyzing data.

The analysis process involves extracting the appropriate data from the supermarket sales CSV file and using queries to identify key metrics like sales volume, revenue, and customer demographics. Then, SQL queries and aggregation functions are used to determine trends over time, detect patterns in customer behavior, and understand the factors that influence sales.

Using SQL facilitates efficient querying and analysis of large datasets, which is essential for obtaining meaningful insights into sales trends and customer behavior. Additionally, employing SQL makes it easy to replicate the analysis, making it a valuable tool for businesses of all sizes.

The project will be documented in a clear and concise manner, with detailed explanations of the SQL queries used and the insights obtained. This will enable the easy replication of the analysis and help others understand the value of using SQL for sales data analysis.

## About the dataset:
The growth of supermarkets in most populated cities are increasing and market competitions are also high. The dataset is one of the historical sales of a supermarket company which has recorded in 3 different branches for 3 months data.

|Column Name                | Description                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------------------- |
|Invoice id                 |Computer generated sales slip invoice identification number                                                    |
|Branch                     | Branch of supercenter (3 branches are available identified by A, B and C)                                     |
|City                       | Location of supercenters                                                                                      |
|Customer type              | Type of customers, recorded by Members for customers using member card and Normal for without member card     |
|Gender                     | Gender type of customer                                                                                       |
|Product line               | General item categorization groups                                                                            |
|Unit price                 | Price of each product in $                                                                                    |
|Quantity                   | Number of products purchased by customer                                                                      |
|Tax                        | 5% tax fee for customer buying                                                                                |
|Total                      | Total price including tax                                                                                     |
|Date                       | Date of purchase (Record available from January 2019 to March 2019)                                           |
|Time                       | Purchase time (10am to 9pm)                                                                                   |
|Payment                    | Payment used by customer for purchase (3 methods are available – Cash, Credit card and Ewallet)               |
|COGS                       | Cost of goods sold                                                                                            |
|Gross margin percentage    | Gross margin percentage                                                                                       |
|Gross income               | Gross income                                                                                                  |
|Rating                     | Customer stratification rating on their overall shopping experience (On a scale of 1 to 10)                   |

[Data Used](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales)

## Objective: Analyzing the sales data to understand sales trends and customer behavior!
Understanding sales trends and customer behavior by analyzing sales data can provide businesses with valuable insights to improve their sales performance, inventory management, pricing strategies, and identify opportunities for growth. By analyzing data, businesses can optimize their marketing strategies, forecast demand, plan inventory, and identify the most effective pricing points for different products. In short, analyzing sales data can help businesses make data-driven decisions that can improve their overall profitability and success.

### **Data Exploration:**<br /> 
When analyzing a dataset, it's important to first explore the data to understand its structure and relationships. This is typically done by using SQL queries to extract basic information such as the number of records, unique values, and data types.

For example, the number of records will give you an idea of how much data you're dealing with, while the unique values can help you identify any potential issues or anomalies in the data. The data types will help you understand the nature of the data, such as whether it's numerical or categorical, and whether any transformations may be needed to use it effectively.

By exploring the data in this way, you can get a better understanding of the dataset and identify any issues or patterns that may need further 
investigation. It can also help you determine the best methods to use when analyzing the data to extract meaningful insights.

```
SELECT * 
FROM sales 
LIMIT 5;
```

| InvoiceID   | Branch| City    | Customertype | Gender | Productline | Unitprice | Quantity | Total  | Date    | Time | Payment | Grossincome | Rating|
| ----------- | ------| ------- | ------------ | ------ | ----------- | --------- | -------- | -----  | ------- | ---- | ------- | ----------- | ------|
| 750-67-8427 | A     | Yangon   | Member       | Female | Health      | 74.69     | 7        | 548.97 | 1/5/2019|13:08 | Ewallet | 26.1415     | 9.1   |
| 226-31-3081 | C     | Naypyitaw| Normal       | Female | Electronics | 15.28     | 5        | 80.22  | 3/8/2019|10:29 | Cash    | 3.82        | 9.6   |
| 631-41-3108 | A     | Yangon   | Normal       | Male   | Home        | 46.33     | 7        | 340.53 | 3/3/2019|13:23 | Credit  | 16.2155     | 7.4   |
| 123-19-1176 | A     | Yangon   | Member       | Male   | Health      | 58.22     | 8        | 489.05 | 1/8/2019|20:33 | Ewallet | 23.288      | 8.4   |
| 373-73-7910 | A     | Yangon   | Member       | Male   | Sports      | 86.31     | 7        | 634.38 | 2/8/2019|10:37 | Ewallet | 30.2085     | 5.3   |
```
SELECT COUNT(*) as total_records,
       COUNT(DISTINCT city) as unique_cities,
       COUNT(DISTINCT customertype) as unique_customers,
       COUNT(DISTINCT gender) as unique_genders,
       MIN(date) as min_date,
       MAX(date) as max_date
FROM sales;
```
| total_records | unique_cities | unique_customers | unique_genders | min_date | max_date|
| ------------- | ------------- | ---------------- | -------------- | -------- | ------- |
| 1000          | 3             | 2                | 2              | 1/1/2019 | 3/9/2019|

### **Sales Analysis:** <br />
When analyzing sales data using SQL, there are a number of different queries and functions that can be used to gain insights into sales trends and customer behavior.

One approach is to analyze the sales data by various factors such as city, customer type, gender, and date to identify which factors have the most impact on sales.

**Total sales by city**<br />
```
SELECT city, SUM(total) as total_sales
FROM sales
GROUP BY city
ORDER BY total_sales DESC;
```
| City          | Total_sales   | 
| ------------- | ------------- | 
| Naypyitaw     | 110568.7065   |
| Yangon        | 106200.3705   |
| Mandalay      | 106197.672    |
 
**Average sales by customer type and gender**<br />
```
SELECT customertype, gender, AVG(total) as avg_sales
FROM sales
GROUP BY customertype, gender;
```
| Customertype  | Gender   | Avg_sales |
| ------------- | -------- | --------- |
| Memeber       | Female   | 337.728   |
| Memeber       | Male     | 316.985   |
| Normal        | Female   | 332.233   |
| Normal        | Male     | 305.048   |
 
**Total sales by date**<br />
```
SELECT date, SUM(total) as total_sales
FROM sales
GROUP BY date
LIMIT 5;
```
| Date          | Total_sales   | 
| ------------- | ------------- | 
| 1/1/2019      | 4745.181      |
| 1/10/2019     | 3560.949      |
| 1/11/2019     | 2114.963      |
| 1/12/2019     | 5184.764      |
| 1/13/2019     | 2451.204      |

### **Customer Analysis:** <br />
When analyzing customer behavior and preferences using SQL, there are various queries and functions that can be used to gain insights.

One approach is to analyze the sales data by different customer attributes such as customer type, gender, and rating. This can help identify which factors have the most influence on customer behavior and preferences.

**Total sales by customer type and gender**<br />
```
SELECT customertype, gender, SUM(total) as total_sales
FROM sales
GROUP BY customertype, gender;
```
| Customertype  | Gender   | Total_sales |
| ------------- | -------- | ----------- |
| Memeber       | Female   | 88146.9436  |
| Memeber       | Male     | 76076.5005  |
| Normal        | Female   | 79735.9815  |
| Normal        | Male     | 79007.3235  |

**Average rating by customer type and gender**<br />
```
SELECT customertype, gender, AVG(rating) as avg_rating
FROM sales
GROUP BY customertype, gender;
```
| Customertype  | Gender   | Avg_rating  |
| ------------- | -------- | ----------- |
| Memeber       | Female   | 6.94        |
| Memeber       | Male     | 6.94        |
| Normal        | Female   | 6.99        |
| Normal        | Male     | 7.02        |

### **Gross Income Analysis:** <br />
When analyzing gross income from sales using SQL, there are various queries and functions that can be used to gain insights.

One approach is to analyze the gross income by different factors such as date, payment method, and customer type. This can help identify which factors have the most impact on gross income.

**Total gross income by date**<br />
```
SELECT date, SUM(grossincome) as total_gross_income
FROM sales
GROUP BY date
LIMIT 5;
```
| Date          | Total_gross_income | 
| ------------- | ------------------ | 
| 1/1/2019      | 225.961            |
| 1/10/2019     | 169.569            |
| 1/11/2019     | 100.712            |
| 1/12/2019     | 246.894            |
| 1/13/2019     | 116.724            |

**Total gross income by payment method**<br />
```
SELECT payment, SUM(grossincome) as total_gross_income
FROM sales
GROUP BY payment;
```
| Payment     | total_gross_income | 
| ----------- | ------------------ | 
| Cash        | 5343.17            | 
| Credit Card | 4798.43            | 
| Ewallet     | 5237.77            | 

**Total gross income by customer type**<br />
```
SELECT customertype, SUM(grossincome) as total_gross_income
FROM sales
GROUP BY customertype;
```
| Customertype | total_gross_income | 
| ------------ | ------------------ | 
| Member       | 7820.164           | 
| Normal       | 7559.205           | 

In summary, this project showcases my proficiency in SQL and my ability to use it as a powerful tool to analyze data and gain valuable insights.

[Queries used](https://github.com/NickZward/Personal-Projects/blob/main/Supermarket%20Sales/Queries.txt)
