from algorithm import CAT
# this function generates an item bank, in case the user cannot provide one
from catsim.cat import generate_item_bank
import catsim.plot as catplot

# generating an item bank
print('Generating item bank...')
bank_size = 50
items = generate_item_bank(bank_size, '1PL')

#catplot.gen3d_dataset_scatter(items, 'Question banks', show = True)

#catplot.item_curve(b = items[0][1], title = 'Question 0')

cat = CAT(items)