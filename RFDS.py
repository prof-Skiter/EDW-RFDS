# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:36:53 2018

@author: skiter
"""

from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mssql+pyodbc://sskiter1:sskiter1@edw123@PRDEDWPLYW2SQL0.corporate.t-mobile.com/DM_RFDS?driver=SQL+Server+Native+Client+11.0')
connection = engine.connect()

print('Enter Site Name: ', end='')
site = input()

stmt =  """
        SELECT SL.SiteID
	         ,AL.SiteLayoutName
	         ,ST.StatusTypeName
	         ,SEC.SectorName
	         ,AD.Azimuth
	         ,AD.AntennaPosition
        FROM SiteLayout AS SL
        LEFT JOIN SiteLayout AS AL ON AL.SiteLayoutID = SL.ALConfig_SiteLayoutID
        LEFT JOIN StatusType AS ST ON ST.StatusTypeID = SL.StatusTypeID
        LEFT JOIN SiteLayout_SectorLayout AS SSL ON SL.SiteLayoutID = SSL.SiteLayoutID
        LEFT JOIN SectorLayout AS SEC ON SEC.SectorLayoutID = SSL.SectorLayoutID
        LEFT JOIN AntennaDetail AS AD ON SSL.SectorLayoutID = AD.SectorLayoutID
        WHERE SL.SiteID Like '{}'
        """.format(site)
results = connection.execute(stmt).fetchall()
AZ = pd.DataFrame(results)
AZ.columns = results[0].keys()
AZ.Azimuth = AZ.Azimuth.astype(int)

config = AZ[['SiteLayoutName']].drop_duplicates().reset_index(drop=True)
choice = {i:config.SiteLayoutName[i] for i in range(len(config))}
print('Choose config:')
for i in range(len(choice)):
    print(i,': ',choice[i])
a = input()
AZ = AZ[AZ['SiteLayoutName'] == config.SiteLayoutName[int(a)]]

status = AZ[['StatusTypeName']].drop_duplicates().reset_index(drop=True)
choice = {i:status.StatusTypeName[i] for i in range(len(status))}
print('Choose status:')
for i in range(len(choice)):
    print(i,': ',choice[i])
a = input()
AZ = AZ[AZ['StatusTypeName'] == status.StatusTypeName[int(a)]]

tmp = AZ.groupby('SectorName')['Azimuth'].apply(lambda x: "%s" % str(set(x)).strip("{}"))
Azimuths = ''
for i in tmp:
    Azimuths = Azimuths + i + '/'

print('Azimuths: ', Azimuths)

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
        """.format(site)
results = connection.execute(stmt).fetchall()
site = pd.DataFrame(results)
site.columns = results[0].keys()

print(site)

a = input()