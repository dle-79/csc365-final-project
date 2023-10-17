## 1 Recipes

### 1.1 Query Recipes `/recipes` (POST)

``
Findings a matching recipe according to user specifications

**Request**

```json
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

```json
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

```json
{
  "name": “string”,
  "macros": [“macro1”, “macro2”, …],
  "quantity": “integer”
}
```

**Returns**

```json
{
"success": “boolean”
}
```

## 2 Virtual Fridge

### 2.1 Adding Ingredient `/ingredients/{ingredient_id}` (PUT)

**Request**

```json
{
  "user_id": "string",
  "amnount": {
    "quantity": "number",
    "unit": "string"
  }
}
```

**Returns**

```json
{
  "success": "boolean"
}
```

### 2.2 Removing Ingredient by Recipe `/ingredients/recipe_remove` (POST)

Removes all the ingredients from the fridge that are in the recipe

**Request**

```json
{
    “recipe_id” : “string”,
    “scalar” : “number”,
    “user_id” “string”
}
```

**Returns**

```json
{ "success": "boolean" }
```

### 2.3 Update quantity of ingredient `ingredients/{ingredient_id}` (POST)

**Request**

```json
{
  "user_id": "string",
  "amount": {
    "quantity": "number",
    "unit": "string"
  }
}
```

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

# Example Flows

1.  Lucas wants to make an Italian meal that feeds 20, but learns he doesn’t have enough ingredients after entering the parameters. He learns which ingredients he’s missing and adds it to his shopping list. He also finds what aisle the ingredients are and goes shopping.

- Lucas first calls POST/recipes, entering Italy for cultural origin, 20 for servings, and sets allow missing ingredients to be true
- He then calls POST/shoppingList in order to add the ingredients he’s missing to his shopping list
- He finally calls POST/shoppingList/sort to order his list by aisle to shop quickly

2.  Theresa wants to try a paleo diet, but doesn’t know what to make. She first adds all the ingredients she has at home to her virtual pantry. She then restricts the recipes she can give to be paleo friendly. She then receives a recipe and starts to use the ingredients. When Theresa makes it, she removes the ingredients used from her virtual pantry.

- Theresa starts by calling POST /ingredients/{ingredient_id} to add all the ingredients in her virtual pantry.
  -then Theresa calls POST /recipes with her paleo diet restrictions.
- She then calls POST /ingredients/{ingredient_id}/recipe_remove in order to remove the recipes from her virtual pantry

3.  Trevor went on vacation for a year with his wife and 2 kids, but forgot to throw away his food. He first needs to update his pantry to remove all of the spoiled food. He wants to make a family meal out of all of the leftover food. He inputs his remaining ingredients and alters the serving size so it can feed four. He makes the recipe and removes the items from his virtual pantry.

- Trevor first calls POST /ingredients/{ingredient_id}/remove in order to remove the spoiled ingredients from his virtual pantry
- then Theresa calls POST /recipes with serving restrictions beings set to 4 and allow extra ingredients to be False
- She then calls POST /ingredients/{ingredient_id}/recipe_remove in order to remove the recipes from her virtual pantry
