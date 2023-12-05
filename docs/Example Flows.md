# Example Flows

1.  Lucas wants to make a meal that feeds 20, but learns he doesn’t have enough ingredients after entering the parameters. He is missing garlic, steak and unslated butter. He then adds the ingredients to his shopping list.

- Lucas starts by calling POST /fridge/add_to_fridge_fridge_add_ingredients_post
- Lucas first calls POST/recipes, 20 for servings
- He then calls POST /shoppingList/add_to_shopList_shoppingList_add_ingredients_post in order to add the ingredients he’s missing to his shopping list

2.  Theresa wants to try a paleo diet, but doesn’t know what to make. She first adds all the ingredients she has at home to her virtual pantry. She then restricts the recipes she can give to be paleo friendly. She then receives a recipe and starts to use the ingredients. When Theresa makes it, she removes the ingredients used from her virtual pantry.

- Theresa starts by calling POST /fridge/add_to_fridge_fridge_add_ingredients_post to add all the ingredients in her virtual fridge.
- then Theresa calls POST /recipes with her paleo diet restrictions.
- She then calls POST /fridge/remove_fridge_ingredients_fridge_remove_repice_ingredients_post in order to remove the recipes from her virtual fridge.

3.  Trevor went on vacation for a year with his wife and 2 kids, but forgot to throw away his food. He first needs to update his pantry to remove all of the spoiled food. He wants to make a family meal out of all of the leftover food. He inputs his remaining ingredients and alters the serving size so it can feed four. He makes the recipe and removes the items from his virtual pantry.

- Trevor first calls POST fridge/remove_fridge_ingredients_fridge_remove_ingredient_post in order to remove the spoiled ingredients from his virtual pantry
- Trevor calls POST /recipes with serving restrictions beings set to 4
- Trevor calls POST /recipe/get_recipes_recipe_get_recipe_post to get recipes to make
- He then calls POST /fridge/remove_fridge_ingredients_fridge_remove_repice_ingredients_post in order to remove the recipes from her virtual fridge.
