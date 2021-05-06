data = {'response': [{'first_name': 'Павел', 'id': 1, 'last_name': 'Дуров', 'sex': 2, 'bdate': '10.10.1984', 'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'status': '道德經'}]}
#
#
# a = {'response': [{'first_name': 'DELETED', 'id': 3, 'last_name': '', 'deactivated': 'deleted', 'sex': 0}]}
print(data.get('response')[0].get('city').get('title'))
