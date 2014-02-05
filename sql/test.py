import sqlite3


conn = sqlite3.connect(r"reduction.db")
c = conn.cursor()

query='''insert into numors (numor,filepath,LastModifiedTime) values (1,"/tmp/123",datetime('now'))'''
c.execute(query)
query='''insert into numors (numor,filepath,LastModifiedTime) values (2,"/tmp/123",datetime('now'))'''
c.execute(query)
query='''insert into numors (numor,filepath,LastModifiedTime) values (3,"/tmp/123",datetime('now'))'''
c.execute(query)
query='''insert into numors (numor,filepath,LastModifiedTime) values (4,"/tmp/123",datetime('now'))'''
c.execute(query)
query='''insert into numors (numor,filepath,LastModifiedTime) values (5,"/tmp/123",datetime('now'))'''
c.execute(query)
query='''insert into numors (numor,filepath,LastModifiedTime) values (6,"/tmp/123",datetime('now'))'''
c.execute(query)
query='''insert into numors (numor,filepath,LastModifiedTime) values (7,"/tmp/123",datetime('now'))'''
c.execute(query)
query='''insert into numors (numor,filepath,LastModifiedTime) values (8,"/tmp/123",datetime('now'))'''
c.execute(query)
query='''insert into numors (numor,filepath,LastModifiedTime) values (9,"/tmp/123",datetime('now'))'''
c.execute(query)
query='''insert into numors (numor,filepath,LastModifiedTime) values (20,"/tmp/123",datetime('now'))'''
c.execute(query)


query='''insert into queries (queryId,numor_id,LastModifiedTime) values ("bgas121",4,datetime('now'))'''
c.execute(query)
query='''insert into queries (queryId,numor_id,LastModifiedTime) values (bgas122,3,datetime('now'))'''
c.execute(query)


conn.commit()

conn.close()

