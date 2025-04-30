import requests 
import os 
from dotenv import load_dotenv

load_dotenv() 

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
if not SPOONACULAR_API_KEY:
    raise ValueError("No Spoonacular API key set! Check your .env file.")
BASE_URL = "https://api.spoonacular.com"


def search_recipe_by_ingredients(ingredients,number_of_recipes): 
    url =f"{BASE_URL}/recipes/findByIngredients"
    params= {
        "ingredients": ",".join(ingredients),
        "number": number_of_recipes, 
        "ranking": 1, 
        "apiKey": SPOONACULAR_API_KEY
    }
    response = response.get(url, params=params)
    response.raise_for_status()
    return response.json()

def search_recipe(query="",cuisine=None,diet=None, intolerances=None,number=None): 
    url= f"{BASE_URL}/recipes/complexSearch"
    params={ 
        "query":query, 
        "cuisine": cuisine, 
        "diet": diet,
        "intolerances":intolerances,
        "number":number
    }
    params = {k: v for k, v in params.items() if v is not None}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
