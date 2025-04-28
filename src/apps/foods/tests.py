# import requests
#
# for i in range(7):
#     name = f"Ovqat{i+1}"
#     section = i % 2
#     profit = 20
#     recipes = []
#     recipes_json = requests.get(
#         url="http://localhost:8000/api/v1/foods/recipe_foods/"
#     ).json()["results"]
#     count = 0
#     for recipe in recipes_json:
#         count += 1
#         recipes.append(recipe["id"])
#         if count == 4:
#             break
#     print(
#         requests.post(
#             url="http://localhost:8000/api/v1/foods/",
#             data={
#                 "name": name,
#                 "section": section,
#                 "profit": profit,
#                 "recipes_id": recipes,
#             },
#         ).json()
#     )


import requests
#
# for i in range(6):
#     data = {
#         "name": f"Ovqat{i}",
#         "recipes_id": ["9c47bdfa-a8f6-4ef0-a4a1-ae0797ef0b7c"],
#         "section": "a8d53a53-5095-4a8a-b9b1-626bfbf47578",
#         "profit": 20,
#         "image": None
#     }
#     url = "http://localhost:8000/api/v1/foods/"
#
#     response = requests.post(url=url, data=data)
#
#     print(response.status_code)


# url = "http://localhost:8000/api/v1/foods/"
# response = requests.get(url=url).json()
#
# ids = []
#
# for obj in response["results"]:
#     ids.append(obj["id"])
#
# print(ids)

for i in range(3):
    url = "http://127.0.0.1:8000/api/v1/menus/"
    data = {
        "name": f"{i}Recipe",
        "foods_id": [
                    "3634f89d-9f45-4d3d-95fe-18991716c4a0",
                    "b06c8759-08b9-4d19-813c-ec67bb1e9304",
                    "e4d6e7d3-3eba-4890-b137-de57ea0c67b4",
                    "c7768839-4cfa-492d-b748-8d19948e630b",
                    "d0a41c2e-a80b-4f8a-aaeb-3e7bcd6b8269",
                    "05131a0f-599f-45b6-a7fe-2067174338f5",
                    "943d665a-9dd2-4323-bf76-4dc90b02cfa6"
                ],
        "profit": 20,
        "image": None
    }
    response = requests.post(url=url, data=data)
    print(response.status_code, response.json())
