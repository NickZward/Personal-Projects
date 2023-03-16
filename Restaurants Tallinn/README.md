# Project 2: Restaurants Tallinn:

The project aims to analyze data related to restaurants in Tallinn, Estonia. The dataset includes several columns such as Restaurant name, Address, 
Cuisine type, Average bill, Atmosphere, Food quality, Service rating, and Geographical coordinates (latitude and longitude).

The analysis will focus on exploring various aspects of the restaurant industry in Tallinn, such as popular cuisine types, average bills, 
customer satisfaction ratings, and more. The data will be extracted, transformed, and loaded into the relational database management system called MySQL.

The project will involve several steps such as cleaning the data, creating tables, running queries, and visualizing the results using tools 
such as Tableau or Power BI. The final report will present insights and recommendations based on the analysis, which can help restaurant owners, 
food enthusiasts, and tourists make informed decisions.

## About the dataset:
|Column Name                   |Description                                   |
|----------------------------- |--------------------------------------------- |
|Restaurant                    |Restaurant name is displayed here             |
|Details URL                   |This is the URLfrom which data is aquired     |
|Address                       |Address of the restaurant                     |
|Cuisine                       |Comma list of types of cuisine served         |
|Avg_Bill                      |Average bill (float), estimated               |
|Additional                    |List of properties that the venue has         |
|Atmosphere                    |Atmosphere rating 1-5, float                  |
|Food                          |Food rating 1-5, float                        |
|Service                       |Service rating 1-5, float                     |
|Latitude                      |Latitude of venue                             |
|Longitude                     |Longitude of venue                            |

[Data Used](https://www.kaggle.com/datasets/ilyasmelyanskiy/tallinn-restaurants)

## Step 1: Cleaning the data:

cleaning data columns in SQL is an important step in ensuring that the data is accurate, complete, consistent, and ready for analysis. It helps to improve the quality of data and the accuracy of the insights that can be derived from it. Luckily the data was already quite clean in this dataset. All I had to do was was changing a column name because it was containing a spelling mistake. I did this using the following query:

ALTER TABLE restaurant_tallinn RENAME COLUMN Restaraunt TO Restaurant;

## Step 2: Looking for insights:
SQL is a powerful tool for data analysis that offers scalability, speed, flexibility, reproducibility, and visualization capabilities. By using SQL to analyze large datasets, it is possible to generate valuable insights that can inform decision-making and drive business growth.

The first insight I analyzed was looking for specific cuisine offered in Tallinn. In the SQL query below I looked specifically for Italian restaurants. The kind of cuisine can easily be changed by modifying the SQL query below.

SELECT restaurant, cuisine
FROM restaurant_tallinn
WHERE cuisine LIKE '%italian%';



