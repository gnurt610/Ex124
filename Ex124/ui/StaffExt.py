import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from StaffManagementMainWindow import Ui_StaffManagementMainWindow

class StaffManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_StaffManagementMainWindow()
        self.ui.setupUi(self)

        # Kết nối các nút với chức năng
        self.ui.pushButtonSaveStaff.clicked.connect(self.add_employee)
        self.ui.pushButtonDelete.clicked.connect(self.delete_employee)
        self.ui.pushButtonSort.clicked.connect(self.sort_employees)
        self.ui.pushButtonCount.clicked.connect(self.count_roles)
        self.ui.pushButtonTop3.clicked.connect(self.show_oldest_employees)
        self.ui.pushButtonCount_2.clicked.connect(self.show_all_employees)  # Nút hiển thị toàn bộ nhân viên

        # Đọc dữ liệu từ file CSV (hoặc tạo DataFrame nếu không có file)
        self.file_path = "employees.csv"
        try:
            self.df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=["ID", "Name", "Dob", "Role"])

        # Hiển thị toàn bộ nhân viên khi mở ứng dụng
        self.show_all_employees()

    def load_table(self, data):
        """ Hiển thị dữ liệu lên QTableWidget """
        self.ui.tableWidgetEmployee.setRowCount(len(data))
        self.ui.tableWidgetEmployee.setColumnCount(len(data.columns))
        self.ui.tableWidgetEmployee.setHorizontalHeaderLabels(data.columns)

        for row, rowData in enumerate(data.values):
            for col, value in enumerate(rowData):
                self.ui.tableWidgetEmployee.setItem(row, col, QTableWidgetItem(str(value)))

    def show_all_employees(self):
        """ Hiển thị toàn bộ nhân viên """
        self.load_table(self.df)

    def add_employee(self):
        """ Thêm nhân viên mới từ LineEdit """
        emp_id = self.ui.lineEditEmployeeID.text()
        name = self.ui.lineEditEmployeeName.text()
        dob = self.ui.lineEditDob.text()
        role = self.ui.lineEditRole.text()

        if not emp_id or not name or not dob or not role:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin nhân viên.")
            return

        if emp_id in self.df["ID"].astype(str).values:
            QMessageBox.warning(self, "Lỗi", "ID đã tồn tại.")
            return

        new_employee = pd.DataFrame([[emp_id, name, dob, role]], columns=self.df.columns)
        self.df = pd.concat([self.df, new_employee], ignore_index=True)

        self.show_all_employees()
        QMessageBox.information(self, "Thành công", "Nhân viên đã được thêm.")
        self.save_data()

    def delete_employee(self):
        """ Xóa nhân viên dựa vào ID """
        emp_id = self.ui.lineEditEmployeeID.text()
        if emp_id not in self.df["ID"].astype(str).values:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy nhân viên.")
            return

        self.df = self.df[self.df["ID"].astype(str) != emp_id]
        self.show_all_employees()
        QMessageBox.information(self, "Thành công", "Nhân viên đã được xóa.")
        self.save_data()

    def sort_employees(self):
        """ Sắp xếp nhân viên theo ID """
        self.df = self.df.sort_values(by="ID", ascending=True)
        self.show_all_employees()

    def count_roles(self):
        """ Đếm số lượng nhân viên theo vai trò """
        role_counts = self.df["Role"].value_counts().reset_index()
        role_counts.columns = ["Role", "Count"]
        self.load_table(role_counts)

    def show_oldest_employees(self):
        """ Xuất 3 nhân viên lớn tuổi nhất """
        self.df["Dob"] = pd.to_datetime(self.df["Dob"], errors='coerce')
        sorted_df = self.df.sort_values(by="Dob", ascending=True).head(3)
        self.load_table(sorted_df)

    def save_data(self):
        """ Lưu dữ liệu vào file CSV """
        self.df.to_csv(self.file_path, index=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StaffManagementApp()
    window.show()
    sys.exit(app.exec())
