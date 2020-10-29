from datetime import datetime
import peewee

import cfg



database = peewee.SqliteDatabase(cfg.db_name)


# SQLite database using WAL journal mode and 64MB cache.
#db = peewee.SqliteDatabase(cfg.db_name, pragmas={'journal_mode': 'wal'})

class NSLookup(peewee.Model):
    COMPNAME = peewee.CharField(max_length=255, default="", index=True)
    DC = peewee.CharField(max_length=255, default="")
    DC_IP = peewee.CharField(max_length=255, default="")
    FQDN = peewee.CharField(max_length=255, default="", index=True)
    FQDN_IP = peewee.CharField(max_length=255, default="", index=True)
    NAME_BY_IP = peewee.CharField(max_length=255, default="")
    WARNING = peewee.CharField(max_length=255, default="")
    LASTUPDATE = peewee.DateField(default=datetime.now)

    class Meta:
        database = database
        db_table = 'nslookup'
        indexes = (
            # create a unique on ...
            #(('ID'), True),
            # create a non-unique on from/to

        )
            # (('ID', 'FQDN'), True),)



NSLookup.create_table()