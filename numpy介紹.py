# numpy_examples.py

# 引入 NumPy 庫
import numpy as np

# -----------------------------
# 一、數組創建函式
# -----------------------------

# 1. 創建基本陣列
arr = np.array([1, 2, 3])  # 將 Python 的列表轉為 NumPy 陣列
print("基本陣列:", arr)

# 2. 創建全為 0 的陣列
zeros_arr = np.zeros((2, 3))  # 形狀為 2x3
print("全為 0 的陣列:\n", zeros_arr)

# 3. 創建全為 1 的陣列
ones_arr = np.ones((2, 3))  # 形狀為 2x3
print("全為 1 的陣列:\n", ones_arr)

# 4. 創建未初始化的陣列
empty_arr = np.empty((2, 3))  # 形狀為 2x3，內容隨機
print("未初始化的陣列:\n", empty_arr)

# 5. 生成等間距數字序列
range_arr = np.arange(0, 10, 2)  # 0 到 10，步長為 2
print("等間距數字序列:", range_arr)

# 6. 在指定範圍生成等間距數字
linspace_arr = np.linspace(0, 1, 5)  # 0 到 1，均分為 5 個數字
print("線性空間數列:", linspace_arr)

# 7. 創建單位矩陣
eye_arr = np.eye(3)  # 單位矩陣，大小為 3x3
print("單位矩陣:\n", eye_arr)

# -----------------------------
# 二、數學運算函式
# -----------------------------

# 1. 計算總和
sum_result = arr.sum()
print("陣列總和:", sum_result)

# 2. 計算均值
mean_result = arr.mean()
print("陣列均值:", mean_result)

# 3. 計算標準差
std_result = arr.std()
print("陣列標準差:", std_result)

# 4. 指數運算
exp_result = np.exp(arr)
print("指數運算結果:", exp_result)

# 5. 平方根
sqrt_result = np.sqrt(arr)
print("平方根結果:", sqrt_result)

# 6. 矩陣乘法
mat1 = np.array([[1, 2], [3, 4]])
mat2 = np.array([[5, 6], [7, 8]])
dot_result = np.dot(mat1, mat2)  # 矩陣乘法
print("矩陣乘法結果:\n", dot_result)

# -----------------------------
# 三、數據處理函式
# -----------------------------

# 1. 改變陣列形狀
reshaped_arr = np.arange(6).reshape((2, 3))  # 將形狀改為 2x3
print("重塑後的陣列:\n", reshaped_arr)

# 2. 矩陣轉置
transposed_arr = reshaped_arr.T  # 矩陣轉置
print("轉置後的陣列:\n", transposed_arr)

# 3. 排序
sorted_arr = np.sort(arr)  # 對一維陣列排序
print("排序後的陣列:", sorted_arr)

# 4. 合併多個陣列
concatenated_arr = np.concatenate((arr, arr))  # 水平合併
print("合併後的陣列:", concatenated_arr)

# 5. 找到唯一值
unique_arr = np.unique([1, 2, 2, 3])
print("唯一值陣列:", unique_arr)

# 6. 條件篩選
condition_result = np.where(arr > 2, 1, 0)  # 條件篩選，滿足條件為 1，否則為 0
print("條件篩選結果:", condition_result)

# -----------------------------
# 四、隨機數生成函式
# -----------------------------

# 1. 生成隨機數
random_arr = np.random.rand(2, 3)  # 生成 2x3 的隨機數
print("隨機數陣列:\n", random_arr)

# 2. 生成隨機整數
random_int_arr = np.random.randint(0, 10, size=(2, 3))  # 指定範圍內的隨機整數
print("隨機整數陣列:\n", random_int_arr)

# 3. 隨機選擇
choice_arr = np.random.choice([1, 2, 3, 4], size=3)  # 從列表中隨機抽取 3 個數
print("隨機選擇結果:", choice_arr)

# 4. 固定隨機種子
np.random.seed(42)
seeded_arr = np.random.rand(2, 3)
print("固定種子隨機數:\n", seeded_arr)

# -----------------------------
# 五、布林運算函式
# -----------------------------

# 1. 布林判斷 - 全部為 True
all_result = np.all(arr > 0)  # 檢查是否所有元素大於 0
print("是否全為 True:", all_result)

# 2. 布林判斷 - 至少一個為 True
any_result = np.any(arr > 2)  # 檢查是否至少一個元素大於 2
print("是否至少一個為 True:", any_result)

# 3. 邏輯運算 - AND
logical_and_result = np.logical_and([True, False], [True, True])
print("邏輯 AND 結果:", logical_and_result)

# 4. 邏輯運算 - OR
logical_or_result = np.logical_or([True, False], [True, True])
print("邏輯 OR 結果:", logical_or_result)

# -----------------------------
# 執行完成訊息
# -----------------------------
print("所有 NumPy 函式範例執行完成！")
