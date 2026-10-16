import pandas as pd

orders_df = pd.read_csv("data/orders.csv")

print("=== KÍCH THƯỚC BẢNG ===")
print("Shape:", orders_df.shape)

print("\n=== 5 DÒNG ĐẦU TIÊN ===")
print(orders_df.head())