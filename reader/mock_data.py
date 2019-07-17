from datetime import datetime
import random
import time
import pickle
from sqlalchemy import create_engine
import pandas as pd

readings = []
weight1 = []
weight2 = []
weight3 = []
weight4 = []

for i in range(50):

    weight1.append(round(random.uniform(0, 65), 3))
    weight2.append(round(random.uniform(0, 65), 3))
    weight3.append(round(random.uniform(0, 65), 3))
    weight4.append(round(random.uniform(0, 65), 3))

weight1 = sorted(weight1, reverse=True)
weight2 = sorted(weight2, reverse=True)
weight3 = sorted(weight3, reverse=True)
weight4 = sorted(weight4, reverse=True)

print(weight1)

for i in range(50):
    read = []

    timestamp = datetime.now()
    posix_timestamp = int(time.mktime(timestamp.timetuple()))
    read.append(timestamp)
    read.append(posix_timestamp)
    read.append(weight1[i])
    read.append(weight2[i])
    read.append(weight3[i])
    read.append(weight4[i])
    readings.append(read)
    time.sleep(3)


with open('sampledata.pkl', 'wb') as f:
    pickle.dump(readings, f)

with open('sampledata.pkl', 'rb') as f:
    readings = pickle.load(f)

df = pd.DataFrame(readings, columns=['time_taken', 'posix', 'keg1_reading', 'keg2_reading', 'keg3_reading', 'keg4_reading'])
print(df)
engine = create_engine("mysql+mysqlconnector://booz:LyTn16pf1vE0@keginstance.czdr6xoja2kz.us-east-2.rds.amazonaws.com/keg_reader")
#
con = engine.connect()
df.to_sql(name='mock_keg_readings',con=con,if_exists='replace')
con.close()
