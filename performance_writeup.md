##Fake Data Modeling
Table_Name : Number_of_Inputs : Justification
fridge : 388,928 : Each user will have between 10 and 50 ingredients in their virtual fridge, reflecting the diversity of items individuals typically keep on hand for cooking and daily meals. Considering the varying culinary preferences and dietary choices in real life, this range provides a flexible and realistic representation of users' virtual pantries.

ingredient : 1,662 : Users will have 10 to 50 ingredients in their virtual fridge, capturing the diversity of common items. This allows for a realistic selection, considering the prevalence of similar ingredients in various recipes.

recipe : 2,031 : This recipe size would result in 25,000 ingredients, with each recipe containing between 5 and 20 ingredients.

recipe_ingredients : 24,909 : Given 2,031 recipes, this quantity aligns with practical expectations, as each recipe will feature between 5 and 20 ingredients, ensuring a diverse yet manageable culinary experience.

review : 316,569 : Each recipe will be accompanied by a range of 5 to 300 reviews, a proportional number considering the variety of recipes available and our user base. This aligns with the expectation that approximately 3% of users will leave a review for each recipe they try.

shopping_list : 261,018 : Each user will have between 10 and 30 items on their shopping list. A reasonable amount for one shopping trip

users : 13,000 : Increasing users affects a lot of other tables so since we are scaling up to 1 million this is a suitable amount.


Total : 1,006,147





