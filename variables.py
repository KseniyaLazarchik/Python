# variables.py
import sqlserverport

# test data
server = "EPPLGDAW009A"
instance_name = "SQLEXPRESS"
driver = "{ODBC Driver 17 for SQL Server}"
#server = "EPPLGDAW009A\SQLEXPRESS"
serverspec = '{0},{1}'.format(server, sqlserverport.lookup(server, instance_name))
#server = "EPPLGDAW009A\SQLEXPRESS"
#server = "http://192.168.0.24/, 1433"
#server = "EPPLGDAW009A, 1433"
database = "TRN"
#authentication = 'ActiveDirectoryIntegrated'
username = "Lazarchik_task4"
password = "Hometask_4"
