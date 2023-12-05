## 1 Recipes

### 1.1 Query Recipes `/recipes` (POST)

``
Findings a matching recipe according to user specifications

**Request**

```ts
{
    "macros"?: {
        "calories"?: {"min": "number", "max": "number"},
        "carbs"?: {"min": "number", "max": "number"},
        "fat"?: {"min": "number", "max": "number"},
        "protein"?: {"min": "number", "max": "number"}
    },
    "dietaryRestrictions"?: "string"[],
    "culturalOrigin"?: "string",
    "maxCost"?: "number",
    "userID": "string",
    "numServings"?: "number",
    "allowIngredientsNotInPantry": "boolean"
}
```

**Returns**

```ts
    "recipes": {"recipeID": "string", "ingredientsMultiplier": "float"}
    "success": "boolean",
    "error"?: "string"
```

### 1.2 Get Recipe `catalog/{recipe_id}` (GET)

**Returns**

```json
[
  {
    "sku": "string",
    "name": "string",
    "Protein": "integer",
    "Calories": "integer",
    "ingredients":
        {
        "ingredient_id": "number",
        "ingredient_name": "string",
        "amount":
        {
            "quantity": "number",
            "aunit": "string"
        }
    }[],
    "vegan": "boolean",
    "paleo": "boolean",
    "meal_type": "string",
    "macros": "string",
    "steps": "string"[]
  }
]
```

### 1.3 Add recipe to the catalog `/recipes` (PUT)

**Request**

```ts
{
  "name": “string”,
  "macros": [“macro1”, “macro2”, …],
  "quantity": “integer”
}
```

**Returns**

```ts
{
"success": “boolean”
}
```

## 2 Virtual Fridge

### 2.1 Adding Ingredient `/fridge/add_ingredients/{ingredient_id}` (POST)
## Complex Endpoint #1

**Request**

```json
{
    "user_id": 0,
    "quantity": 0
}
```

**Returns**

```json
{
  "success": "boolean"
}
```

# Complex Endpoint #2
### 2.2 Removing Ingredient by Recipe `/fridge/remove_recipe/ingredients/{recipe_id, user_id}` (POST)

Removes all the ingredients from the fridge that are in the recipe being made

**Returns**

```json
{ "success": "boolean" }
```

### 2.3 Remove ingredients from the frigde '/fridge/remove_ingredient/{ingredient_id, user_id}' (DELETE)

**Returns**

```json
{
  "success": "boolean"
}
```

### 2.4 Get ingredients from a fridge '/fridge/get_ingredients/{user_id}'
**Returns**

```json
{
  "success": "boolean"
}
```

## 3 Shopping List

### 3.1 Add add ingredients to shopping list `/shoppingList` (POST)

Adds the needed ingredients that the user doesn't have in their fridge to a shopping list

**Request**

```json
{
  "user_id": "string",
  "ingredient_id": "string"
}
```

**Returns**

```json
{
  "success": "boolean"
}
```

### 3.2 Sort shopping list `/shoppingList/sort` (POST)

Sorts the users shopping list by what type each ingredient is, so they can buy it easy in the story

**Request**

```json
{
  "user_id": "string"
}
```

**Returns**

```json
{
  {
    "ingredient": "string",
    "amount": {
        "quantity": "number",
        "unit": "string"
        }
    }[]
}
```

## 4 User

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
