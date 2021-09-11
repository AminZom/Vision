SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE usp_UpdateInspectionOutput
	-- Add the parameters for the stored procedure here
	@Id int,
	@PartNumber NVARCHAR(50),
	@IsDefective bit,
	@DefectType NVARCHAR(50),
	@Accuracy int,
	@PathToImage NVARCHAR(MAX)
	
AS

BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	IF EXISTS (SELECT 1 FROM dbo.InspectionOutput WHERE Id = @Id)
	BEGIN
		UPDATE dbo.InspectionOutput 
		SET PartNumber = @PartNumber, 
			IsDefective = @IsDefective,
			DefectType = @DefectType,
			Accuracy = @Accuracy,
			PathToImage = @PathToImage
		WHERE Id = @Id
	END
END
GO
