
import sys
import pandas as pd


if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def stage_1_inspect_data():
    print("=" * 60)
    print("STAGE 1: KHÁM NGHIỆM DỮ LIỆU BAN ĐẦU (INSPECT DATA)")
    print("=" * 60)

    orders = pd.read_csv("data/orders.csv")
    products = pd.read_csv("data/products.csv")  
    customers = pd.read_csv("data/customers.csv")

    print(f"[*] Kích thước orders: {orders.shape} (gồm {orders.shape[0]} dòng, {orders.shape[1]} cột)")

    print("\n[*] 3 dòng đầu của orders (head):")
    print(orders.head(3))

    print("\n[*] 2 dòng cuối của orders (tail):")
    print(orders.tail(2))

    print("\n[*] Danh sách các cột:", list(orders.columns)) 
    print("\n[*] Kiểu dữ liệu từng cột (.dtypes):")
    print(orders.dtypes)

    print("\n[*] Chụp X-Quang dữ liệu (.info()):")
    orders.info()

    print("\n[*] Thống kê mô tả các cột số (.describe()):")
    print(orders.describe())

    return orders, products, customers


def stage_2_select_and_filter(orders):
    print("\n" + "=" * 60)
    print("STAGE 2: CHỌN CỘT VÀ LỌC DỮ LIỆU (SELECT & FILTER)")
    print("=" * 60)

    price_series = orders["unit_price"]
    sub_df = orders[["order_id", "product_id", "quantity"]]

    print(f"[*] Chọn 1 cột (Series, type={type(price_series).__name__}): 3 phần tử đầu:\n{price_series.head(3)}")

    print(f"\n[*] Chọn nhiều cột (DataFrame, shape={sub_df.shape}):\n{sub_df.head(2)}")

    print("\n[*] .loc: Lấy dòng index 0 đến 2, cột 'order_id' và 'quantity':")
    print(orders.loc[0:2, ["order_id", "quantity"]])


    print("\n[*] .iloc: Lấy 2 dòng đầu, 3 cột đầu:")
    print(orders.iloc[0:2, 0:3])
 
    mask_high_qty = orders["quantity"] >= 3
    print(f"\n[*] Mặt nạ Boolean (Series kiểu bool):\n{mask_high_qty.head(3)}")
     
    high_qty_orders = orders[mask_high_qty]
    print(f"\n[*] Các đơn hàng có số lượng >= 3 (có {len(high_qty_orders)} dòng):")
    print(high_qty_orders.head(3))

    complex_filter = orders[(orders["quantity"] >= 2) & (orders["unit_price"] >= 100.0)]
    print(f"\n[*] Đơn hàng số lượng >= 2 VÀ đơn giá >= 100 ({len(complex_filter)} dòng):")
    print(complex_filter.head(3))

    sorted_orders = orders.sort_values(by="unit_price", ascending=False)
    print("\n[*] Top 3 đơn hàng có đơn giá cao nhất:")
    print(sorted_orders[["order_id", "product_id", "unit_price"]].head(3))

    return orders

def stage_3_calculate(orders):
    print("\n" + "=" * 60)
    print("STAGE 3: TÍNH TOÁN & TẠO CỘT MỚI (CALCULATE & DERIVE)")
    print("=" * 60)

    orders["gross_revenue"] = orders["quantity"] * orders["unit_price"]
    print("[*] 5 dòng đầu sau khi tạo cột mới 'gross_revenue':")
    print(orders[["order_id", "quantity", "unit_price", "gross_revenue"]].head())

    total_revenue = orders["gross_revenue"].sum()
    avg_price = orders["unit_price"].mean()
    max_qty = orders["quantity"].max()
    min_qty = orders["quantity"].min()

    print(f"\n[*] Tổng doanh thu sơ bộ: {total_revenue:,.2f}")
    print(f"[*] Đơn giá trung bình: {avg_price:,.2f}")
    print(f"[*] Số lượng lớn nhất: {max_qty}, nhỏ nhất: {min_qty}")

    print("\n[*] Tần suất xuất hiện của từng sản phẩm trong các đơn hàng:")
    print(orders["product_id"].value_counts())

    return orders


def stage_4_group_and_aggregate(orders):
    print("\n" + "=" * 60)
    print("STAGE 4: GOM NHÓM VÀ TỔNG HỢP (GROUPBY & AGGREGATE)")
    print("=" * 60)

    prod_rev = orders.groupby("product_id")["gross_revenue"].sum()
    print("[*] Doanh thu theo từng mã sản phẩm (Series có index là product_id):")
    print(prod_rev)


    prod_summary = orders.groupby("product_id").agg(
        total_revenue=("gross_revenue", "sum"),
        avg_revenue=("gross_revenue", "mean"),
        order_count=("order_id", "count")
    ).reset_index()  

    prod_summary = prod_summary.sort_values(by="total_revenue", ascending=False)
    print("\n[*] Bảng tổng hợp hiệu suất từng sản phẩm (đã sắp xếp giảm dần):")
    print(prod_summary)

    return prod_summary


