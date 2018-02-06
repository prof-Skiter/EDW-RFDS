SELECT SL.SiteID
	  ,AL.SiteLayoutName
	  ,ST.StatusTypeName
	  ,SEC.SectorName
	  ,AD.Azimuth
	  ,AD.AntennaPosition
FROM [DM_RFDS].[dbo].[SiteLayout] AS SL
LEFT JOIN [DM_RFDS].[dbo].[SiteLayout] AS AL ON AL.SiteLayoutID = SL.ALConfig_SiteLayoutID
LEFT JOIN [DM_RFDS].[dbo].[StatusType] AS ST ON ST.StatusTypeID = SL.StatusTypeID
LEFT JOIN [DM_RFDS].[dbo].[SiteLayout_SectorLayout] AS SSL ON SL.[SiteLayoutID] = SSL.[SiteLayoutID]
LEFT JOIN [DM_RFDS].[dbo].[SectorLayout] AS SEC ON SEC.SectorLayoutID = SSL.SectorLayoutID
LEFT JOIN [DM_RFDS].[dbo].[AntennaDetail] AS AD ON SSL.SectorLayoutID = AD.SectorLayoutID
WHERE SL.[SiteID] Like 'AU01556A' AND AL.SiteLayoutName Like '761P_RUSq_No U2100' AND ST.StatusTypeName Like 'Live'
ORDER BY AL.SiteLayoutName