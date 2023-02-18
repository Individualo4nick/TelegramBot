import MySQLdb


def add_family(params):
    # TO DO : put connection data in confi
    conn = MySQLdb.connect(host="localhost", user="root",
                           password="Vladik_1", database="telegrambot")
    x = conn.cursor()
    try:
        x.execute(f'insert family(Login, Pass, FamilyName) values ("{params[0]}", "{params[1]}", "{params[2]}" )')
        conn.commit()
    except:
        conn.rollback()
    conn.close()