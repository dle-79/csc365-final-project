Fake Data Modeling

Table_Name : Number_of_Inputs : Justification

fridge : 388,928 : Each user will have between 10 and 50 ingredients in their virtual fridge, reflecting the diversity of items individuals typically keep on hand for cooking and daily meals. Considering the varying culinary preferences and dietary choices in real life, this range provides a flexible and realistic representation of users' virtual pantries.

ingredient : 1,662 : Users will have 10 to 50 ingredients in their virtual fridge, capturing the diversity of common items. This allows for a realistic selection, considering the prevalence of similar ingredients in various recipes.

recipe : 2,031 : This recipe size would result in 25,000 ingredients, with each recipe containing between 5 and 20 ingredients.

recipe_ingredients : 24,909 : Given 2,031 recipes, this quantity aligns with practical expectations, as each recipe will feature between 5 and 20 ingredients, ensuring a diverse yet manageable culinary experience.

review : 316,569 : Each recipe will be accompanied by a range of 5 to 300 reviews, a proportional number considering the variety of recipes available and our user base. This aligns with the expectation that approximately 3% of users will leave a review for each recipe they try.

shopping_list : 261,018 : Each user will have between 10 and 30 items on their shopping list. A reasonable amount for one shopping trip

users : 13,000 : Increasing users affects a lot of other tables so since we are scaling up to 1 million this is a suitable amount.

Total : 1,006,147

******************************************************************************************************************************************************************
Performance results of hitting endpoints

Endpoint_Name : Time it Takes (ms)

/user/create_user : 64.20 milliseconds

/user/get_user/{userid} : 10.04 milliseconds

/shoppingList/add_ingredients : 69.82 milliseconds

/shoppingList/remove_ingredients : 9.30 milliseconds

/shoppingList/sort_ingredients : 12.91 milliseconds

/shoppingList/add_recipe_ingredients : 161.53 milliseconds

/review/add_review : 82.45 milliseconds

/review/get_rating_by_recipe : 89.54 milliseconds

/review/get_review_by_recipe : 31.73 milliseconds

/review/get_review_by_user : 30.68 milliseconds

/review/get_rating_by_user_and_recipe : 37.60 milliseconds

/recipe/get_recipe_macros : 69.54 milliseconds

/recipe/get_recipe_name : 31.64 milliseconds

/recipe/check_recipe_ingredient : 17.04 milliseconds

/fridge/get_ingredient_catalog : 58.69 milliseconds

/fridge/add_ingredients : 18.31 milliseconds

/fridge/remove_recipe_ingredients : 5.95 milliseconds

/fridge/remove_ingredient : 15.85 milliseconds

/fridge/get_fridge_ingredients : 52.05 milliseconds

Three slowest endpoints:
1) /shoppingList/add_recipe_ingredients
2) /review/add_review 
3) /review/get_rating_by_recipe

******************************************************************************************************************************************************************
Performance Tuning:

Endpoint : EXPLAIN ANALYZE : Meaning : Add indexing : Result

--------------------------------------------------------------------------------------------------------------------------------------------------------------------
/shoppingList/add_recipe_ingredients
[('Index Scan using shopping_list_pkey on shopping_list  (cost=0.42..8.44 rows=1 width=8) (actual time=0.125..0.125 rows=0 loops=1)',), ('  Index Cond: ((user_id = 80) AND (ingredient_id = 80))',), ('Planning Time: 0.452 ms',), ('Execution Time: 0.153 ms',)]      [('Update on shopping_list  (cost=0.42..8.44 rows=0 width=0) (actual time=0.012..0.012 rows=0 loops=1)',), ('  ->  Index Scan using shopping_list_pkey on shopping_list  (cost=0.42..8.44 rows=1 width=14) (actual time=0.010..0.010 rows=0 loops=1)',), ('        Index Cond: ((user_id = 80) AND (ingredient_id = 80))',), ('Planning Time: 0.088 ms',), ('Execution Time: 0.207 ms',)]

Indexes are all ready being applied to the columns user_id and ingredient. This is because we defined the two keys to be unique so indexing has already been applied. So adding an index should change the time.

[('Index Scan using shopping_list_pkey on shopping_list  (cost=0.42..8.44 rows=1 width=8) (actual time=0.333..0.334 rows=0 loops=1)',), ('  Index Cond: ((user_id = 80) AND (ingredient_id = 80))',), ('Planning Time: 0.692 ms',), ('Execution Time: 0.365 ms',)]    [('Update on shopping_list  (cost=0.42..8.44 rows=0 width=0) (actual time=0.011..0.011 rows=0 loops=1)',), ('  ->  Index Scan using shopping_list_pkey on shopping_list  (cost=0.42..8.44 rows=1 width=14) (actual time=0.009..0.010 rows=0 loops=1)',), ('        Index Cond: ((user_id = 80) AND (ingredient_id = 80))',), ('Planning Time: 0.088 ms',), ('Execution Time: 0.225 ms',)] 

The result time is similar which is what was to be expected.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------
/review/add_review

[('Insert on review  (cost=0.00..0.01 rows=0 width=0) (actual time=2.754..2.755 rows=0 loops=1)',), ('  ->  Result  (cost=0.00..0.01 rows=1 width=66) (actual time=0.313..0.314 rows=1 loops=1)',), ('Planning Time: 0.058 ms',), ('Execution Time: 2.797 ms',)]

There is no actually time difference because it is an insert function. The tiem must be coming from the python side and not the sql. There is nothing to create an index around because it is not getting, updating and deleting. Therefore we should do nothing.

[('Insert on review  (cost=0.00..0.01 rows=0 width=0) (actual time=2.688..2.755 rows=0 loops=1)',), ('  ->  Result  (cost=0.00..0.01 rows=1 width=66) (actual time=0.299..0.314 rows=1 loops=1)',), ('Planning Time: 0.058 ms',), ('Execution Time: 2.679 ms',)]

As excepted it didn’t do anything.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------
/review/get_rating_by_recipe

[('Gather  (cost=1000.00..6270.61 rows=149 width=43) (actual time=1.943..57.541 rows=251 loops=1)',), ('  Workers Planned: 1',), ('  Workers Launched: 1',), ('  ->  Parallel Seq Scan on review  (cost=0.00..5255.71 rows=88 width=43) (actual time=23.265..49.855 rows=126 loops=2)',), ('        Filter: (recipe_id = 17)',), ('        Rows Removed by Filter: 158160',), ('Planning Time: 0.903 ms',), ('Execution Time: 57.602 ms',)]

This is being done in parallel. However there is no indexing going on so I adding an index should make the query faster.

[('Index Scan using recipe_id_idx on review  (cost=0.42..12.10 rows=149 width=43) (actual time=0.177..0.202 rows=251 loops=1)',), ('  Index Cond: (recipe_id = 17)',), ('Planning Time: 0.407 ms',), ('Execution Time: 0.233 ms',)]

Yes it did make it a lot faster. Going from around 57ms to 0.233. Really good improvement!
