from algorithm import CAT, generate_bank

items = generate_bank()

# CAT process
cat = CAT(items)
_stop = False

while True:
    (_stop, item_index) = cat.item_selection() # Get next item

    if _stop:
        break

    cat.administered_items.append(item_index)
    
    response = bool(int(input("True or False? (1 / 0): "))) # Get user respone for current question
    cat.responses.append(response)
    cat.item_administration()