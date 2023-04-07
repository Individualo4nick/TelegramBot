"""
 This is module for database access
"""
from aifc import Error

import MySQLdb
import json


with open("../config.json") as json_data:
    data = json.load(json_data)

def connect_db():
    """
    Function for connection to our database
    :return: database connection
    """
    return MySQLdb.connect(host=data["ConnectionString"]["host"],
                           user=data["ConnectionString"]["user"],
                           password=data["ConnectionString"]["password"],
                           database=data["ConnectionString"]["database"])

def register(user_name, telegram_id):
    """
    Function for user registration
    :param user_name: how the user will be displayed in the application
    :param telegram_id: telegram id of user
    """
    conn = connect_db()
    x = conn.cursor()
    try:
        x.execute(f'insert familymember(UserName, TelegramId) values ("{user_name}", "{telegram_id}")')
        conn.commit()
    except:
        conn.rollback()
    conn.close()


def check_family_login(login):
    """
    Check for existing family account
    :param login: special name of family for authifications
    :return: -1 if family not found, 0 family founded
    """
    conn = connect_db()
    x = conn.cursor()
    try:
        x.execute(f'select * from family where Login = "{login}"')
        result = x.fetchall()
        if len(result) != 0:
            conn.close()
            return -1
    except:
        conn.rollback()
    conn.close()
    return 0


def user_has_family(username):
    """
    Сhecks the user's family status
    :param username: name of user
    :return: -1 : user has family, 0 : user without family
    """
    conn = connect_db()
    x = conn.cursor()
    try:
        x.execute(f'select * from familymember where TelegramId = "{username}"')
        result = x.fetchall()
        if not x.fetchall()[3] is None:
            conn.close()
            return -1
    except:
        conn.rollback()
    conn.close()
    return 0


def add_family(params, username):
    """
    :param params: FamilyInfo object
    :param username: telegram id of user
    :return:
    """
    conn = connect_db()
    x = conn.cursor()
    try:

        x.execute(f'insert family(Login, Pass, FamilyName) values ("{params.login}", "{params.password}", "{params.family_name}" )')
        conn.commit()
        x.execute(f'update familymember set FamilyId = (select Id from family where Login = "{params[0]}") where TelegramId = "{username}"')
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    return 0

def get_family_id(user_id):
    conn = connect_db()
    x = conn.cursor()
    try:
        x.execute(f'select FamilyId from familymember where TelegramId="{user_id}" ')
        return x.fetchall()[0]
    except:
        conn.rollback()
    conn.close()


def add_purchase(params):
    conn = connect_db()
    x = conn.cursor()
    try:
        x.execute(f'insert purchase(BuyDate, MemberId, FamilyId, BuyType, Price) values ("{params[0]}", "{params[1]}", "{params[2]}", "{params[3]}", "{params[4]}" )')
        conn.commit()
    except:
        conn.rollback()
    conn.close()

def execute_read_query(connection, query):
    """
    Executes queries to find data in the database
    :param connection: connection with db
    :param query: database query
    :return: result of query
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def get_period_members(period_name, period, family_id):
    """
    Searches information about family members who made purchases in the current month
    :param period_name: the period for which we want to get information: day, week or month
    :param period: current day, week or month
    :param family_id: id current family
    :return: family members who made purchases in the current month
    """
    conn = connect_db()
    select_spendings_member = f'select MemberId from purchase where {period_name}(BuyDate)="{period}" and FamilyId="{family_id}"'
    spendings_member = execute_read_query(conn, select_spendings_member)
    return spendings_member
def get_spend_member(period_name, period, member, family_id):
    """
    Searches for information about product categories and prices, purchases in the current period of a particular user
    :param period_name: the period for which we want to get information: day, week or month
    :param period: current day, week or month
    :param family_id: id current family
    :return: information about product categories and prices
    """
    conn = connect_db()
    select_spendings_price = f'select Price from purchase where {period_name}(BuyDate)="{period}" and MemberId="{member}" and FamilyId="{family_id}"'
    select_spendings_category = f'select BuyType from purchase where {period_name}(BuyDate)="{period}" and MemberId="{member}" and FamilyId="{family_id}"'
    spendings_price = execute_read_query(conn, select_spendings_price)
    spendings_category = execute_read_query(conn, select_spendings_category)
    return spendings_price, spendings_category
def get_spend(period_name, period, family_id):
    """
    Searches for information about product categories and prices, purchases in the current period
    :param period_name: the period for which we want to get information: day, week or month
    :param period: current day, week or month
    :param family_id: id current family
    :return: information about product categories and prices
    """
    conn = connect_db()
    select_spendings_price = f'select Price from purchase where {period_name}(BuyDate)="{period}" and FamilyId="{family_id}"'
    select_spendings_category = f'select BuyType from purchase where {period_name}(BuyDate)="{period}" and FamilyId="{family_id}"'
    spendings_price = execute_read_query(conn, select_spendings_price)
    spendings_category = execute_read_query(conn, select_spendings_category)
    return spendings_price, spendings_category