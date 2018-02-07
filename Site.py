# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 19:16:08 2018

@author: skiter
"""

# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mssql+pyodbc://sskiter1:sskiter1@edw123@PRDEDWPLYW2SQL0.corporate.t-mobile.com/DM_RFDS?driver=SQL+Server+Native+Client+11.0')
connection = engine.connect()

print('Enter Site Name: ', end='')
a = input()

stmt =  """
        SELECT [SiteID]
              ,[Address]
              ,[City]
              ,[State]
              ,[Zip]
              ,[Latitude]
              ,[Longitude]
        FROM [DM_RFDS].[dbo].[Site]
        WHERE [SiteID] Like '{}'
        """.format(a)
results = connection.execute(stmt).fetchall()
site = pd.DataFrame(results)
site.columns = results[0].keys()


print(site)
a = input()