from datetime import date
data = {'response': [{'first_name': 'Павел', 'id': 1, 'last_name': 'Дуров', 'sex': 2, 'bdate': '10.10.1984', 'city': {'id': 2, 'title': 'Санкт-Петербург'}, 'status': '道德經'}]}
#
#
# a = {'response': [{'first_name': 'DELETED', 'id': 3, 'last_name': '', 'deactivated': 'deleted', 'sex': 0}]}

def calculate_age(data):

    bd = (data.get('response')[0].get('bdate')).split('.')
    if len(bd) == 3:
        today = date.today()

        return today.year - int(bd[2]) - ((today.month, today.day) < (int(bd[1]), (int(bd[0]))))#interesting solution))

l = []
l['kek'] = calculate_age(data)
l['lol'] = calculate_age(data)
print(l)
