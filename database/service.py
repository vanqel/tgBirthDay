import datetime
import json

import asyncio



def usecsv(func):
    def wrapper(*args, **kwargs):
        flag = False
        try:
            a = pd.read_csv('keys_100_first.csv', sep=';')
            a = a.set_index("Value")
            result = func(a, *args, **kwargs)
            result[0].to_csv('keys_100_first.csv', sep=';', encoding="utf-8")
            print("DONE")
            return result[1]
        except Exception as ex:
            print(ex)

    return wrapper

@usecsv
def update_database(a):
    for i, v in a.iterrows():
        manager.add_key(i, v['Link'], 'Active')
        print(f'index - {i} added')


#manager.reloadTable()
#update_database()
A = "{\"\u0412\u0430\u0448 \u043b\u043e\u0433\u0438\u043d telegram\": \"dasd\", \"\u0412\u0430\u0448\u0435 \u0438\u043c\u044f\": \"asdasda\", \"\u0412\u0430\u0448 \u043f\u043e\u043b\": \"\u041c\u0443\u0436\u0441\u043a\u043e\u0439\", \"\u0414\u0430\u0442\u0430 \u0442\u0432\u043e\u0435\u0433\u043e \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f\": \"2321-02-12\"}"
print()