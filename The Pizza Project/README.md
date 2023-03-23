
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
