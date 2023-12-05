# Peer Review Responses

## Schema/API Design
- /ingredients (GET) endpoint to see what is in the fridge would be helpful for knowing what to add/update
  - Added get_fridge_ingredients to fridge.py
- Adding Ingredient /ingredients/{ingredient_id} should be POST instead of PUT
  - Updated POST to PUT
- Update quantity of ingredient ingredients/{ingredient_id} should be PUT instead of POST
   - Updated POST to PUT
- Removing Ingredient by Recipe /ingredients/recipe_remove should be DELETE instead of POST
   - Updated POST to DELETE
- Query Recipes /recipes should be get instead of POST
   - Changed endpoints, and now takes in a body so need to be a POST
- Similiar endpoints like Add recipe to the catalog (PUT) and Sort shopping list /shoppingList/sort (POST) also need to be changed but are similar to 2-5.
   - Updated both enedpoints
-  /recipe/get_recipe and /shoppingList/sort_ingredients should be GET instead of POST
   - Changed endpoints, and now takes in a body so need to be a POST
1. I think adding an ingredient should be (POST) and updating should be (PUT)
   - Change
1. change a /shoppingList/sort (POST) to a (GET)
   - Changed
1. Should add a password colums when creating users to protect user accounts from malicious parties
   - Help
- Time_to_make column in the recipes table is never used in the code to filter out recipes
   - Used in recipe.py
- Aisle column is not used in data, maybe sorting by quantity would be more intuitive
   - Used in sort_ingredients in shopping_list.py, can now sort by three different parameters
- Units may be important for certain recipes/ingredients
   - Have a units column in the ingredient table
- It may be better to use an Ingredient SKU over ingredient_id
   - No, since sku would be similar to name
- Quantity is stored as text for ingredient table, and as an int in other tables. Should be int for everything.
   - Renamed quantity to units in ingredient table for clarity, remains a string
- num_ingredients is not necessary since you can count the ingredients using recipe_ingredients
   - Deleted column from recipe table
- For /recipe/get_recipe, it's unclear what values the user is supposed to enter for protein, calories, carbs, etc, since so far we have been setting all of those parameters to 0 and accessing recipes. If entering an exact number for each macro is too complicated to implement, you could allow users to specify "high / low protein" or "high / low calorie" instead. Defining categories for the macros may make it easier to retrieve recipes that match the search criteria best.
   - Added min and max parameters for all macro values
- For all endpoints that ask to enter ingredient_id, it may be easier for the user to just enter the ingredient name, since I didn't know which ID to input for ingredients not referenced in the example flows.
   - No, since this is a backend, it wouldn't need to know the name. For testing, added catalog of all ingredients
- On the same note, add an endpoint like /get_ingredient_list to one of the classes so that users can see what ingredients they can query without returning error
   - Added get_catalog in fridge.py
- In /user/{userid}, entering the user's name instead of user ID to retrieve the cart would be more intuitive
   - No, since this is backend, id is easier to reference. For testing, added endpoint to get id from username
- In general, all endpoints that ask to enter user_id could be changed to ask for the user's name
   - See above
- Endpoints like /fridge/remove_recipe_ingredients should accept the recipe name instead of the recipe ID, since users don't know what ID to enter
   - See comment above, added get_recipe_by_name endpoint in recipe.py
- /fridge/remove_recipe_ingredients and /fridge/remove_ingredient could be combined into just one endpoint, since they both remove fridge ingredients, and knowing which one to use is confusing as a user. Having an endpoint that takes in the recipe, user, and ingredients to be removed all at once would be much easier to keep track of
   - Modified endpoints so they differ
- The aisle column in the ingredient table is never updated / used, which may have caused issues in the /shoppingList/sort_ingredients endpoint since the list is ordered by aisle
   - Updated so aisle column is used
- The time_to_make column in the recipes table is also never used in the code to filter out recipes, so it doesn't make a difference if users want to put a time constraint
   - Added it to get_recipe constraint
- For all tables that reference ingredients, there should be a column that stores the ingredient name (in fridge, in shopping list) so it's much easier to see on your end what ingredients are being stored rather than having to reference the IDs each time
   - Didn’t modify, ingredient_id is easier to reference in code, adding extra column is repetitive, and since this is backend, it doesn't require it
- Consider changing the way you sort ingredients in the shopping list - could sort alphabetically or by quantity if the aisle category is still not going to be used
   - Added parameter for it
- The user ID (or name) should be a parameter for the fridge/add_ingredients endpoint, and the ingredient_id's along with their quantities should be put in the request body, so that the user can add multiple ingredients to their fridge at once
   - Updated
- looking at the ER diagram, I'm a little confused as to how the shopping list links to the ingredient. Perhaps it would be beneficial to include an ingredient_id in "shopping_list" (i think you did in your code/schema)
   - Modified
- looking at the ER diagram, I see array values for ingredients and steps. I think it makes sense to have array values for steps, but ingredients should be a separate table (which I think you did in your schema)
   - Changed
- since you are dealing with ingredients a big part of storing the data is also the amount with units. It might be useful to include the units in "shopping_list", "ingredient", "recipe_ingredient"...
   - No, the units can be referenced in the ingredient table, repetitive
- decide how to implement shopping list: I noticed how you included is_bought on your ER diagram but couldn't find it in your code for getting and removing ingredients. Removing an ingredient is deleting it from the shopping list or is it just checking off the is_bought so you can keep track of what you bought
   - Removed purchased column
- In recipe you don't include a vegetarian option but include in ingredient
   - Added to recipe constraint
