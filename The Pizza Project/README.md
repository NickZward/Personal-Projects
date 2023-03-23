
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
