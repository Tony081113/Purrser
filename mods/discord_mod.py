# Discord 模組
# 提供 Discord 訊息資料的存取介面

from core.interpreter import BaseModule


class DiscordModule(BaseModule):
    """
    Discord 模組
    允許腳本透過 #load 存取 Discord 訊息資料
    """
    
    def __init__(self, message_data):
        """
        初始化 Discord 模組
        :param message_data: Discord 訊息物件或包含訊息資料的字典
        """
        super().__init__("message")
        
        # 儲存訊息資料
        if isinstance(message_data, dict):
            self.data = message_data
        else:
            # 如果傳入的是物件，提取相關屬性
            self.data = {
                'username': getattr(message_data, 'username', 'unknown'),
                'id': getattr(message_data, 'id', 0)
            }
    
    def load(self, context):
        """
        載入 Discord 訊息資料到執行環境
        :param context: 執行環境上下文（變數字典）
        """
        # 將 message 物件載入到變數空間
        context['message'] = self.data


class MockDiscordMessage:
    """
    模擬 Discord 訊息物件（用於測試）
    """
    
    def __init__(self, username, message_id):
        """
        初始化模擬訊息
        :param username: 使用者名稱
        :param message_id: 訊息 ID
        """
        self.username = username
        self.id = message_id
