import MySQLdb
import json

with open("config.json") as json_data:
    data = json.load(json_data)


def register(user_name, telegram_id):
    conn = MySQLdb.connect(host=data["ConnectionString"]["host"],
                           user=data["ConnectionString"]["user"],
                           password=data["ConnectionString"]["password"],
                           database=data["ConnectionString"]["database"])
    x = conn.cursor()
    try:
        x.execute(f'insert familymember(UserName, TelegramId) values ("{user_name}", "{telegram_id}")')
        conn.commit()
    except:
        conn.rollback()
    conn.close()


def add_family(params):
    conn = MySQLdb.connect(host=data["ConnectionString"]["host"],
                           user=data["ConnectionString"]["user"],
                           password=data["ConnectionString"]["password"],
                           database=data["ConnectionString"]["database"])
    x = conn.cursor()
    try:
        x.execute(f'insert family(Login, Pass, FamilyName) values ("{params[0]}", "{params[1]}", "{params[2]}" )')
        conn.commit()
    except:
        conn.rollback()
    conn.close()


def add_purchase(params):
    conn = MySQLdb.connect(host=data["ConnectionString"]["host"],
                           user=data["ConnectionString"]["user"],
                           password=data["ConnectionString"]["password"],
                           database=data["ConnectionString"]["database"])
    x = conn.cursor()
    try:
        x.execute(f'insert purchase(Login, Pass, FamilyName) values ("{params[0]}", "{params[1]}", "{params[2]}" )')
        conn.commit()
    except:
        conn.rollback()
    conn.close()
