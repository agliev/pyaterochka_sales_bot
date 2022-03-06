from pprint import pprint
from functions import get_categories, get_closest_store, get_products

# get_categories unit test
categories_list = get_categories()
assert isinstance(categories_list, dict), 'get_categories return type test failed'
assert len(categories_list.values()) != 0, 'get_categories return len test failed'
print('get_categories return:')
pprint(categories_list)
print('\n')

# get_closest_store unit test
closest_store = get_closest_store(55.660202, 37.227595)
assert isinstance(closest_store, dict), 'get_closest_store return type test failed'
assert len(closest_store.values()) != 0, 'get_closest_store return len test failed'
print('get_closest_store return:')
pprint(closest_store)
print('\n')

# get_products unit test
category = categories_list['Замороженные продукты']
print(closest_store)
print('\n')
print(category)
print(get_products(closest_store, category))
