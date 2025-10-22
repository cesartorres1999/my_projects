def get_servings():
    """
    Ask the user how many servings they want to make.
    Returns:
        int: The number of servings entered by the user.
    If the user enters 0 or a negative number, an error message is shown and None is returned.
    """
    try:
        servings = int(input("Enter number of servings: "))
        if servings <= 0:
            print("Error: Number of servings must be greater than zero.")
            return None
        return servings
    except ValueError:
        print("Error: Please enter a valid integer.")
        return None


def scale_ingredients(servings):
    """
    Scale the base recipe ingredients by the number of servings.
    Args:
        servings (int): Number of servings requested.
    Returns:
        dict: A dictionary with scaled ingredient amounts.
    """
    base_recipe = {
        "flour": 100.0,   # grams per serving
        "sugar": 50.0,
        "butter": 25.0
    }
    return {ingredient: amount * servings for ingredient, amount in base_recipe.items()}


def print_scaled_recipe(servings, scaled_recipe):
    """
    Print the scaled recipe ingredients and total weight.
    Args:
        servings (int): Number of servings requested.
        scaled_recipe (dict): Scaled ingredients with weights in grams.
    """
    print(f"\nScaled recipe for {servings} servings:")
    total = 0
    for ingredient, amount in scaled_recipe.items():
        print(f"- {amount:.2f} g {ingredient}")
        total += amount
    print(f"Total: {total:.2f} g of ingredients")


def main():
    """
    Main function to run the grandma's cookie recipe scaling program.
    Steps:
    1. Ask the user for servings.
    2. Validate input.
    3. Scale and display the recipe.
    """
    servings = get_servings()
    if servings is not None:
        scaled_recipe = scale_ingredients(servings)
        print_scaled_recipe(servings, scaled_recipe)


# Run program
if __name__ == "__main__":
    main()

# Normal Case
# Input:
# 2
# Output:
# Scaled recipe for 2 servings:
# - 200.00 g flour
# - 100.00 g sugar
# - 50.00 g butter
# Total: 350.00 g of ingredients

# Edge Case (minimum valid)
# Input:
# 1
# Output:
# Scaled recipe for 1 servings:
# - 100.00 g flour
# - 50.00 g sugar
# - 25.00 g butter
# Total: 175.00 g of ingredients

# Invalid Case:
# Input:
# 0
# Output:
# Error: Number of servings must be greater than zero.
# Input:
# -3
# Output:
# Error: Number of servings must be greater than zero.
# Input:
# abc
# Output:
# Error: Please enter a valid integer.
