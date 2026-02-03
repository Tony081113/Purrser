# 文藝復興風格直譯器核心
import re


class BaseModule:
    """
    模組基礎類別
    所有模組都應該繼承此類別並實作必要的方法
    """
    
    def __init__(self, name):
        """
        初始化模組
        :param name: 模組名稱
        """
        self.name = name
        self.data = {}
    
    def load(self, context):
        """
        載入模組資料到執行環境
        :param context: 執行環境上下文
        """
        raise NotImplementedError("子類別必須實作 load 方法")
    
    def get_attribute(self, attr_name):
        """
        取得模組屬性
        :param attr_name: 屬性名稱
        :return: 屬性值
        """
        return self.data.get(attr_name, None)


class CatInterpreter:
    """
    文藝復興風格的 Cat 直譯器
    支援變數賦值、基礎運算、字串串接與輸出功能
    """
    
    def __init__(self):
        """初始化直譯器"""
        self.variables = {}  # 儲存變數
        self.modules = {}    # 儲存已載入的模組
        self.output_buffer = []  # 儲存輸出內容
    
    def register_module(self, module):
        """
        註冊模組到直譯器
        :param module: BaseModule 實例
        """
        self.modules[module.name] = module
    
    def execute(self, script):
        """
        執行腳本
        :param script: 腳本內容
        :return: 執行結果（輸出列表）
        """
        # 清空輸出緩衝區
        self.output_buffer = []
        
        # 移除多餘空白並分割行
        script = script.strip()
        
        # 嚴格檢查腳本開頭與結尾
        if not script.startswith('begin;'):
            raise SyntaxError("腳本必須以 'begin;' 開始")
        
        if not script.endswith('end;'):
            raise SyntaxError("腳本必須以 'end;' 結束")
        
        # 移除 begin; 和 end;
        script = script[6:-4].strip()
        
        # 解析並執行每一行
        lines = script.split(';')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            self._execute_line(line)
        
        return self.output_buffer
    
    def _execute_line(self, line):
        """
        執行單一行指令
        :param line: 指令行
        """
        # 處理 #load 指令
        if line.startswith('#load'):
            self._handle_load(line)
        # 處理 output 指令
        elif line.startswith('output{') and line.endswith('}'):
            self._handle_output(line)
        # 處理變數賦值
        elif '=' in line:
            self._handle_assignment(line)
        else:
            raise SyntaxError(f"無法解析的指令: {line}")
    
    def _handle_load(self, line):
        """
        處理模組載入指令
        :param line: #load <module_name>
        """
        match = re.match(r'#load\s+(\w+)', line)
        if not match:
            raise SyntaxError(f"無效的 #load 語法: {line}")
        
        module_name = match.group(1)
        if module_name not in self.modules:
            raise RuntimeError(f"模組 '{module_name}' 未註冊")
        
        # 載入模組資料到變數空間
        module = self.modules[module_name]
        module.load(self.variables)
    
    def _handle_output(self, line):
        """
        處理輸出指令
        :param line: output{expression}
        """
        # 提取大括號內的表達式
        expr = line[7:-1]
        result = self._evaluate_expression(expr)
        self.output_buffer.append(str(result))
    
    def _handle_assignment(self, line):
        """
        處理變數賦值
        :param line: variable = expression
        """
        parts = line.split('=', 1)
        if len(parts) != 2:
            raise SyntaxError(f"無效的賦值語句: {line}")
        
        var_name = parts[0].strip()
        expr = parts[1].strip()
        
        # 驗證變數名稱（只允許字母、數字、底線和點號）
        if not re.match(r'^[\w.]+$', var_name):
            raise SyntaxError(f"無效的變數名稱: {var_name}")
        
        # 計算表達式並賦值
        value = self._evaluate_expression(expr)
        self.variables[var_name] = value
    
    def _evaluate_expression(self, expr):
        """
        計算表達式
        支援：數字、字串、變數、加法、減法
        :param expr: 表達式
        :return: 計算結果
        """
        expr = expr.strip()
        
        # 處理字串字面值
        if (expr.startswith('"') and expr.endswith('"')) or \
           (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        
        # 處理數字
        if expr.isdigit() or (expr.startswith('-') and expr[1:].isdigit()):
            return int(expr)
        
        # 處理加法運算
        if '+' in expr:
            parts = expr.split('+')
            result = self._evaluate_expression(parts[0].strip())
            for part in parts[1:]:
                right = self._evaluate_expression(part.strip())
                # 字串串接或數字相加
                if isinstance(result, str) or isinstance(right, str):
                    result = str(result) + str(right)
                else:
                    result = result + right
            return result
        
        # 處理減法運算（僅數字）
        if '-' in expr and not expr.startswith('-'):
            parts = expr.split('-')
            result = self._evaluate_expression(parts[0].strip())
            for part in parts[1:]:
                right = self._evaluate_expression(part.strip())
                if not isinstance(result, int) or not isinstance(right, int):
                    raise TypeError("減法運算僅支援數字")
                result = result - right
            return result
        
        # 處理變數或屬性存取
        if '.' in expr:
            # 屬性存取 (例如: message.username)
            parts = expr.split('.')
            if len(parts) == 2:
                obj_name = parts[0]
                attr_name = parts[1]
                if obj_name in self.variables:
                    obj = self.variables[obj_name]
                    if isinstance(obj, dict) and attr_name in obj:
                        return obj[attr_name]
                    # 如果物件是模組，嘗試取得其屬性
                    elif hasattr(obj, attr_name):
                        return getattr(obj, attr_name)
                raise NameError(f"找不到屬性: {expr}")
        
        # 處理簡單變數
        if expr in self.variables:
            return self.variables[expr]
        
        raise NameError(f"未定義的變數: {expr}")
