import requests

for i in range(7):
    name = f"Ovqat{i}"
    section = i%2
    profit = 20
    recipes = []
    recipes_json = requests.get(url="http://localhost:8000/api/v1/foods/recipe_foods/").json()["results"]
    count = 0
    for recipe in recipes_json:
        count =+ 1
        recipes.append(recipe["id"])
        if count == 3:
            break
    requests.post(url="http://localhost:8000/api/v1/foods/", data={
        "name": name,
        "section": section,
        "profit": profit,
        "recipes": recipes
    })
