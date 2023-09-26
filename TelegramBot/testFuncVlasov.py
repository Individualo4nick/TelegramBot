import TelegramBot.handlers


def test_save_purchase_success():
    assert TelegramBot.handlers.get_save_purchase_status(1000) == 0


def test_save_purchase_with_negative_number():
    assert TelegramBot.handlers.get_save_purchase_status(-410401) == -1


def test_save_purchase_with_text_message():
    assert TelegramBot.handlers.get_save_purchase_status("fgaigiaigdsgsdgjksdgl") == -2


# good
def test_validate_password_success():
    assert TelegramBot.handlers.validate_password("Aboba12345") == 1


def test_validate_password_less_than_8_chars():
    assert TelegramBot.handlers.validate_password("af141") == -1


def test_validate_password_no_digits():
    assert TelegramBot.handlers.validate_password("fkafjakfajfkkafma") == -1


if __name__ == "__main__":
    test_save_purchase_success()
    test_save_purchase_with_text_message()
    test_save_purchase_with_negative_number()

    test_validate_password_no_digits()
    test_validate_password_success()
    test_validate_password_less_than_8_chars()
    print("Everything passed")
