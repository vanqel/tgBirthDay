from aiogram import Bot

from database.database import database_manager


class CalendarManager:
    def __init__(self):
        pass

    async def getseqdate(self, chat_id: int | str, bot: Bot):
        name_chat = await bot.get_chat(chat_id)
        name_chat = name_chat.title
        data = database_manager.get_all_users_date(chat_id)
        users = {
            '❄️ Январь': {},
            '❄️ Февраль': {},
            '🌱 Март': {},
            '🌱 Апрель': {},
            '🌱 Май': {},
            '🔆 Июнь': {},
            '🔆 Июль': {},
            '🔆 Август': {},
            '🍁 Сентябрь': {},
            '🍁 Октябрь': {},
            '🍁 Ноябрь': {},
            '❄️ Декабрь': {}
        }
        for month in data.items():
            m = month[1]['date'].month
            match (m):
                case 1:  #
                    users['❄️ Январь'][month[0]] = month[1]
                case 2:
                    users['❄️ Февраль'][month[0]] = month[1]
                case 3:
                    users['🌱 Март'][month[0]] = month[1]
                case 4:
                    users['🌱 Апрель'][month[0]] = month[1]
                case 5:
                    users['🌱 Май'][month[0]] = month[1]
                case 6:
                    users['🔆 Июнь'][month[0]] = month[1]
                case 7:
                    users['🔆 Июль'][month[0]] = month[1]
                case 8:
                    users['🔆 Август'][month[0]] = month[1]
                case 9:
                    users['🍁 Сентябрь'][month[0]] = month[1]
                case 10:
                    users['🍁 Октябрь'][month[0]] = month[1]
                case 11:
                    users['🍁 Ноябрь'][month[0]] = month[1]
                case 12:
                    users['❄️ Декабрь'][month[0]] = month[1]
        return self.genericCalendar(users, name_chat)

    def genericCalendar(self, users, name_chat):
        line = f'<b> Наш календарик | {name_chat}</b>\n\n'
        for date in users.items():
            if date[1] != {}:
                print(date[1])
                line += f"  <b>{date[0]}:</b> \n"
                for value in date[1].items():
                    line += f"      - <i>{value[1]['date'].day} числа </i> - празднует  <a href='https://t.me/{value[1]['login']}'>{value[1]['name']}</a>\n"
        line += "\n<blockquote>Список остальных комманд можно узнать /help </blockquote>"
        return line

    def getChatList(self, user_id):
        return database_manager.get_user_in_chat(user_id)


service = CalendarManager()
