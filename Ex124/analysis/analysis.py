import pandas as pd

# Bước 0: Đọc dữ liệu từ file CSV và thêm 5 nhân viên mới
file_path = r"D:\Kĩ thuật lập trình\Ex124\dataset\employee.csv"  # Dùng 'r' để tránh lỗi escape characters
df = pd.read_csv(file_path)

# Chuyển đổi cột 'Dob' sang định dạng datetime
df['Dob'] = pd.to_datetime(df['Dob'], format='%d/%m/%Y')

# Thêm 5 nhân viên mới vào DataFrame
new_employees = pd.DataFrame({
    "Id": [5, 6, 7, 8, 9],
    "Name": ["Le Trung Nhan", "Doan Quoc Vinh", "Ngo Viet Thanh", "Bui Hoang Dieu", "Vo Tran Nha Thi"],
    "Dob": pd.to_datetime(["6/10/1995", "13/10/2000", "24/05/1998", "07/12/1999", "05/08/2002"], format='%d/%m/%Y'),
    "Role": ["Developer", "Tester", "Manager", "Analyst", "Developer"],
})

df = pd.concat([df, new_employees], ignore_index=True)

# Bước 1: Xuất toàn bộ dữ liệu ra màn hình
print("=== Tất cả nhân viên ===")
print(df)

# Bước 2: Lọc ra nhân viên KHÔNG sinh năm 2001
df_filtered = df[df['Dob'].dt.year != 2001]
print("\n=== Nhân viên không sinh năm 2001 ===")
print(df_filtered)

# Bước 3: Xuất 3 nhân viên lớn tuổi nhất (có năm sinh nhỏ nhất)
df_sorted = df.sort_values(by="Dob", ascending=True).head(3)
print("\n=== 3 nhân viên lớn tuổi nhất ===")
print(df_sorted)

# Bước 4: Lọc ra nhân viên không có vai trò 'Tester'
df_no_tester = df[df["Role"] != "Tester"]
print("\n=== Nhân viên không có vai trò Tester ===")
print(df_no_tester)

# Bước 5: Đếm số lượng nhân viên theo vai trò
role_counts = df["Role"].value_counts()
print("\n=== Số lượng nhân viên theo vai trò ===")
print(role_counts)

# Lưu kết quả vào file CSV mới
df.to_csv("updated_employee.csv", index=False)
print("\nDữ liệu đã được lưu vào 'updated_employee.csv'.")
