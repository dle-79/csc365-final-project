## 1 User

### 1.1 Create New User `/user/create_user` (POST)

Create a new user with a unique user id and name

**Request**
```json
{
    "name": "string"
}
```

**Returns**
```json
{
    "user_id": "integer"
}
```

### 1.2 Get User `/user/get_user/{userid}` (GET)

Get an existing user name based on an input user_id

**Request**
```json
{
    "user_id": "integer"
}
```

**Returns**
```json
{
    "name": "string"
}
```

## 2 Shopping List

### 2.1 Add Ingredients `/add_ingredients` (POST)

Add ingredients to the fridge

**Request**

```json
{
    "ingredients_needed":
        [{
            ingredient_id: integer
            quantity: integer  
        }]
    "user_id" : integer
}
```

**Request**
```
"OK"
```

### 2.2 Delete Ingredients `/remove_ingredients` (POST)

Delete ingredients from the fridge

**Request**

```json
{
    "ingredients_needed":
        [{
            "ingredient_id": integer
            "quantity": integer  
        }]
    "user_id" : integer
}
```

**Request**
```
"OK"
```

### 2.3 Sort Ingredients `/sort_ingredients` (GET)

Delete ingredients from the fridge

**Request**

```json
{
    "user_id": integer
    "parameter" : string
}
```

**Request**
```
[
    Ingredient: {
        "ingredient_id" : integer
        "quantity" : integer
    }
]
```

## 3 Recipe
### 3.1 Get Recipe Macros `/get_recipe_macros` (GET)

Get the macros given input value

**Request**

```json
{
    "recipe_constraints":
    {
        min_protein: int = 0
        max_protein: int = 10000000
        min_calories: int = 0
        max_calories: int = 100000
        vegan: bool = False
        vegetarian: bool = False
        paleo: bool = False
        min_carbs: int = 0
        max_carbs: int = 1000000
        max_time_to_make : int = 10000
        country_origin: str = "United States"
        meal_type: str = "Dinner"
    }
}
```

**Request**
```
[
    final_recipes: {
        "recipe_id": integer
        "ingredients": [string]
        "name": string
        "steps": integer
    }
]
```

### 3.2 Get Recipe based on Name `/get_recipe_name` (GET)

Get recipes based on name

**Request**

```json
{
   "recipe_name" : string
}
```

**Request**
```
[
    final_recipes: {
        "recipe_id": integer
        "ingredients": [string]
        "name": string
        "steps": integer
    }
]
```

### 3.3 Check the recipes for given values `/check_recipe_ingredient` (POST)

Check recipes

**Request**

```json
{
    "user_id": integer
    "recipe_id": integer
    "servings": integer
}
```

**Request**
```
{
    boolean
}
```

### 3.4 Get recipe ingredients `/get_recipe_ingredient` (POST)

Get recipe indgredients

**Request**

```json
{
    "user_id": integer
    "servings": integer
}
```

**Request**
```
[
    final_recipes: {
        "recipe_id": integer
        "ingredients": [string]
        "name": string
        "steps": integer
    }
]
```

## 4 Fridge
### 4.1 Get Ingredient Catalog `/get_ingredient_catalog` (GET)

Get a catalog of all the ingredients

**Request**
```
{
    "ingredient_id" (integer) : "ingredient_name" (string)
}
```

### 4.2 Add ingredients `/add_ingredients` (POST)

Add indgredients

**Request**

```json
{
    user_id: integer
    fridge_request: {
        ingredient_id : integer
        quantity : integer
    }
}
```

**Request**
```
"string"
```

### 4.3 Remove Recipe Ingredients `/remove_recipe_ingredients` (PUT)

Remove recipe ingredients for a specific recipe

**Request**

```json
{
    recipe_id: integer
    user_id: integer
}
```

**Request**
```
"string"
```

### 4.4 Remove Ingredients `/remove_ingredient` (PUT)

Remove ingredients

**Request**

```json
{
    "ingredient_id": integer
    "user_id": integer
    "quantity": integer
}
```

**Request**
```
"string"
```

### 4.5 Get Fridge Ingredients `/get_fridge_ingredients` (GET)

Get fridge ingredients

**Request**

```json
{
    "user_id" : integer
}
```

**Request**
```json
[
    {
        "ingredient": string
        "quantity": integer
        "units": integer
    }
]
```


