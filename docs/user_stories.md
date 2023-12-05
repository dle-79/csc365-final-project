# Stories

- As a bodybuilder, I want to design a meal plan that stays within a calorie range and meets a protein threshold, so I can meet my dietary goals
- As a home cook, I want to be able to find recipes that use ingredients that I have in my kitchen, so I can avoid going grocery shopping if I don't need it
- As a home cook, if I do need any groceries, I'd like to sort them by what aisle/type they are, so I can save time at the store
- As someone with dietary restrictions, I want to be able to generate recipes that meet my restrictions, so I can eat within my restriction
- As the cook for my family, I want to be able to find recipes that will feed my entire family for a week night dinner, so I don't have to spend time looking for recipes
- As a foodie, I want to be able to find recipies based on their cultural background, so I experience new tastes
- As someone who already has some food made, I want to find what recipes I can make that will meet my goals, incorporating the nutrients of my current food, so I can create a balanced meal.
- As a frugal person, I want to find recipes that meet my nutritional goals as cheap as possible, so I can save money
- As a student, I want to find recipes that i can meal prep, so I can avoid spending time on weeknights
- As someone who wants breakfast for dinner, I want to be able to specify what type of meal (breakfast, lunch, dinner) when generation a recipe, so I can meet my tastes
- As someone in a rush, I want to be able find meals that take as little time as possible to make, so I can save on time.
- As someone who's skeptical recipes, I want to be able to only generate well-rated recipes, so I can avoid making a bad meal
- As a home cook, I want to be able to add ingredients into a virtual pantry, so I know what I have in stock, an I can find recipes based on my ingredients
- As a cook, when I make a recipe, I want to substract those ingredeitns from my virtual pantry, so I don't have to manually update it
- As a home cook, I want to be able to add a recipe to a planned list of recipes I'll make, and then it'll add any ingredients I need to a shopping list

# Exceptions

Execption: no recipes found for macro/calory range:
Response: recommend recipes that are close to the range, and give option to reprompt with wider range

Exception: No recipes found with current ingredients:
Response: recommend recipes that include substitutions that you have, or recommend recipes that have most of the ingredients. Also, give users the option to reprompt

Exception: They're might be a ingredient that doesn't have a type for it, when sorting ingredients by type
Response: Sort them by "other" type, but give users the option to manually input a type for ingredients

Exception: no recipes found for macro/calory range:
Response: Recommend recipes that are close to the range, and give option to reprompt with wider range

Exception: returned recipe doesn't actually meet users dietary restrictions:
Response: users can flag recipes as wrong, and make note not to return that recipe to that user.

Exception: no recipes can meet their dietary restrictions:
Response: return recipes that meet some one of them, if available, and give option to reprompt

Exception: No recipes found for desired serving amount
Response: offer recipes that match dietary restrictions, but modify amount to meet serving size

Exception: no recipes found for cultural background
Response: Ask user to reprompt

Exception: user enters a negative number for ingredient amount
Response: Database isn't update, alert user of error and ask to reprompt

Exception: user inputs an ingredient that doesn't exist
If a user inputs an ingredient that doesn't exist, don't add it to the database, and ask them to reinput it

Exception: no recipes found for given filter, and no near matches
Response: Ask user to change parameters

Exception: No combination exists between currently made food, and possible recipes for nutritional goals
Response: Return recipes that are closer to meeting goals, and offer to reprompt
