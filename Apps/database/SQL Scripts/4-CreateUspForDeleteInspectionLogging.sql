SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE usp_DeleteInspectionOutput
	-- Add the parameters for the stored procedure here
	@Id int
	
AS

BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

	IF EXISTS (SELECT 1 FROM dbo.InspectionOutput WHERE Id = @Id)
	BEGIN
		DELETE FROM dbo.InspectionOutput 
		WHERE Id = @Id
	END
END
GO
