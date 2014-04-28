# Shell
mysql -u root -p

# MySQL prompt
# Create DB and user for the db
create database reductiondb;
grant usage on *.* to testuser@localhost identified by 'testpassword';
grant all privileges on reductiondb.* to testuser@localhost ;

# Shell
# connect to the db as testuser
mysql -u testuser -p'testpassword' reductiondb

# MySQL prompt
source schema.sql

