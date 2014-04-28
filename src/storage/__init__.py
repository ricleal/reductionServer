from storage.storageFacade import StorageFacade
import logging

logger = logging.getLogger(__name__)

db = None
    
def getDBConnection():
    global db
    if not db: 
        db = StorageFacade()
    else:
        logger.debug("Database is already created.")
    return db

