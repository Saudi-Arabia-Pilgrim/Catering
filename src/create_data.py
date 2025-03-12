import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from apps.products.models import Product
from apps.sections.models import Section, Measure
from apps.foods.models import Food, RecipeFood
from apps.menus.models import Menu, Recipe



section_names = ["Meva", "Sabzavot", "Suyug'lik", "Go'sht", "Ziravor", "Don"]
sections = {}
for name in section_names:
    section, _ = Section.objects.get_or_create(name=name)
    sections[name] = section

measure_data = [
    ("Gram", "G"), ("KiloGram", "KG"), ("Litr", "L"),
    ("MilliLitr", "ML"), ("Dona", "D"),
]
measures = {}
for name, abbreviation in measure_data:
    measure, _ = Measure.objects.get_or_create(name=name, abbreviation=abbreviation)
    measures[name] = measure

product_data = [
    ("Yog'", "MilliLitr", "Suyug'lik"),
    ("Qo'y Go'shti", "Gram", "Go'sht"),
    ("Sabzi", "Gram", "Sabzavot"),
    ("Kartoshka", "Gram", "Sabzavot"),
    ("Guruch", "Gram", "Don"),
    ("Tuz", "Gram", "Ziravor"),
    ("Pomidor", "Gram", "Sabzavot"),
    ("Bodring", "Gram", "Sabzavot"),
    ("Piyoz", "Gram", "Sabzavot"),
    ("Baliq", "Gram", "Go'sht"),
    ("Un", "Gram", "Don"),
    ("Shakar", "Gram", "Ziravor"),
    ("Smetana", "Gram", "Suyug'lik"),
    ("Tovuq Go'shti", "Gram", "Go'sht"),
    ("Qaymoq", "Gram", "Suyug'lik"),
    ("Makkajo'xori", "Gram", "Don"),
    ("Moy", "Litr", "Suyug'lik"),
    ("Limon", "Gram", "Meva"),
    ("Chesnok", "Gram", "Ziravor"),
]
products = {}
for name, measure_name, section_name in product_data:
    product, _ = Product.objects.get_or_create(
        name=name,
        measure=measures[measure_name],
        section=sections[section_name],
    )
    products[name] = product

recipe_foods = {
    "Osh": [("Yog'", 300), ("Tuz", 150), ("Guruch", 3000), ("Qo'y Go'shti", 800), ("Sabzi", 450)],
    "Mastava": [("Guruch", 500), ("Yog'", 200), ("Tuz", 100), ("Kartoshka", 100), ("Qo'y Go'shti", 250)],
    "Shorva": [("Baliq", 500), ("Piyoz", 200), ("Kartoshka", 300), ("Sabzi", 150), ("Tuz", 100)],
    "Lag'mon": [("Un", 1000), ("Qo'y Go'shti", 700), ("Piyoz", 250), ("Sabzi", 200), ("Tuz", 100)],
    "Somsa": [("Un", 500), ("Qo'y Go'shti", 600), ("Piyoz", 400), ("Tuz", 50), ("Yog'", 100)],
    "Chuchvara": [("Un", 800), ("Qo'y Go'shti", 900), ("Piyoz", 300), ("Tuz", 100), ("Yog'", 100)],
    "Borsh": [("Baliq", 500), ("Kartoshka", 400), ("Piyoz", 200), ("Tuz", 50), ("Smetana", 150)],
    "Tovuq Sho'rva": [("Tovuq Go'shti", 600), ("Piyoz", 200), ("Sabzi", 250), ("Kartoshka", 300), ("Tuz", 100)],
    "Makkajo'xori Sho'rva": [("Makkajo'xori", 400), ("Limon", 100), ("Tuz", 50), ("Chesnok", 20)],
}

for i in range(10, 130):
    food_name = f"Taom {i}"
    ingredients = [("Qo'y Go'shti", 500), ("Piyoz", 200), ("Sabzi", 150), ("Tuz", 100)]
    recipe_foods[food_name] = ingredients

food_data = [
    ("Osh", Food.Section.DEEP, 30),
    ("Mastava", Food.Section.LIQUID, 20),
    ("Shorva", Food.Section.LIQUID, 25),
    ("Lag'mon", Food.Section.DEEP, 35),
    ("Somsa", Food.Section.DEEP, 40),
    ("Chuchvara", Food.Section.DEEP, 30),
    ("Borsh", Food.Section.LIQUID, 25),
    ("Tovuq Sho'rva", Food.Section.LIQUID, 30),
    ("Makkajo'xori Sho'rva", Food.Section.LIQUID, 20),
]

for i in range(10, 130):
    food_data.append((f"Taom {i}", Food.Section.DEEP if i % 2 == 0 else Food.Section.LIQUID, 25))

foods = {}
for name, section, profit in food_data:
    food, _ = Food.objects.get_or_create(name=name, section=section, profit=profit)
    foods[name] = food

for food_name, ingredients in recipe_foods.items():
    food = foods[food_name]
    for product_name, count in ingredients:
        recipe_food, _ = RecipeFood.objects.get_or_create(
            product=products[product_name],
            defaults={"count": count}
        )
        food.recipes.add(recipe_food)

print("\033[32mCreated Successfully\033[0m")