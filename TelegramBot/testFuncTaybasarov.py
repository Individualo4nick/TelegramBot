
import TelegramBot.handlers
import TelegramBot.db
def test_spendings_period_1(mocker):
    mocker.patch("TelegramBot.db.get_period_members", return_value=(("individualo4nick",),))
    mocker.patch("TelegramBot.db.get_spend_member", return_value=(((123,),), (('Transport',),)))
    mocker.patch("TelegramBot.db.get_spend", return_value=(((123,),), (('Transport',),)))
    assert TelegramBot.handlers.get_spending_period(1, "Month")=='''This Month you made purchases in the following categories:\n\nTransport: for the amount of 123 rubles\n\n=================================\n\nUser individualo4nick made purchases this Month in the following categories:\n\nTransport category for the amount of 123 rubles\n\n'''

def test_spendings_period_2():
    assert TelegramBot.handlers.get_spending_period(1, "Aboba")=="Unable to view information for this period"

def test_members_1(mocker):
    mocker.patch("TelegramBot.db.get_family_name", return_value=["MyFamily"])
    mocker.patch("TelegramBot.db.get_members", return_value=(['Vitaliy'], ['individualo4nick']))
    assert TelegramBot.handlers.get_members(1) =='''Family MyFamily: \nVitaliy - individualo4nick \n'''

def test_members_2(mocker):
    mocker.patch("TelegramBot.db.get_family_name", return_value=["AnotherFamily"])
    mocker.patch("TelegramBot.db.get_members", return_value=(['Vitaliy', 'Vlad'], ['individualo4nick', 'sinforge']))
    assert TelegramBot.handlers.get_members(1) == '''Family AnotherFamily: \nVitaliy - individualo4nick \nVlad - sinforge \n'''

if __name__ == "__main__":
    test_spendings_period_1()
    test_spendings_period_2()
    test_members_1()
    test_members_2()
    print("Everything passed")