# pandas_examples.py

# 引入 pandas 模組
import pandas as pd

# -----------------------------
# 一、Pandas 的基本結構
# -----------------------------

# 1. 創建 Series（一維數據結構，類似帶索引的列表）
series = pd.Series([1, 2, 3], index=['a', 'b', 'c'])  # 自訂索引
print("Series 範例:\n", series)

# 2. 創建 DataFrame（表格結構，類似 Excel）
data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}  # 資料來源
df = pd.DataFrame(data)  # 使用字典創建 DataFrame
print("\nDataFrame 範例:\n", df)

# -----------------------------
# 二、數據載入與儲存
# -----------------------------

# 1. 載入 CSV 文件（需替換為實際文件路徑）
# df = pd.read_csv('data.csv')
# print("\n載入 CSV 文件:\n", df)

# 2. 儲存為 CSV 文件
df.to_csv('output.csv', index=False)  # 不包含索引
print("\n已將 DataFrame 儲存為 output.csv")

# -----------------------------
# 三、數據查看與探索
# -----------------------------

# 查看數據
print("\n數據的前 5 行:\n", df.head())  # 預設顯示前 5 行
print("\n數據的統計摘要:\n", df.describe())  # 基本統計信息
print("\n數據結構信息:")
print(df.info())  # 數據類型和非空值數量

# 選擇列和行
print("\n選擇 'Name' 列:\n", df['Name'])  # 獲取單列
print("\n選擇第 0 行:\n", df.loc[0])  # 使用標籤索引選擇
print("\n選擇第 0 行第 1 列的值:\n", df.iloc[0, 1])  # 使用位置索引

# -----------------------------
# 四、數據操作
# -----------------------------

# 1. 篩選數據（年齡大於 30）
filtered_df = df[df['Age'] > 30]
print("\n篩選年齡大於 30 的數據:\n", filtered_df)

# 2. 新增列
df['Salary'] = [50000, 60000, 70000]  # 添加工資列
print("\n新增 'Salary' 列:\n", df)

# 3. 修改數據
df.loc[0, 'Age'] = 26  # 修改第一行的年齡
print("\n修改後的 DataFrame:\n", df)

# 4. 刪除行或列
df = df.drop('Salary', axis=1)  # 刪除 'Salary' 列
print("\n刪除 'Salary' 列後的 DataFrame:\n", df)

# -----------------------------
# 五、缺失值處理
# -----------------------------

# 模擬含缺失值的 DataFrame
df_with_nan = pd.DataFrame({'Name': ['Alice', 'Bob', None], 'Age': [25, None, 35]})
print("\n含缺失值的 DataFrame:\n", df_with_nan)

# 檢查缺失值
print("\n檢查缺失值:\n", df_with_nan.isnull())
print("\n每列缺失值數量:\n", df_with_nan.isnull().sum())

# 填補缺失值
df_with_nan['Age'].fillna(30, inplace=True)  # 填補年齡的缺失值
print("\n填補缺失值後的 DataFrame:\n", df_with_nan)

# 刪除含缺失值的行
df_no_nan = df_with_nan.dropna()
print("\n刪除含缺失值行後的 DataFrame:\n", df_no_nan)

# -----------------------------
# 六、資料聚合與分組
# -----------------------------

# 按 "Name" 分組並計算年齡平均值
grouped = df.groupby('Name')['Age'].mean()
print("\n按 'Name' 分組的年齡平均值:\n", grouped)

# 使用多重聚合函式
agg_result = df.groupby('Name').agg({'Age': 'mean'})
print("\n多重聚合結果:\n", agg_result)

# -----------------------------
# 七、數據合併
# -----------------------------

# 創建 DataFrame 進行合併
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'C': [5, 6], 'D': [7, 8]})

# 水平合併
merged_horizontally = pd.concat([df1, df2], axis=1)
print("\n水平合併結果:\n", merged_horizontally)

# 垂直合併
merged_vertically = pd.concat([df1, df2], axis=0)
print("\n垂直合併結果:\n", merged_vertically)

# -----------------------------
# 執行完成訊息
# -----------------------------
print("\n所有 Pandas 功能範例執行完成！")
