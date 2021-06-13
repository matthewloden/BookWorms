import datetime as dt
import pandas as pd
from sqlalchemy import create_engine, text
import json
import logging
#from app import logging

try:
    with open('app/config/config.json') as f:
        data = json.load(f)
        host = data["dbconfiginfo"]["host"] 
        dbname = data["dbconfiginfo"]["dbname"] 
        schema = data["dbconfiginfo"]["schema"]
        username = data["dbconfiginfo"]["username"]
        password = data["dbconfiginfo"]["password"]
        port = data["dbconfiginfo"]["port"]

    def connection_pgsql(schema,username,password,port,host,db):
        schema = schema
        engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(username, password,host,port,dbname))
        logging.info("Successful postgreSQL DB connection.")
        return engine,schema


    # Creating SQLAlchemy engine and schema objects
    engine,schema= connection_pgsql(schema,username,password,port,host,dbname) #engine, schema are global vars



    # Registering users
    def reg_user(email, name, pword, age):
        with engine.connect() as conn:
            logging.info("Registering the user")
            # Getting the idnum for the new user
            sql_query="SELECT * FROM dev.users;"
            df_users = pd.read_sql(sql_query,conn)
            if(len(df_users["userID"]) > 0):
                idnum = max([user for user in df_users["userID"]]) + 1
            else:
                idnum = 0
            # Inserting user information into table
            conn.execute("INSERT INTO dev.users VALUES (%s, %s, %s, %s, %s);",
            (email, name, pword, age, idnum))
    
    # Read all registered users
    def read_users():
        with engine.connect() as conn:
            logging.info("Getting users that have not been enabled")
            sql_query2="SELECT * FROM dev.users;"  #
            users = pd.read_sql(sql_query2,conn)
            return users
        
    # Insert into book recs table

    # Insert entry to dashboard information table. note must be enduser email.

    # Reading the book recs
   

except Exception as e:
   # logging.error(str(e))
   print(e)
