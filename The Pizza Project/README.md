I got a task from a fictional person named Ben. Ben is opening a new pizzeria in his town. It won't be a dine in. Just a delivery and take out restaurant. He has given me a project brief. The first part is to design and build a relational database for his business that will allow him to store all the important data the business collects and generates. This will in turn help Ben monitor business performance in dashboards. The main areas of focus are orders, stock control and staff.

During this project I wanted to do more than just write queries and extract data. This project includes creating a relational SQL databse, writing SQL queries to create the data sources for a dashboard & building 3 different dashboards using Google Looker.

This dataset wil consist of an order data table, a customers table, an address table, an item table, an ingridient table, a recipe table, an inventory table, a shift table, a staff table and a rota table.

The different tables and the relationship between them have been drawn using QuickDBD. After connecting all the tables, the relational SQL database will look like this: Screenshot 2023-03-22 at 5 01 32 PM

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
