import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import cv2

# === 1. 輸入股票代號並取得資料 ===
stock_symbol = input("請輸入股票代號: ").strip()
input_data = yf.download(stock_symbol, start="2010-01-01", end="2024-12-01") # 因為懶得輸入 所以直接從這邊而不是使用input
input_data.reset_index(inplace=True)

# 標準化數據
scaler = MinMaxScaler()
input_data[['Open', 'High', 'Low', 'Close', 'Volume']] = scaler.fit_transform(
    input_data[['Open', 'High', 'Low', 'Close', 'Volume']]
)

# === 2. 將市場數據轉換為黑白圖像 ===

WINDOW_SIZE = 30  # 以30天數據做為預期來建構圖像
IMG_SIZE = (64, 64) #指定生成的 OHLC 圖像的大小，為 64x64 像素。

def generate_OHLC_image(data, window_size=WINDOW_SIZE, img_size=IMG_SIZE):
    # 初始化一個空的黑白圖像
    image = np.zeros(img_size, dtype=np.uint8)
    
    # 計算當前窗口內的最高價與最低價的差值，作為價格範圍。
    high_low_range = data['High'].max() - data['Low'].min()
    if high_low_range == 0:
        return None  # 避免無效的數據
    
    # 將數據標準化並縮放，使其適合圖像的縱軸範圍。
    scaled_data = ((data[['Open', 'High', 'Low', 'Close']] - data['Low'].min()) / high_low_range * (img_size[0]-1)).astype(int)
    for idx, row in scaled_data.iterrows():
        x = (idx - data.index[0]) * (img_size[1] // window_size)
        cv2.line(image, (x, img_size[0]-row['High']), (x, img_size[0]-row['Low']), 255, 1)
        cv2.line(image, (x, img_size[0]-row['Open']), (x+2, img_size[0]-row['Open']), 255, 1)
        cv2.line(image, (x, img_size[0]-row['Close']), (x+2, img_size[0]-row['Close']), 255, 1)
    
    # 轉換為 PyTorch 張量格式，適合 CNN 模型的輸入。
    return torch.tensor(image[np.newaxis, :, :], dtype=torch.float32)

# 自定義 Dataset 類
class StockImageDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# === 3. 定義 CNN 模型 ===
class CNN_Regressor(nn.Module): # 定義了一個卷積神經網路的架構，用於處理 2D 圖像數據並進行迴歸。
    def __init__(self):
        super(CNN_Regressor, self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(256 * 8 * 8, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1)  # 預測收益率
        )

    def forward(self, x):
        return self.model(x)

# === 4. 訓練模型並保存 ===
X_train, y_train = [], []

# 生成數據並過濾無效圖像
for i in range(len(input_data) - WINDOW_SIZE - 30):
    image = generate_OHLC_image(input_data.iloc[i:i+WINDOW_SIZE])
    if image is not None:  # 確保圖像有效
        X_train.append(image)
        # 標籤：30天後的收益率
        future_return = (input_data['Close'].iloc[i+WINDOW_SIZE+30] / input_data['Close'].iloc[i+WINDOW_SIZE-1]) - 1
        y_train.append(future_return)

# 將數據轉換為Tensor
X_train = torch.stack(X_train)  # 堆疊為Tensor
y_train = torch.tensor(y_train, dtype=torch.float32)  # 標籤轉為Tensor

# 創建數據集和DataLoader
train_loader = DataLoader(StockImageDataset(X_train, y_train), batch_size=32, shuffle=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = CNN_Regressor().to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0005)

# 訓練
num_epochs = int(input("請輸入訓練的次數: "))
model.train()
for epoch in range(num_epochs):
    total_loss = 0
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        optimizer.zero_grad()
        outputs = model(X_batch).squeeze()
        loss = criterion(outputs, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss/len(train_loader):.4f}")

# 保存模型參數
torch.save(model.state_dict(), "monthly_strategy_model_weights.pth", _use_new_zipfile_serialization=True)
print("模型參數已保存至 'monthly_strategy_model_weights.pth'")

# 測試加載模型參數
# 重新創建模型結構
loaded_model = CNN_Regressor().to(device)

# 加載參數
loaded_model.load_state_dict(torch.load("monthly_strategy_model_weights.pth", map_location=device))
print("模型參數已成功加載")

# 確保加載的模型可以正常運行，並可視化輸出
loaded_model.eval()
with torch.no_grad():
    # 選擇一個測試樣本
    sample_input = X_train[0].unsqueeze(0).to(device)  # 單一輸入
    prediction = loaded_model(sample_input).item()
    print(f"測試輸入的預測值: {prediction:.4f}")

    # 計算預期年化報酬率
    annualized_return = ((1 + prediction) ** 12) - 1  # 轉換為年化
    annualized_return_percentage = annualized_return * 100  # 轉換為百分比
    print(f"預期年化報酬率: {annualized_return_percentage:.2f}%")
    
    # 可視化 OHLC 圖像
    sample_image = X_train[0].squeeze().cpu().numpy()  # 從 Tensor 轉換回 NumPy
    plt.figure(figsize=(8, 6))
    plt.imshow(sample_image, cmap='gray')
    plt.title(f"OHLC Image\nPredicted Return: {annualized_return_percentage:.2f}%")
    plt.axis('off')
    plt.show()
