import MySQLdb
import json

with open("config.json") as json_data:
    data = json.load(json_data)

def connect_db():
    return MySQLdb.connect(host=data["ConnectionString"]["host"],
                           user=data["ConnectionString"]["user"],
                           password=data["ConnectionString"]["password"],
                           database=data["ConnectionString"]["database"])

def register(user_name, telegram_id):
    conn = connect_db()
    x = conn.cursor()
    try:
        x.execute(f'insert familymember(UserName, TelegramId) values ("{user_name}", "{telegram_id}")')
        conn.commit()
    except:
        conn.rollback()
    conn.close()

def check_family_login(login):
    conn = connect_db()
    x = conn.cursor()
    try:
        x.execute(f'select * from family where Login = "{login}"')
        print(x.fetchall())
        if x.fetchall() is None:
            conn.close()
            return -1
    except:
        conn.rollback()
    conn.close()
    return 0


def user_has_family(username):
    conn = connect_db()
    x = conn.cursor()
    try:
        x.execute(f'select * from familymember where TelegramId = "{username}"')
        if x.fetchall() is None:
            conn.close()
            return -1
        x.execute(f'select FamilyId from familymember where TelegramId = "{username}"')
        if "None" not in x.fetchall()[0]:
            conn.close()
            return -2
    except:
        conn.rollback()
    conn.close()
    return 0


def add_family(params, username):
    conn = connect_db()
    x = conn.cursor()
    try:

        x.execute(f'insert family(Login, Pass, FamilyName) values ("{params[0]}", "{params[1]}", "{params[2]}" )')
        conn.commit()
        x.execute(f'update familymember set FamilyId = (select Id from family where Login = "{params[0]}") where TelegramId = "{username}"')
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    return 0



def add_purchase(params):
    conn = connect_db()
    x = conn.cursor()
    try:
        x.execute(f'insert purchase(Login, Pass, FamilyName) values ("{params[0]}", "{params[1]}", "{params[2]}" )')
        conn.commit()
    except:
        conn.rollback()
    conn.close()
