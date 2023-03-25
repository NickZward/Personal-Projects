# Project 4: The Pizza Project:
As a data analyst, I was approached by a client named Ben who is planning to start a new pizza delivery and take-out restaurant in his town. He requested me to design and build a relational database that will enable him to store and manage all the critical data related to his business operations. The objective of the project is to help Ben monitor the performance of his business through insightful dashboards. The key areas of focus for the database are orders, stock control, and staff management. The database will serve as a valuable tool for Ben to make data-driven decisions and ensure the success of his business.

As part of the project, I went beyond just writing queries and extracting data. I also created three different dashboards using Google Looker, which allowed me to visualize and present data in a user-friendly way.

The different tables and the relationship between them have been drawn using QuickDBD. After connecting all the tables, the relational SQL database will look like this:

![Screenshot 2023-03-22 at 5 01 32 PM](https://user-images.githubusercontent.com/29818091/226965890-71248a15-746f-4247-baf7-a951c90cbf98.png)

## Order Activity:
The first dashboard focused on order activity, providing valuable insights into sales trends, top-selling items, and customer preferences. In order to extract the information needed for this dashboard I used this query:

```
SELECT
	o.order_id,
	i.item_prize,
	o.quantity,
	i.item_cat,
	i.item_name,
	o.created_at,
	a.delivery_address1,
	a.delivery_address2,
	a.delivery_city,
	a.delivery_zipcode,
	o.delivery 
FROM
	orders o
	LEFT JOIN item i ON o.item_id = i.item_id
	LEFT JOIN address a ON o.add_id = a.add_id
  ```
|order_id|item_prize|quantity|item_cat|item_name                   |created_at|deliveryaddress1 |deliveryaddress2|delivery_city|delivery_zipcode|delivery|
|--------|----------|--------|--------|----------------------------|----------|-----------------|----------------|-------------|----------------|--------|
|109	   |12	      |2	     |Pizza	  |Pizza Margherita Reg	       |10/08/2022|	607 Trails Road |NULL            |Manchester   |6042	          |1       |
|110	   |16	      |1	     |Pizza	  |Pizza Diavola (hot) Reg     |10/08/2022|	25 Cliffside	  |NULL            |Manchester	 |6042	          |1       |
|111	   |12	      |1	     |Pizza	  |Pizza Margherita Reg	       |10/08/2022|	56 Concord Road |NULL            |Manchester	 |6042	          |1       |
|111	   |16	      |1	     |Pizza	  |Pizza Diavola (hot) Reg     |10/08/2022|	56 Concord Road |NULL            |Manchester	 |6042	          |1       |
|112	   |19	      |3	     |Pizza	  |Pizza Quattro Formaggi Large|10/08/2022|	82 Lookout Drive|NULL            |Manchester	 |6040	          |0       |

![Screenshot 2023-03-24 at 10 51 15 PM](https://user-images.githubusercontent.com/29818091/227715330-41088c54-cad8-4b54-a46c-e4cf2d259f34.png)

## Inventory Management:
The second dashboard was more complex, involving inventory management, where I needed to calculate inventory usage and identify which items needed reordering. I also calculated the cost of each pizza based on the cost of ingredients, enabling me to monitor pricing and profits. I added some extra conditional formatting to see which items are in need of some restocking. In order to extract the information needed for this dashboard I used this query: 

```
SELECT
	s1.item_name AS item_name,
	s1.ing_name AS ing_name,
	s1.ing_id AS ing_id,
	s1.ing_weight AS ing_weight,
	s1.ing_price AS ing_price,
	s1.order_quantity AS order_quantity,
	s1.recipe_quantity AS recipe_quantity,(
		s1.order_quantity * s1.recipe_quantity 
		) AS ordered_weight,(
		s1.ing_price / s1.ing_weight 
		) AS unit_cost,((
			s1.order_quantity * s1.recipe_quantity 
		) * ( s1.ing_price / s1.ing_weight )) AS ingredient_cost 
FROM
	(
	SELECT
		o.item_id AS item_id,
		i.sku AS sku,
		i.item_name AS item_name,
		r.ing_id AS ing_id,
		ing.ing_name AS ing_name,
		ing.ing_weight AS ing_weight,
		ing.ing_price AS ing_price,
		sum( o.quantity ) AS order_quantity,
		r.quantity AS recipe_quantity 
	FROM
		(((
					orders o
					LEFT JOIN item i ON ((
							o.item_id = i.item_id 
						)))
				LEFT JOIN recipe r ON ((
						i.sku = r.recipe_id 
					)))
			LEFT JOIN ingredient ing ON ((
					ing.ing_id = r.ing_id 
				))) 
	GROUP BY
		o.item_id,
		i.sku,
		i.item_name,
		r.ing_id,
		r.quantity,
		ing.ing_weight,
	ing.ing_price 
	) s1

SELECT
s2.ing_name,
s2.ordered_weight,
ing.ing_weight,
inv.quantity,
ing.ing_weight * inv.quantity AS total_inv_weight 
FROM
	( SELECT ing_id, ing_name, sum( ordered_weight ) AS ordered_weight FROM stock1 GROUP BY ing_name, ing_id ) s2
	LEFT JOIN inventory inv ON inv.item_id = s2.ing_id
	LEFT JOIN ingredient ing ON ing.ing_id = s2.ing_id
```
|ing_name       |ordered_weight|ing_weight|quantity|total_inv_weight|
|---------------|--------------|----------|--------|----------------|
|Anchovies	|1850	       |1000	  |2	   |2000            |
|Banoffee pie	|4200	       |1200	  |2	   |2400            |
|Caesar dressing|740	       |3800	  |5	   |19000           |
|Calamari       |1250	       |2500	  |3	   |7500            |
|Capers	        |133	       |1000	  |2	   |2000            |

![Screenshot 2023-03-24 at 10 51 26 PM](https://user-images.githubusercontent.com/29818091/227715401-f3351551-292e-4ffe-bc29-de67b35c263d.png) 

## Staff:
The third and final dashboard was relatively simple, focusing on staff management and costs. I also added a slider where the user van adjust the date and see which employee is available at any chosen week. In order to extract the information needed for this dashboard I used this query: 

```
SELECT
	r.date,
	s.first_name,
	s.last_name,
	s.hourly_rate,
	sh.start_time,
	sh.end_time,
	CAST((strftime('%s', sh.end_time) - strftime('%s', sh.start_time)) / 3600.0 AS REAL) AS hours_in_shift,
	CAST((strftime('%s', sh.end_time) - strftime('%s', sh.start_time)) / 3600.0 AS REAL) * s.hourly_rate AS staff_cost 
FROM
	rota r
	LEFT JOIN staff s ON r.staff_id = s.staff_id
	LEFT JOIN shift sh ON r.shift_id = sh.shift_id;
```
|date     |first_name|last_name|hourly_rate|start_time|end_time|hours_in_shift|staff_cost|
|---------|----------|---------|-----------|----------|--------|--------------|----------|
|10/8/2022|Mindy     |Sloan    |17.25	   |10:30:00  |14:30:00|4.0	      |69.0      |   
|10/8/2022|Luqman    |Cantu    |21.5	   |10:30:00  |14:30:00|4.0	      |86.0      |
|10/8/2022|Lilly-Rose|Vaughn   |14.5       |10:30:00  |14:30:00|4.0	      |58.0      |
|10/8/2022|Desiree   |Gardner  |14.5       |10:30:00  |14:30:00|4.0	      |58.0      |
|10/8/2022|Mindy     |Sloan    |17.25	   |18:30:00  |23:00:00|4.5	      |77.625    | 

![Screenshot 2023-03-25 at 12 44 24 PM](https://user-images.githubusercontent.com/29818091/227715590-282f8623-9bcf-4785-9f3b-6341e21cdfa9.png)

Throughout the project, my SQL and dashboarding skills were put to the test. I had to create a relational database with multiple tables and set up relationships between them, ensuring data integrity and accuracy. I also had to write SQL queries to extract and manipulate data, as well as create visually appealing and informative dashboards to present this data in a clear and concise manner. Overall, this project provided me with valuable experience in database design and management, SQL programming, and dashboarding, which I can apply to future projects and career opportunities.

[Link to dashboard](https://lookerstudio.google.com/s/io2YMLtATEM)
[Queries used](https://github.com/NickZward/Personal-Projects/blob/main/The%20Pizza%20Project/Queries.txt)
