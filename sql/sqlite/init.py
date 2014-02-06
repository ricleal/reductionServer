import sqlite3

conn = sqlite3.connect(r"reduction.db")

c = conn.cursor()


# INSERT INTO t1 VALUES(NULL,123); for auto increment PK
# work with times:
# insert into TestDate (LastModifiedTime) values (datetime('now'));
# select datetime(LastModifiedTime), strftime('%s.%f', LastModifiedTime)  from TestDate;
query='''CREATE TABLE numors(
  --id INTEGER PRIMARY KEY AUTOINCREMENT,
  numor INTEGER PRIMARY KEY,
  filePath TEXT,
  lastModifiedTime DATETIME
)'''
c.execute(query)

query='''CREATE TABLE queries(
  -- id INTEGER PRIMARY KEY AUTOINCREMENT,
  queryId TEXT PRIMARY KEY,
  lastModifiedTime DATETIME,
  numor_id INTEGER,
  FOREIGN KEY(numor_id) REFERENCES numors(id)
);'''
c.execute(query)

# TODO :

# query='''CREATE TRIGGER delete_if_limit_exceeded AFTER  INSERT ON numors
# BEGIN
# 	DROP TEMPORARY TABLE IF EXISTS NEWEST_NUMORS;
# 	CREATE TEMPORARY TABLE NEWEST_NUMORS AS 
# 		select numor from numors order by lastModifiedTime desc limit 5;
# 	DROP TABLE IF EXISTS NUMORS_TO_DELETE;
# 	CREATE TEMPORARY TABLE NUMORS_TO_DELETE AS 
# 		select numor from numors where numor not in NEWEST_NUMORS;

# 	DELETE FROM queries WHERE numor IN NUMORS_TO_DELETE;
# 	DELETE FROM numors WHERE numor IN NUMORS_TO_DELETE;
# END'''
# c.execute(query)

conn.commit()

conn.close()
