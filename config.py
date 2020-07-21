import os

class Config(object):
    SECRET_KEY=os.urandom(64)

    MONGODB_SETTINGS= {'db':'UTA_Enrollment',
        'host':DB_URI_KEY
    }

#?retryWrites=true&w=majority
