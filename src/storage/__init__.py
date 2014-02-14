from storage.mongo import MongoDB
import logging

logger = logging.getLogger(__name__)

db = None
    
def getDBConnection():
    global db
    if not db: 
        db = MongoDB()
    else:
        logger.debug("Database is already created.")
    return db

