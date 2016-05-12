#Commands to see options, inventory, and craft itmes.
commands = {
                "i" : "see inventory",
                "c" : "see crafting options",
                "craft [item]" : "craft something from inventory items",
           }

#an inventory of items
items = {
            "flint" : 50,

            "grass" : 100,
            "hay" : 0,

            "tree" : 100,
            "log" : 0,

            "sapling" : 100,
            "twig" : 0,

            "boulder" : 30,
            "rock" : 0,

            "pickaxe" : 0,
            "axe" : 0,

            "firepit" : 0,
            "tent" : 0,

            "torch" : 0,
        }

# Items needed to make an item for survival.
craft = {
            "hay" : { "grass" : 1 },
            "twig" : { "sapling" : 1 },
            "log" : { "axe" : 1, "tree" : 1 },
            "axe" : { "twig" : 3, "flint" : 1 },
            "tent" : { "twig" : 10, "hay" : 15 },
            "firepit" : { "boulder" : 5, "log" : 3, "twig" : 1, "torch" : 1 },
            "torch" : { "flint" : 1, "grass" : 1, "twig" : 1 },
            "pickaxe" : { "flint" : 2, "twig" : 1 }
        }

defaults = {
	"wins" : 10,
	"total_played": 0
}

def loadInventory():
    inven= Inventory(flint = items.get("flint"), grass=items.get("grass"), boulder=items.get("boulder"), hay = items.get("hay"))
    return inven

#inven= Inventory(flint = items.get("flint"), grass=items.get("grass"), boulder=items.get("boulder"), hay = items.get("hay"))
