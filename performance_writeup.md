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





