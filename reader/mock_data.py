import pandas as pd
from datetime import datetime
import random
import time
import pymysql
import pickle
from sqlalchemy import create_engine
import pandas as pd

readings = []

for i in range(50):
    read = []
    timestamp = datetime.now()
    posix_timestamp = int(time.mktime(timestamp.timetuple()))
    weight1 = round(random.uniform(0, 65), 3)
    weight2 = round(random.uniform(0, 65), 3)
    weight3 = round(random.uniform(0, 65), 3)
    weight4 = round(random.uniform(0, 65), 3)
    read.append(timestamp)
    read.append(posix_timestamp)
    read.append(weight1)
    read.append(weight2)
    read.append(weight3)
    read.append(weight4)
    readings.append(read)
    time.sleep(3)

with open('sampledata.pkl', 'wb') as f:
    pickle.dump(readings, f)

with open('sampledata.pkl', 'rb') as f:
    readings = pickle.load(f)

df = pd.DataFrame(readings, columns=['time_taken', 'posix', 'keg1_reading', 'keg2_reading', 'keg3_reading', 'keg4_reading'])
engine = create_engine("mysql+mysqlconnector://booz:LyTn16pf1vE0@keginstance.czdr6xoja2kz.us-east-2.rds.amazonaws.com/keg_reader")

con = engine.connect()
df.to_sql(name='keg_readings',con=con,if_exists='append')
con.close()
