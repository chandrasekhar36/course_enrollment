import os

class Config(object):
    SECRET_KEY=os.urandom(64)

    MONGODB_SETTINGS= {'db':'UTA_Enrollment',
        'host':'mongodb://localhost:27017/UTA_Enrollment'
    }
