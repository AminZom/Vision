USE [Dev_VisionInspection]
GO

/****** Object:  Table [dbo].[InspectionOutput]    Script Date: 2021-09-11 3:05:08 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[InspectionOutput](
	[Id] [int] NOT NULL IDENTITY,
	[PartNumber] [nvarchar](50) NOT NULL,
	[IsDefective] [bit] NOT NULL,
	[DefectType] [nvarchar](50) NULL,
	[Accuracy] [int] NULL,
	[PathToImage] [nvarchar](max) NULL,
	[CreatedAt] [datetime] NULL,
 CONSTRAINT [PK_InspectionOutput] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