1. I wonder if you can just store vegan/vegetarian/paleo properties in ingredients or in recipe (to see if a recipe has these prop check if every ingredient has a True value for vegan/vegetarian/paleo)
   - May take a while to run
1. Additionally in testing, I noticed that the recipe may not appear if the vegan/vegetarian is not set to True - maybe it'd be beneficial to have the recipes show up even though they are vegan/vegetarian/paleo when set to False, but only the VVP recipes to show up when set to True
   - Maybe add????
- It may help to have some constraints on specific columns. For example, the quantity in the "ingredient" table shouldn't be null - maybe 0 for default.
   - Added constraints
- same goes for total protein, calories, carbs, fat since they can be calculated from ingredients table
   - No, can be different nutritionally when you cook things
- it might be good to have units in fridge (like you had in your ER diagram)
   - Units are in ingredient table, so everything is already standardized
- for catalog/{recipe_id} it might be better to add a request for recipe_id?
   - Couldn’t find this code
- Inputting both Id and name seems redundant for adding ingredients to shoplist, especially since user does not know ingredient Ids
   - Removed name for adding ingredient to shop list
- I suggest adding a login endpoint to authorize users before giving them access to their sensitive account data
   - No, since this is a backend we don’t need login endpoint
1. Units for time to make should be clarified
   - Added to API spec
1. sort_ingredients should be a GET (labelled as POST on docs)
   - get_recipe should be a GET (labelled as POST on docs)
1. recipe_id should be requested for remove_recipe_ingredients and not a parameter (user cannot enter the recipe id)
   - idk
1. add ingredients to shoplist should take a recipe_id and add what to the list what isnt in your fridge instead of manually entering it (Or another endpoint with this option)
   - asdf
- Add a description to recipes so users can get an idea about it before they make it
   - added


## Code Fixes

- Any comments about recipe omitted and addressed, redid endpoint
   - Fixed
- Endpoints files duplicated in main and src folders like shopping_list.py,user.py,etc
   - Deleted
- .env file should not be in repository because it contains sensitive information
   - Deleted
1. curl in v1/v2 manual tests results should have render.com url, not local url
   - fixed
- .scalar_one() should be used when selecting only one value instead of .first()
   - Changed
- create_user inserts name into user table, but does not insert email or phone, as per ER diagram
   - Removed email and phone from user table
- Function get_cart named inappropriately, should probably be called get_user
   - Renamed
- remove_fridge_ingredients function name is used twice in fridge.py
   - Changed names and differentiated function
- Maybe set the paleo/vegan/vegetarian to false by default, currently defaults to true when testing endpoints
   - Set
1. Maybe return success or failure if a user tries to delete something from shoplist that they dont have in remove_shoplist
- Id in Ingredients class is ambiguous for user (asks for Id, but doesn't specify which Id when testing)
   - Renamed to ingredient_id
- Consider limiting how many search results are returned if a lot of recipes meet the search criteria
   - Added LIMIT 10 to SQL statement
- add_ingredients requests user_id and has ingredient_id as a parameter, should be the other way around. And maybe request ingredient name instead of id
   - Switched, don't request name anymore
   - Added get_ingredient_catalog to return a catalog of ingredients
- /remove_ingredient should allow you to input how much of that ingredient to remove
   - Added functionally
1. recipe_id should be a requested value in /remoe_recipe_ingredients, not a parameter (user can't enter paramters)
   
1. Remove recipe ingredients endpoint in v1_manual_test_results is spelled incorrectly in the link
1. Endpoints in v2_manual_test_results may have been copy-pasted wrong in the user story descriptions, because the names are twice as long and don't match up to the API Spec

- For endpoints in fridge.py that take in ingredient_id as a parameter, it may make more sense for the user to enter the name of the ingredient rather than the id. 
   - id is easier to reference throughout code

- The duplicate method remove_fridge_ingredients(recipe_id: int, user_id: int) can be renamed to something like remove_recipe_from_fridge to avoid confusion when referencing both remove methods
   - renamed
1. Raise errors or print message when user tries to remove fridge ingredients that don't exist, and display current fridge contents, so that user knows why the request didn't go through
1. /remove_ingredients should be modified so that if users try to remove ingredients from the fridge that don't exist, an error or message is written instead of just returning "OK"
- /remove_ingredients should also be storing ingredients and the quantities associated with each ingredient together, to streamline the process of deleting ingredient from the list that were found in the fridge already
   - Made both a requested item
- /sort_ingredients returns Internal Server Error because aisle was never assigned a value for each ingredient, and we are trying to sort by aisle. Instead of checking if ingredients were already in the fridge before sorting, it would be easier to just access the list and sort by some attribute like alphabetical order or quantity.
   - Endpoint works now
- In general, allowing users to enter their username instead of ID in the parameters would be more intuitive. Could also place a restraint requiring that the name column is unique to avoid confusion
   - Made username column unique constraint, id easier to reference throughout code
- might be helpful to have a docs folder
   - Created docs folder
1. try/raise statements for update/insert transactions

- What if the quantity to be removed is greater than what we have?
   - Checks for thsi now

could be useful to have a pagination feature to see the recipes if there are too many recipes that meet the criteria


- from my understanding, remove_shoplist will remove the ingredient from the list if we have enough of it in our fridge. Could it be useful to update the value in the shopping list with the new amount of things that we need? Say we have 12 eggs in the fridge, but we need 24 eggs. Should the shopping list say 12 or 24 eggs needed?
   - Quantity is based on standardized units in 
1. could be useful to have multiple search possibilities, like the search endpoint in the potion shop

1. Could add Try Except conditions to check for exceptions in the insert/update queries
1. add_to_fridge endpoint does not check for possible invalid inputs, like if quantity is a negative number
   - check

