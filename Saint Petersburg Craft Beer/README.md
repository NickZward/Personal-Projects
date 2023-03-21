# Project 3: Saint Petersburg Craft Beer:
![beers_0](https://user-images.githubusercontent.com/29818091/226423880-d7068268-8707-4f1a-b40b-6001bf183ab7.jpg)

This project aims to analyze data related to different beers served in Saint Petersburg, Russia. By analyzing this data the following points could be achieved.

1	Understanding beer preferences: Analyzing the dataset can help identify popular beer types, brands, and breweries. This information can be useful for breweries to understand customer preferences and develop new products.<br />
2	Optimizing beer distribution: Knowing the location of popular bars can help breweries optimize their distribution network and ensure their products are available at the right places.<br />
3	Identifying trends: By analyzing the ratings of different beers, breweries can identify trends and adjust their products accordingly. For instance, if there is a trend towards hoppy beers, breweries can create more of these to meet the demand.<br />
4	Marketing and advertising: By analyzing the dataset, breweries can identify popular bars and locations and target their marketing and advertising efforts towards those areas.<br />
5	Improving customer experience: Understanding customer preferences can help breweries improve their product offerings and provide a better customer experience. For example, if customers prefer lighter beers, breweries can offer more of these options.<br />
6	Identifying opportunities for growth: Analyzing the dataset can help breweries identify gaps in the market and areas where they can expand their offerings. For instance, if there are no popular breweries in a particular location, a brewery can consider opening a new location in that area.<br />

In summary, exploring this dataset can provide valuable insights for breweries and help them make data-driven decisions to improve their products, distribution, and overall performance.

## About the dataset:
Data was obtained from untappd, popular social network for beer geeks.

|Column Name                   |Description                                                                  |
|----------------------------- |---------------------------------------------------------------------------- |
|Username                      |Depersonalized users nickname                                                |
|Beer                          |Name of the beer                                                             |
|Brewery                       |Name of the brewery which brew the beer                                      |
|Rating                        |User rating of the beer in 0-5 scale                                         |
|Bar                           |Name of the bar in which beer was purchased                                  |
|Checkin Text                  |Text added by user for his check-in                                          |
|Serving                       |Type of serving in which beer was received (Draft, Bottle, etc.)             |
|Date                          |Date of check-in in YYYY-MM-DD HH-MM-SS format, timezone is GMT+3            |
|Beer Link                     |Link to the beer profile in social network                                   |
|Brewery Link                  |Link to the brewery profile in social network                                |
|Bar Link                      |Link to the bar profile in social network                                    |
|Bar Adress                    |Address of bar                                                               |
|Latitude                      |Bar location latitude (geometric center of object from google geocoding api) |
|Longitude                     |Bar location longitude (geometric center of object by google geocoding api)  |

[Data Used](https://www.kaggle.com/datasets/kondrasso/saint-petersburg-craft-beer?resource=download)

## Step 1: Data Exploration
Before starting with the analysis, it's important to understand the data. We can start by running some basic SQL queries to explore the data.

Count the total number of different beers in the database:
```
SELECT COUNT (DISTINCT beer)
FROM beer;
```
Find the total number of breweries in the database:
```
SELECT COUNT(DISTINCT brewery)  
FROM beer;
```
Find the total number of bars in the database:
```
SELECT COUNT(DISTINCT bar)  
FROM beer;
```
Find the highest rated beer in the database:
```
SELECT beer, AVG(rating) AS avg_rating 
FROM beer 
GROUP BY beer 
ORDER BY avg_rating DESC;
```
Find the lowest rated beer in the database:
```
SELECT beer, AVG(rating) AS avg_rating 
FROM beer 
GROUP BY beer 
ORDER BY avg_rating ASC;
```
## Step 2: Data Analysis
After exploring the data, we can start analyzing it to find some insights:

Find the average rating for each beer:
```
SELECT beer, AVG(rating) AS avg_rating 
FROM beer 
GROUP BY beer 
ORDER BY avg_rating DESC;
```
Find the top-rated beers for each brewery:
```
SELECT brewery, beer, AVG(rating) AS avg_rating
FROM beer 
GROUP BY brewery
ORDER BY avg_rating DESC;
```
Find the top-rated beers for each bar:
```
SELECT bar, beer, AVG(rating) AS avg_rating
FROM beer 
GROUP BY bar
ORDER BY avg_rating DESC;
 ```
Find the number of check-ins for each month:
```
SELECT strftime('%Y-%m', date) AS month, COUNT(*) AS total_checkins 
FROM beer 
GROUP BY month 
ORDER BY month;
```

## Step 3: Data Visualization

Create a bar chart showing the total number of check-ins for each month.
Create a heatmap showing the density of check-ins across the city.
Create a bubble map showing where the beers with an average rating of 5 are served.
