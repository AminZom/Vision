import pyodbc


class InspectionOutputDbConn:
    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                                   'Server=DESKTOP-SRSA7IQ\\SQLEXPRESS;'
                                   'Database=Dev_VisionInspection;'
                                   'Trusted_Connection=yes;', autocommit=True)
        self.cursor = self.conn.cursor()

    def ReadAll(self):
        query = "SELECT * FROM dbo.InspectionOutput"
        for row in self.cursor.execute(query).fetchall():
            print(row)

    def ReadById(self, id_to_read):
        query = "SELECT * FROM dbo.InspectionOutput WHERE Id = " + id_to_read
        for row in self.cursor.execute(query).fetchall():
            print(row)

    def InsertInspectionOutput(self, part_num, is_defective, defect_type, accuracy, path_to_image):
        query = "EXEC dbo.usp_InsertInspectionOutput @PartNumber=?, @IsDefective=?, @DefectType=?, @Accuracy=?, " \
                "@PathToImage=? "

        for row in self.cursor.execute(query, (part_num, is_defective, defect_type, accuracy, path_to_image)).fetchone():
            print(row)

    def UpdateInspectionOutput(self, id_to_update, part_num, is_defective, defect_type, accuracy, path_to_image):
        query = "EXEC dbo.usp_UpdateInspectionOutput @Id=?, @PartNumber=?, @IsDefective=?, @DefectType=?, " \
                "@Accuracy=?, @PathToImage=? "
        self.cursor.execute(query, id_to_update, part_num, is_defective, defect_type, accuracy, path_to_image)

    def DeleteInspectionOutput(self, id_to_delete):
        query = "EXEC dbo.usp_DeleteInspectionOutput @Id=?"
        self.cursor.execute(query, id_to_delete)

    def CloseConn(self):
        self.conn.close()


class InspectionOutputRow:
    def __init__(self, part_num, is_defective, defect_type, accuracy, path_to_image):
        self.PartNumber = part_num
        self.IsDefective = is_defective
        self.DefectType = defect_type
        self.Accuracy = accuracy
        self.PathToImage = path_to_image
