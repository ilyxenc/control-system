import control.db as db

username = 'admin'
password = '12345678'

db.createTableUsersWithDefault(username, password, db.admin)

db.createTableData()