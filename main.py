from fastapi import FastAPI, Query
from api_handler import search_recipe, search_recipe_by_ingredients
from typing import List, Optional

app = FastAPI(title="Personalized Recipe Recommender, Chef's Choice")



@app.get("/")
def home():
    return {"message": "Welcome to the Recipe Recommender API!"}

@app.get("/recipes/search_recipe_by_ingredients")
def search_by_ingredients(ingredients:list[str]): 
    return {"Recipes :": recipes}

@app.get("/recipes/search_recipe")
def search(query: str = Query(...),
    cuisine: Optional[str] = Query(None),
    diet: Optional[str] = Query(None),
    intolerances: Optional[str] = Query(None),
    number: int = Query(5)
): 
    results = search_recipe(query,cuisine, diet,intolerances, number)
    return {"Recipes :": results }

""" def main(): 
    print("Welcome to the Chefs Choice app! For now please enter your name.")
    username = input("Enter username: ")
    # query to see if username already exists
    yes = input("Would you like to search up a recipe?")
    if(yes.lower()=="y"): 

     if(username.contains_indb): 
        printf("Welcome back!"); 
        next = input("Would you like to update or add preferences to your recipe history? (add/update)")
        if(next.lower() == "add"): 

        elif(next.lower()=="update"): 
        
        else: 
            printf("Nothing") 
    else: 
        ingredients = input("What are your current ingredients:")
        intolernaces = input("Any allergies?")
        cuisine = input("Prefernce for types of cuisine?")
 """ 