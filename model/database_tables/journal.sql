USE Alexandria;
GO

CREATE TABLE [dbo].[Journal] (
	Id INT IDENTITY(1,1) NOT NULL,
	[date] DATETIME NOT NULL,
	[entry] VARCHAR(300),
	PRIMARY KEY ([date])
);
GO