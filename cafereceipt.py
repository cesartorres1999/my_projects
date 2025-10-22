# Mini Receipt Calculator
# Defined function to calculate total price for one item
def item_total_calculator(price, quantity):
    return price * quantity
# Defined function to calculate grand total
def grand_total_calculator(firstitemtotal, seconditemtotal):
    return firstitemtotal+seconditemtotal
# Gather inputs for first item
first_item_name = input("Enter name of first item: ")
first_item_price = float(input(f"Enter price of {first_item_name}: "))
first_item_quantity = int(input(f"Enter quantity of {first_item_name}: "))
# Get inputs for second item
second_item_name = input("Enter name of second item: ")
second_item_price = float(input(f"Enter price of {second_item_name}: "))
second_item_quantity = int(input(f"Enter quantity of {second_item_name}: "))
# Calculate totals
firstitemtotal = item_total_calculator(first_item_price, first_item_quantity)
seconditemtotal = item_total_calculator(second_item_price, second_item_quantity)
grand_total = grand_total_calculator(firstitemtotal, seconditemtotal)
# Print Simple Receipt
print(f"{first_item_name} x{first_item_quantity} @ ${first_item_price:.2f} = ${firstitemtotal:.2f}")
print(f"{second_item_name} x{second_item_quantity} @ ${second_item_price:.2f} = ${seconditemtotal:.2f}")
print(f"Grand Total: ${grand_total:.2f}")
