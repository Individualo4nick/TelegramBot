"""
 This is module for database access
"""
from aifc import Error

import MySQLdb
import json
import pytest
import unittest.mock


def __init__():
    pass
####
print()
with open("./config.json") as json_data:
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
    except Exception as e:
        print(e)
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
        if result[0][3] is None:
            conn.close()
            return 0
        else :
            conn.close()
            return 1
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()
    return -1


def add_family(params, username):
    """
    Add family info to database
    :param params: FamilyInfo object
    :param username: telegram id of user
    :return:
    """
    conn = connect_db()
    x = conn.cursor()
    try:

        x.execute(f'insert family(Login, Pass, FamilyName) values ("{params.login}", "{params.password}", "{params.family_name}" )')
        conn.commit()
        x.execute(f'update familymember set FamilyId = (select Id from family where Login = "{params.login}") where TelegramId = "{username}"')
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    return 0

def get_family_id(user_id):
    """
    Search family id by user telegram id
    :param user_id: telegram id of user
    :return:
    """
    conn = connect_db()
    x = conn.cursor()
    try:
        x.execute(f'select FamilyId from familymember where TelegramId="{user_id}" ')
        return x.fetchall()[0]
    except:
        conn.rollback()
    conn.close()

def get_family_name(family_id):
    """
    Search family name by user telegram id
    :param family_id: id of family
    :return:
    """
    conn = connect_db()
    x = conn.cursor()
    try:
        x.execute(f'select FamilyName from family where Id="{family_id}"')
        return x.fetchall()[0]
    except:
        conn.rollback()
    conn.close()

def add_purchase(params):
    """
    Method to add purchase in database
    :param params: PurchaseData object
    :return:
    """
    conn = connect_db()
    x = conn.cursor()
    try:
        x.execute(f'insert purchase(BuyDate, MemberId, FamilyId, BuyType, Price) values ("{params.buy_date}", "{params.member_id}", "{params.family_id}", "{params.buy_type}", "{params.price}" )')
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


def check_family_data_to_enter(family_data, username):
    """
    Check family data from user
    """
    conn = connect_db()
    x = conn.cursor()
    try:
        family_id = x.execute(f'select Id from family where Login="{family_data.login}" and Pass="{family_data.password}" ')
        if family_id is None or family_id == 0:
            return False
        else:
            x.execute(
                f'update familymember set FamilyId = (select Id from family where Login="{family_data.login}" and Pass="{family_data.password}" ) where TelegramId = "{username}"')
            conn.commit()
            return True
    except Error as err:
        conn.rollback()
    conn.close()
    return False


def leave_family(username):
    """
    Delete foreign key about family
    :param username:
    :return:
    """
    conn = connect_db()
    x = conn.cursor()
    try:
        family_id = x.execute(
            f'select FamilyId from familymember where TelegramId="{username}"')
        if family_id is None:
            return False
        else:
            x.execute(
                f'update familymember set FamilyId = NULL where TelegramId = "{username}"')
            conn.commit()
            return True
    except Error as err:
        conn.rollback()
    conn.close()
    return False


def get_members(family_id):
    '''
    Get list of tuples (member_name, member_tg_id)
    :param family_id: family id
    :return username, nickname: username and telegram id
    '''
    conn = connect_db()
    username_req = f'select UserName from familymember where FamilyId="{family_id}"'
    nickname_req = f'select TelegramId from familymember where FamilyId="{family_id}"'
    username = [t[0] for t in execute_read_query(conn, username_req)]
    nickname = [t[0] for t in execute_read_query(conn, nickname_req)]
    return username, nickname
