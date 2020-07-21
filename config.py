import os

class Config(object):
    SECRET_KEY=os.urandom(64)

    MONGODB_SETTINGS= {'db':'UTA_Enrollment',
        'host':'mongodb+srv://admin:admin@cluster0.wrvu8.gcp.mongodb.net/UTA_Enrollment'
    }

#?retryWrites=true&w=majority
