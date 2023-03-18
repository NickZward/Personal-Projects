# Project 2: Restaurants Tallinn:
![tallinn](https://user-images.githubusercontent.com/29818091/225739169-8c30b52a-8174-4586-958b-31764191e66f.jpeg)

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
```
ALTER TABLE restaurant_tallinn RENAME COLUMN Restaraunt TO Restaurant;
```
## Step 2: Looking for insights:
SQL is a powerful tool for data analysis that offers scalability, speed, flexibility, reproducibility, and visualization capabilities. By using SQL to analyze large datasets, it is possible to generate valuable insights that can inform decision-making and drive business growth.

The first insight I analyzed was looking for specific cuisine offered in Tallinn. In the SQL query below I looked specifically for Italian restaurants. The kind of cuisine can easily be changed by modifying the SQL query below.
```
SELECT restaurant, cuisine
FROM restaurant_tallinn
WHERE cuisine LIKE '%italian%';
```
| Restaurant              | Cuisine|
| ----------------------- | -------|
| IO restaurant           | italian|
| La Prima Pizza Vanalinn | italian|
| Gianni                  | italian|

Another useful insight could be looking for specific attributes of a restaurant. For example if I would go out for dinner with someone in a wheelchair I would like te see which restaurants are accissible for people in wheelchairs. The two queries down below show how this could be achieved.
```
SELECT restaurant, cuisine, additional
FROM restaurant_tallinn
WHERE additional LIKE '%wheelchair%';
```
| Restaurant              | Cuisine                   | Additional                                   |
| ----------------------- | ------------------------- | -------------------------------------------- |
| Al Mare Grill           | grill, european, american | wifi, internet, wheelchair access, catering  |
| Allee                   | international             | wifi, internet, wheelchair access, breakfast |
| Argentiina (Lootsi 8)   | argentinian               | wifi, internet, wheelchair access, lounge    |
| Charlies Corner         | international             | wifi, internet, wheelchair access, breakfast |
| GC Gastrobar            | european, scandinavian    | wifi, internet, wheelchair access, live music|
```
SELECT restaurant, cuisine, additional
FROM restaurant_tallinn
WHERE additional LIKE '%sea view%' OR '%live music%';
```
| Restaurant               | Cuisine                   | Additional                                                            |
| -----------------------  | ------------------------- | ----------------------------------------------------------------------|
| Al Mare Grill            | grill, european, american | wifi, internet, wheelchair access, catering, live music, sea view     |
| Riviera Palais Brasserie | international             | wifi, internet, accessible toilet, sea view, live music, private room |
| Sardiinid                | argentinian               | wifi, internet, sea view, lounge, live music, business meetings       |

A second useful insight could be looking for the average bill in case you want to spent a lot of money or not so much money. This could be achieved by using the queries down below.

**Select all restaurants with an average bill greater than 15**<br />
```
SELECT restaurant, cuisine, avg_bill
FROM restaurant_tallinn
WHERE avg_bill > 15;
```
| Restaurant               | Cuisine                        | Avg_Bill  |
| ------------------------ | ------------------------------ | --------- |
| Argentiina (Parnu mnt.37 | argentinian                    | 18        |
| Dominic                  | european, estonian             | 18        |
| Leib                     | dedicated to estonian produce  | 18        |
| MEAT Resto & Butchery    | steak house                    | 18        |
| Olde Hansa               | medieval                       | 18        |

**Select all restaurants with an average bill between 5 and 15**<br />
```
SELECT restaurant, cuisine, avg_bill
FROM restaurant_tallinn
WHERE avg_bill BETWEEN 5 AND  15;
```
| Restaurant               | Cuisine                        | Avg_Bill  |
| ------------------------ | ------------------------------ | --------- |
| Hans                     | chinese, sichuan               | 12        |
| IO restaurant            | italian                        | 15        |
| Kalevi Jahtklubi Resto   | mediterranean                  | 12        |
| Kivi Paber Kaarid        | fusion                         | 12        |
| KARBES Kitchen & Bar     | nordic                         | 12        |

**Which are the top 10 restaurants with the highest average bill amount/**<br />
```
SELECT Restaurant, AVG_bill
FROM restaurant_tallinn
ORDER BY AVG_bill DESC
LIMIT 10;
```
| Restaurant               | Avg_Bill  |
| ------------------------ | --------- |
| Argentiina (Parnu mnt.37 | 18        |
| Dominic                  | 18        |
| Leib                     | 18        |
| MEAT Resto & butchery    | 18        |
| Olde Hansa               | 18        |
| Troika                   | 18        |
| Gianni                   | 18        |
| SOE                      | 18        |
| GC Gastrobar             | 15        |
| Goodwin The Steak House  | 15        |

You can also gain some useful insights looking at the ratings. The queries down below will show some examples on queries you could use to gain some insights looking at the ratings of a restaurant. There are three kind of ratings. Food, Service and Atmosphere.

**Select the top 5 highest rated restaurants based on the average of their food, service, and atmosphere ratings**<br />
```
SELECT restaurant, food, service, atmosphere,
    (food + service + atmosphere)/3 as rating_avg
FROM restaurant_tallinn
ORDER BY rating_avg DESC
LIMIT 5;
```
| Restaurant               | Food  | Service | Atmosphere | rating_avg |
| ------------------------ | ----- | ------- | ---------- | ---------- |
| Rae                      | 5.0   | 5.0     | 4.8        | 4.93       |
| La Prima Pizza Vanalinn  | 4.7   | 5.0     | 5.0        | 4.9        |
| MOON                     | 4.9   | 4.9     | 4.8        | 4.86       |
| Rukis                    | 4.6   | 5.0     | 5.0        | 4.86       |
| Chapters Boutique Cafe   | 4.7   | 4.9     | 4.9        | 4.83       |
```
SELECT cuisine, AVG((food + atmosphere + service) / 3) AS avg_overall_rating
FROM restaurant_tallinn
GROUP BY cuisine
ORDER BY avg_overall_rating DESC;
```
| Cuisine                  | rating_avg |
| ------------------------ | ---------- |
| fusion, european         | 4.83       | 
| european, scandinavian   | 4.8        |
| european, estonian       | 4.8        | 
| thai, indian             | 4.73       |
| italian                  | 4.72       |

**Which are the top 5 cuisines with the highest average rating for food?**<br />
```
SELECT cuisine, AVG(food) AS avg_food_rating
FROM restaurant_tallinn
GROUP BY cuisine
ORDER BY avg_food_rating DESC
LIMIT 5;
```
| Cuisine                  | avg_food_rating |
| ------------------------ | --------------- |
| european, scandinavian   | 4.9             | 
| american, european       | 4.9             |
| european, estonian       | 4.8             |  
| world                    | 4.7             |
| thai, indian             | 4.7             |

**Which are the top 5 restaurants with the highest average rating for atmosphere?**<br />
```
SELECT restaurant, AVG(atmosphere) AS avg_atmosphere_rating
FROM restaurant_tallinn
GROUP BY restaurant
ORDER BY avg_atmosphere_rating DESC
LIMIT 5;
```
| Restaurant                  | avg_atmosphere_rating |
| --------------------------- | --------------------- |
| St.Patricks Foorum          | 5.0                   | 
| Rukis                       | 5.0                   |
| La Prima Pizza Vanalinn     | 5.0                   |  
| Riviera Palais Brasserie    | 5.0                   |
| Olde Hansa                  | 4.9                   |

**Which are the top restaurants with the highest overall rating per specific cuisine?**<br />
```
SELECT cuisine, restaurant, (food + atmosphere + service) / 3 AS avg_overall_rating
FROM restaurant_tallinn
WHERE (cuisine, (food + atmosphere + service) / 3) IN 
    SELECT cuisine, MAX((food + atmosphere + service) / 3) AS max_overall_rating
    FROM restaurant_tallinn
    GROUP BY cuisine
)
ORDER BY cuisine, avg_overall_rating DESC;
```
| Cuisine                     | Restaurant              | avg_overall_rating |
| --------------------------- | ----------------------- | ------------------ |
| american, european          | SUSI Grill & Chill      | 4.7                |
| american                    | Goodwin The Steak House | 4.43               |
| estonian                    | Rukis                   | 4.86               |
| french                      | Riviera Palais Brasserie| 4.7                |
| greek                       | Oia                     | 4.53               |
| russian                     | MOON                    | 4.86               |

In the end I made a distribution of the average ratings to see what the avarage is across all these different rating.

**What is the distribution of ratings for food, service, and atmosphere?**<br />
```
SELECT 
  ROUND(AVG(food), 1) AS avg_food_rating, 
  ROUND(AVG(service), 1) AS avg_service_rating,
  ROUND(AVG(atmosphere), 1) AS avg_atmosphere_rating 
FROM restaurant_tallinn;
```
| avg_food_rating             | avg_service_rating      | avg_atmosphere_rating |
| --------------------------- | ----------------------- | --------------------- |
| 4.0                         | 3.9                     | 4.0                   |

[Queries used](https://github.com/NickZward/Personal-Projects/blob/main/Restaurants%20Tallinn/Queries.txt)

## Step 3: Visualizing the data:
I decided to visualize some of my findings since the data contained latitude and lonitude data. Visualizing some data can give some other perspectives in contrary to just a table. The first data I wanted to visualize were the restaurants serving estonian and european cuisine. Showing this on a map can help to make the search process easier, faster, and more engaging for users. It provides a visual representation of the location of each restaurant. I made this visualization using Google Looker Studio.

In order to make this work I had to concatenate the latitude and longitude data first. I did this using the query below.<br />
```
SELECT restaurant, cuisine, latitude ||','||longitude as geo_location
FROM restaurant_tallinn
WHERE cuisine LIKE '%estonian%' OR cuisine LIKE '%european%';
```
This is how the visualization turned out. If you open the visualization through the link provided below, you get taken to an interactive version of it.

<img width="905" alt="Estonian   European cuisine" src="https://user-images.githubusercontent.com/29818091/225737773-7191084d-8039-4805-8914-d5fc9524e313.png">

[Link to the visual](https://lookerstudio.google.com/s/n6p9O5GgmM0)

Secondly I wanted to see where the restaurants were located who served the best rated food according to the data. Like before I had to concatenate the latitude and longitude first. I used this query to pull the relevant data out of the database.
```
SELECT restaurant,  food, latitude||','||longitude as geo_location
FROM restaurant_tallinn
ORDER BY food DESC
LIMIT 15;
```
[Link to the visual]

Lastly I wanted to see where the restaurants were located who were the most expensive according to the data. Like before I had to concatenate the latitude and longitude first. I used this query to pull the relevant data out of the database.

[Link to the visual]









