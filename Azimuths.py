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

# GET RMOD
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
        WHERE SL.SiteID Like 'AU01556A' AND AL.SiteLayoutName Like '761P_RUSq_No U2100' AND ST.StatusTypeName Like 'Live'
        """
results = connection.execute(stmt).fetchall()
AZ = pd.DataFrame(results)
AZ.columns = results[0].keys()
AZ.Azimuth = AZ.Azimuth.astype(int)
tmp = AZ.groupby('SectorName')['Azimuth'].apply(lambda x: "%s" % str(set(x)).strip("{}"))
Azimuths = ''
for i in tmp:
    Azimuths = Azimuths + i + '/'

print(Azimuths)

