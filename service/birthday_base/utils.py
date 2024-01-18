import datetime

from database.database import manager


class CalendarManager:
    def __init__(self):
        pass

    def getseqdate(self, chat_id):
        data = manager.getAllDate(chat_id)
        users = {
            'Январь': {},
            'Февраль': {},
            'Март': {},
            'Апрель': {},
            'Май': {},
            'Июнь': {},
            'Июль': {},
            'Август': {},
            'Сентябрь': {},
            'Октябрь': {},
            'Ноябрь': {},
            'Декабрь': {}
        }
        for month in data.items():
            m = month[1]['date'].month
            match (m):
                case 1:
                    users['Январь'][month[0]] = month[1]
                case 2:
                    users['Февраль'][month[0]] = month[1]
                case 3:
                    users['Март'][month[0]] = month[1]
                case 4:
                    users['Апрель'][month[0]] = month[1]
                case 5:
                    users['Май'][month[0]] = month[1]
                case 6:
                    users['Июнь'][month[0]] = month[1]
                case 7:
                    users['Июль'][month[0]] = month[1]
                case 8:
                    users['Август'][month[0]] = month[1]
                case 9:
                    users['Сентябрь'][month[0]] = month[1]
                case 10:
                    users['Октябрь'][month[0]] = month[1]
                case 11:
                    users['Ноябрь'][month[0]] = month[1]
                case 12:
                    users['Декабрь'][month[0]] = month[1]
        return users

    def genericCalendar(self, users):
        print(users)
        line = 'Наш календарик\n'
        for date in users.items():
            for value in date[1].items():
                line += f"{date[0]}:\n{value[1]['date'].day} числа - празднует <a href='tg://user?id={value[0]}'>{value[1]['name']}</a>"
                line += "\n"
        return line
    def getChatList(self,user_id):
        return manager.getUserInChat(user_id)

service = CalendarManager()
service.genericCalendar(service.getseqdate("-1002104132939"))
