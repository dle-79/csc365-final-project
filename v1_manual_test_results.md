# Example workflow
Theresa then calls POST /ingredients/{ingredient_id}/recipe_remove in order to remove the recipes from her virtual pantry

# Testing results
<Repeated for each step of the workflow>
Removing Ingredient by Recipe /ingredients/recipe_remove (POST)
curl -X 'POST' \


Removes all the ingredients from the fridge that are in the recipe

Request
curl
    “recipe_id” : "int",
    “fridge_id” : "int"
Returns

{ "success": "boolean" }

