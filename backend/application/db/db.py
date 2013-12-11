import psycopg2

class Db:
    __conn = None
    __settings = {
        'host'     : '10.14.212.108',
        'dbname'   : 'version_hub',
        'user'     : 'version_hub_user',
        'password' : 'Eur0pa42!'
    }

    @staticmethod
    def connect():
        if Db.__conn is None:
            #Db.__conn = psycopg2.connect(Db.dsn())
            print(Db.__settings)
            Db.__conn = psycopg2.connect(**Db.__settings)

        return Db.__conn.cursor()

    @staticmethod
    def dsn():
        return '"' + ' '.join([k+'='+v for k,v in Db.__settings.items()]) + '"'

