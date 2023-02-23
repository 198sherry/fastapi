#import sys
#sys.path.insert(0, "C:\\Users\\Xia\\Documents\\work\\python\\onlinecourse\\PythonAPI\\app")
import pytest
from app.calculations import add, substract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def fifty_bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [(5, 3, 8), (4, 1, 5), (12, 4, 16)])
def test_add(num1, num2, expected):
    print("run test")
    assert add(num1,num2)==expected

def test_substract():
    assert substract(5,3)==2

def test_multiply():
    assert multiply(5,3)==15

def test_divide():
    assert divide(9,3)==3

def test_bank_set_initial_amount(fifty_bank_account):
#def test_bank_set_initial_amount():
    # bank_account = BankAccount(50)
    # assert bank_account.balance == 50
    assert fifty_bank_account.balance == 50

def test_bank_default_amount():
    bank_account = BankAccount()
    assert bank_account.balance == 0

# def test_withdraw():
#     bank_account = BankAccount(50)
#     bank_account.withdraw(30)
#     assert bank_account.balance == 20
def test_withdraw(fifty_bank_account):
    fifty_bank_account.withdraw(30)
    assert fifty_bank_account.balance == 20

def test_deposit():
    bank_account = BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_intrest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 1) == 55

@pytest.mark.parametrize("deposited, withdraw, expected", [(200, 100, 100), (40, 10, 30), (12, 4, 8)])
def test_bank_transaction(zero_bank_account, deposited, withdraw, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

def test_insufficient_fund(fifty_bank_account):
    with pytest.raises(InsufficientFunds):
        fifty_bank_account.withdraw(90)


