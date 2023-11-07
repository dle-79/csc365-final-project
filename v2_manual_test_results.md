# Example workflow
1. Lucas wants to make a meal that feeds 20, but learns he doesn’t have enough ingredients after entering the parameters. He is missing garlic, steak and unslated butter. He then adds the ingredients to his shopping list.

- Lucas starts by calling POST /fridge/add_to_fridge_fridge_add_ingredients_post
- Lucas first calls POST/recipes, 20 for servings
- He then calls POST /shoppingList/add_to_shopList_shoppingList_add_ingredients_post in order to add the ingredients he’s missing to his shopping list

2. Trevor went on vacation for a year with his wife and 2 kids, but forgot to throw away his food. He first needs to update his pantry to remove all of the spoiled food. He wants to make a family meal out of all of the leftover food. He inputs his remaining ingredients and alters the serving size so it can feed four. He makes the recipe and removes the items from his virtual pantry.

- Trevor first calls POST fridge/remove_fridge_ingredients_fridge_remove_ingredient_post in order to remove the spoiled ingredients from his virtual pantry
- Trevor calls POST /recipes with serving restrictions beings set to 4
- Trevor calls POST /recipe/get_recipes_recipe_get_recipe_post to get recipes to make
- He then calls POST /fridge/remove_fridge_ingredients_fridge_remove_repice_ingredients_post in order to remove the recipes from her virtual fridge.

# Testing results Trevor
1. Removes the item that went bad brussel sprouts
curl -X 'POST' \
  'http://127.0.0.1:8000/fridge/remove_ingredient?ingredient_id=25&user_id=4' \
  -H 'accept: application/json' \
  -d ''

2. "OK"

3. Find recipes
curl -X 'POST' \
  'http://127.0.0.1:8000/recipe/get_recipe?user_id=4' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "protein": 0,
  "calories": 0,
  "vegan": false,
  "vegetarian": false,
  "paleo": true,
  "carbs": 0,
  "servings": 4,
  "time_to_make": 0
}'

4. 
[
  {
    "recipe_id": 2,
    "sku": "GARLIC_BUTTER_STEAK_BITES_0",
    "name": "garlic butter steak bites",
    "steps": "1. Season the steak bites with salt, pepper, and red pepper flakes and stir until well coated.\n2. Heat a large skillet over medium-high heat. Add the avocado oil to the hot skillet and then add the steak in a single layer. Cook the steak bites for 3-4 minutes until brown, stirring occasionally. You may have to do this in batches depending on the size of your skillet. Once the steak is brown, remove it from the pan.\n3. Remove any excess water from the skillet and then add the butter or ghee to the pan. Next add the garlic and saute for 1 minute.\n4. Add the steak back to the pan and cook for 1-2 minutes stirring to coat it in the butter sauce. Remove the pan from the heat and stir in the chopped parsley. Garnish with green onion and serve immediately."
  }
]

5. Remove the ingredients used
curl -X 'POST' \
  'http://127.0.0.1:8000/fridge/remove_repice_ingredients?recipe_id=4&user_id=2' \
  -H 'accept: application/json' \
  -d ''

6. "OK"


# Testing results Lucas
1. Lucas user is created 
curl -X 'POST' \
  'http://127.0.0.1:8000/user/' \
  -H 'accept: application/json' \
  -H 'access_token: recipe' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Lucas"
}'

2. "string"

3. Remove looks to see if he can make any recipe with 20 servings
curl -X 'POST' \
  'http://127.0.0.1:8000/recipe/get_recipe?user_id=3' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "protein": 0,
  "calories": 0,
  "vegan": true,
  "vegetarian": true,
  "paleo": true,
  "carbs": 0,
  "servings": 20,
  "time_to_make": 0
}'

4. "no recipes available"

5. Add the ingredients to his shopping list
curl -X 'POST' \
  'http://127.0.0.1:8000/shoppingList/add_ingredients?user_id=3' \
  -H 'accept: application/json' \
  -H 'access_token: recipe' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "id": 13,
    "name": "steak",
    "quantity": 5
  },
{
    "id": 7,
    "name": "garlic",
    "quantity": 6
  },
{
    "id": 15,
    "name": "unsalted butter",
    "quantity": 2
  }
]'

6. "OK"