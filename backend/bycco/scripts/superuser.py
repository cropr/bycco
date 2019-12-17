# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

from bycco.models.md_account import AccountModel

def createsuperuser():
    ik = {
        'username': 'admin',
        'email': 'admin',
        'first_name': 'Admin',
        'last_name': '',
        'mobilephone': '',
        'password': 'Bycco2020'
    }
    acc = AccountModel.create_account(ik)
    acc.update_right('superuser')

if __name__ == '__main__':
    createsuperuser()