def stage_5_merge_tables(orders, products, customers):
    print("\n" + "=" * 60)
    print("STAGE 5: GHÉP NỐI BẢNG (MERGE / JOINS)")
    print("=" * 60)

    print(f"[*] Số dòng trước khi merge: orders={len(orders)}, products={len(products)}")
    
    orders_with_prod = pd.merge(
        left=orders,
        right=products,
        on="product_id",
        how="left"
    )


    print(f"[*] Số dòng sau khi merge với products: {len(orders_with_prod)}")
    print(orders_with_prod[["order_id", "product_id", "product_name", "category", "unit_price"]].head(6))

    full_df = pd.merge(
        left=orders_with_prod,
        right=customers,
        on="customer_id",
        how="left"
    )

    print(f"\n[*] Bảng hợp nhất đầy đủ thông tin (shape: {full_df.shape}):")
    print(full_df[["order_id", "customer_name", "region", "product_name", "gross_revenue"]].head(10))

    region_revenue = full_df.groupby("region")["gross_revenue"].sum().reset_index()
    print("\n[*] Tổng doanh thu theo từng Vùng miền (Region):")
    print(region_revenue)

    return full_df


def stage_6_clean_data(full_df):
    print("\n" + "=" * 60)
    print("STAGE 6: LÀM SẠCH VÀ KIỂM SOÁT DỮ LIỆU (DATA CLEANING)")
    print("=" * 60)

    print("[*] Số lượng ô bị thiếu (NaN) trên từng cột:")
    print(full_df.isna().sum())

    dup_count = full_df.duplicated(subset=["order_id"]).sum()
    print(f"\n[*] Số lượng đơn hàng bị trùng lặp order_id: {dup_count}")
    
    clean_df = full_df.drop_duplicates(subset=["order_id"], keep="first").copy()
    print(f"[*] Số dòng sau khi xóa trùng: {len(clean_df)}")

    clean_df["order_date_clean"] = pd.to_datetime(clean_df["order_date"], errors="coerce")

    invalid_dates = clean_df[clean_df["order_date_clean"].isna()]
    print(f"\n[*] Các đơn hàng có ngày không hợp lệ (bị ép thành NaT):\n{invalid_dates[['order_id', 'order_date']]}")

    invalid_qty = clean_df[clean_df["quantity"] <= 0]
    print(f"\n[*] Đơn hàng có số lượng vô lý (<= 0):\n{invalid_qty[['order_id', 'quantity']]}")
    
    valid_sales = clean_df[(clean_df["quantity"] > 0) & (clean_df["quantity"].notna())].copy()
    print(f"[*] Số đơn hàng hợp lệ cuối cùng: {len(valid_sales)}")

    return valid_sales


def stage_7_capstone_report(valid_sales):
    print("\n" + "=" * 60)
    print("STAGE 7: BÁO CÁO KINH DOANH TỔNG HỢP (CAPSTONE REPORT)")
    print("=" * 60)

    valid_sales["gross_revenue"] = valid_sales["quantity"] * valid_sales["unit_price"]

    total_rev = valid_sales["gross_revenue"].sum()
    print(f"1. TỔNG DOANH THU THỰC TẾ: {total_rev:,.2f} USD")

    cat_summary = valid_sales.groupby("category")["gross_revenue"].sum().sort_values(ascending=False)
    print(f"\n2. DOANH THU THEO DANH MỤC:\n{cat_summary}")

    reg_summary = valid_sales.groupby("region")["gross_revenue"].sum().sort_values(ascending=False)
    print(f"\n3. HIỆU SUẤT KHU VỰC:\n{reg_summary}")

    valid_sales["month"] = valid_sales["order_date_clean"].dt.to_period("M")
    valid_sales["year"] = valid_sales["order_date_clean"].dt.to_period("Y")

    yearly_rev = valid_sales.groupby("month")["gross_revenue"].sum()
    monthly_rev = valid_sales.groupby("month")["gross_revenue"].sum()

    print(f"\n4. XU HƯỚNG DOANH THU THEO THÁNG:\n{monthly_rev}")
    print(f"\n4.1 XH PHÁT TRIỂN THEO NĂM: \n {yearly_rev}") 

    print("\n" + "=" * 60)
    print("HOÀN THÀNH QUY TRÌNH PHÂN TÍCH SALES DATA ANALYZER!")
    print("=" * 60)


if __name__ == "__main__":
    orders_df, products_df, customers_df = stage_1_inspect_data()
    orders_df = stage_2_select_and_filter(orders_df)
    orders_df = stage_3_calculate(orders_df)
    stage_4_group_and_aggregate(orders_df)
    full_df = stage_5_merge_tables(orders_df, products_df, customers_df)
    clean_df = stage_6_clean_data(full_df)
    stage_7_capstone_report(clean_df)
