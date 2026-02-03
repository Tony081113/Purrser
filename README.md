# Purrser - 文藝復興風格直譯器

Purrser 是一個以文藝復興風格設計的輕量級腳本直譯器，支援基本的運算、字串處理與模組化架構。

## 特色

- 🎨 **文藝復興風格語法**：使用 `begin;` 和 `end;` 標記腳本界限
- 📦 **模組化架構**：支援可插拔的模組系統
- 🔗 **Discord 整合**：內建 Discord 模組，可存取訊息資料
- 🇹🇼 **繁體中文註解**：所有程式碼註解皆使用繁體中文

## 安裝

```bash
git clone https://github.com/Tony081113/Purrser.git
cd Purrser
python main.py
```

## 快速開始

### 基本語法

所有 Purrser 腳本必須以 `begin;` 開始，以 `end;` 結束：

```
begin;
    x = 10;
    y = 5;
    result = x + y;
    output{result};
end;
```

### 語法特性

#### 1. 變數賦值

```
begin;
    name = "貓貓";
    age = 3;
    output{name};
end;
```

#### 2. 數字運算

支援加法與減法：

```
begin;
    a = 100;
    b = 30;
    sum = a + b;
    diff = a - b;
    output{sum};
    output{diff};
end;
```

#### 3. 字串串接

使用 `+` 運算符串接字串：

```
begin;
    greeting = "你好";
    name = "世界";
    message = greeting + "，" + name + "！";
    output{message};
end;
```

#### 4. 輸出指令

使用 `output{...}` 輸出內容：

```
begin;
    x = 42;
    output{x};
    output{"直接輸出文字"};
end;
```

#### 5. 模組載入

使用 `#load` 指令載入模組：

```
begin;
    #load message;
    output{message.username};
    output{message.id};
end;
```

## 模組系統

### 內建模組

#### Discord 模組

Discord 模組提供存取 Discord 訊息資料的介面。

**使用方式：**

```python
from core.interpreter import CatInterpreter
from mods.discord_mod import DiscordModule, MockDiscordMessage

# 建立直譯器
interpreter = CatInterpreter()

# 建立 Discord 訊息物件
message = MockDiscordMessage("使用者名稱", 123456789)

# 註冊模組
discord_mod = DiscordModule(message)
interpreter.register_module(discord_mod)

# 執行腳本
script = """
begin;
    #load message;
    greeting = "歡迎，" + message.username;
    output{greeting};
    output{message.id};
end;
"""

outputs = interpreter.execute(script)
print(outputs)
```

**可用屬性：**
- `message.username` - 使用者名稱
- `message.id` - 訊息 ID

### 開發自訂模組

#### Mod 開發指南

要建立自訂模組，請遵循以下步驟：

##### 1. 繼承 BaseModule

所有模組都必須繼承 `BaseModule` 類別：

```python
from core.interpreter import BaseModule

class MyCustomModule(BaseModule):
    def __init__(self):
        # 呼叫父類別建構子，傳入模組名稱
        super().__init__("mymodule")
        
        # 初始化模組資料
        self.data = {
            'property1': 'value1',
            'property2': 'value2'
        }
```

##### 2. 實作 load 方法

`load` 方法負責將模組資料載入到執行環境：

```python
def load(self, context):
    """
    載入模組資料到執行環境
    :param context: 執行環境上下文（變數字典）
    """
    # 將模組資料載入到變數空間
    context['mymodule'] = self.data
```

##### 3. 註冊模組

在使用前，需要將模組註冊到直譯器：

```python
from core.interpreter import CatInterpreter

interpreter = CatInterpreter()
my_module = MyCustomModule()
interpreter.register_module(my_module)
```

##### 4. 在腳本中使用

使用 `#load` 指令載入模組：

```
begin;
    #load mymodule;
    output{mymodule.property1};
    output{mymodule.property2};
end;
```

#### 完整範例：天氣模組

```python
from core.interpreter import BaseModule

class WeatherModule(BaseModule):
    """天氣資訊模組"""
    
    def __init__(self, temperature, condition):
        super().__init__("weather")
        self.data = {
            'temperature': temperature,
            'condition': condition
        }
    
    def load(self, context):
        """載入天氣資料"""
        context['weather'] = self.data

# 使用範例
interpreter = CatInterpreter()
weather_mod = WeatherModule(25, "晴天")
interpreter.register_module(weather_mod)

script = """
begin;
    #load weather;
    report = "今日天氣：" + weather.condition;
    output{report};
    output{weather.temperature};
end;
"""

outputs = interpreter.execute(script)
```

## 檔案結構

```
Purrser/
├── core/
│   ├── __init__.py
│   └── interpreter.py      # 直譯器核心
├── mods/
│   ├── __init__.py
│   └── discord_mod.py      # Discord 模組
├── main.py                 # 執行入口
├── README.md              # 說明文件
└── LICENSE
```

## API 參考

### CatInterpreter

直譯器核心類別。

#### 方法

- `__init__()` - 初始化直譯器
- `register_module(module)` - 註冊模組
- `execute(script)` - 執行腳本，回傳輸出列表

#### 例外

- `SyntaxError` - 語法錯誤
- `NameError` - 未定義的變數或屬性
- `TypeError` - 類型錯誤
- `RuntimeError` - 執行時期錯誤

### BaseModule

模組基礎類別。

#### 方法

- `__init__(name)` - 初始化模組
- `load(context)` - 載入模組資料（必須在子類別中實作）
- `get_attribute(attr_name)` - 取得模組屬性

## 授權

本專案採用 LICENSE 檔案中指定的授權條款。

## 貢獻

歡迎提交 Pull Request 或回報 Issue！

## 聯絡方式

如有任何問題或建議，請透過 GitHub Issues 聯繫我們。