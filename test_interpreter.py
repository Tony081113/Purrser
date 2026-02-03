#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purrser 直譯器測試
驗證核心功能是否正常運作
"""

import sys
import os

# 將專案根目錄加入路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.interpreter import CatInterpreter, BaseModule
from mods.discord_mod import DiscordModule, MockDiscordMessage


def test_basic_syntax():
    """測試基本語法檢查"""
    print("測試：基本語法檢查")
    
    interpreter = CatInterpreter()
    
    # 測試缺少 begin;
    try:
        interpreter.execute("x = 5; end;")
        print("  ❌ 應該拋出 SyntaxError（缺少 begin;）")
        return False
    except SyntaxError as e:
        print(f"  ✓ 正確捕獲錯誤: {e}")
    
    # 測試缺少 end;
    try:
        interpreter.execute("begin; x = 5;")
        print("  ❌ 應該拋出 SyntaxError（缺少 end;）")
        return False
    except SyntaxError as e:
        print(f"  ✓ 正確捕獲錯誤: {e}")
    
    # 測試正確語法
    try:
        interpreter.execute("begin; x = 5; end;")
        print("  ✓ 正確的語法通過")
    except Exception as e:
        print(f"  ❌ 不應該拋出錯誤: {e}")
        return False
    
    return True


def test_variable_assignment():
    """測試變數賦值"""
    print("\n測試：變數賦值")
    
    interpreter = CatInterpreter()
    
    script = """
    begin;
        x = 10;
        name = "測試";
    end;
    """
    
    interpreter.execute(script)
    
    if interpreter.variables.get('x') == 10:
        print("  ✓ 數字賦值正確")
    else:
        print(f"  ❌ 數字賦值錯誤: {interpreter.variables.get('x')}")
        return False
    
    if interpreter.variables.get('name') == "測試":
        print("  ✓ 字串賦值正確")
    else:
        print(f"  ❌ 字串賦值錯誤: {interpreter.variables.get('name')}")
        return False
    
    return True


def test_arithmetic():
    """測試算術運算"""
    print("\n測試：算術運算")
    
    interpreter = CatInterpreter()
    
    # 測試加法
    script = """
    begin;
        a = 10;
        b = 5;
        sum = a + b;
        output{sum};
    end;
    """
    
    outputs = interpreter.execute(script)
    if outputs == ['15']:
        print("  ✓ 加法運算正確")
    else:
        print(f"  ❌ 加法運算錯誤: {outputs}")
        return False
    
    # 測試減法
    interpreter2 = CatInterpreter()
    script2 = """
    begin;
        x = 100;
        y = 30;
        diff = x - y;
        output{diff};
    end;
    """
    
    outputs2 = interpreter2.execute(script2)
    if outputs2 == ['70']:
        print("  ✓ 減法運算正確")
    else:
        print(f"  ❌ 減法運算錯誤: {outputs2}")
        return False
    
    return True


def test_string_concatenation():
    """測試字串串接"""
    print("\n測試：字串串接")
    
    interpreter = CatInterpreter()
    
    script = """
    begin;
        first = "Hello";
        second = "World";
        result = first + " " + second;
        output{result};
    end;
    """
    
    outputs = interpreter.execute(script)
    if outputs == ['Hello World']:
        print("  ✓ 字串串接正確")
    else:
        print(f"  ❌ 字串串接錯誤: {outputs}")
        return False
    
    return True


def test_output():
    """測試輸出功能"""
    print("\n測試：輸出功能")
    
    interpreter = CatInterpreter()
    
    script = """
    begin;
        x = 42;
        msg = "測試訊息";
        output{x};
        output{msg};
        output{"直接輸出"};
    end;
    """
    
    outputs = interpreter.execute(script)
    expected = ['42', '測試訊息', '直接輸出']
    
    if outputs == expected:
        print("  ✓ 輸出功能正確")
    else:
        print(f"  ❌ 輸出功能錯誤: {outputs}")
        print(f"     預期: {expected}")
        return False
    
    return True


def test_discord_module():
    """測試 Discord 模組"""
    print("\n測試：Discord 模組")
    
    interpreter = CatInterpreter()
    
    # 建立並註冊模組
    message = MockDiscordMessage("測試使用者", 987654321)
    discord_mod = DiscordModule(message)
    interpreter.register_module(discord_mod)
    
    script = """
    begin;
        #load message;
        output{message.username};
        output{message.id};
    end;
    """
    
    outputs = interpreter.execute(script)
    expected = ['測試使用者', '987654321']
    
    if outputs == expected:
        print("  ✓ Discord 模組正確")
    else:
        print(f"  ❌ Discord 模組錯誤: {outputs}")
        print(f"     預期: {expected}")
        return False
    
    # 測試使用字典初始化
    interpreter2 = CatInterpreter()
    discord_mod2 = DiscordModule({'username': '字典使用者', 'id': 111111})
    interpreter2.register_module(discord_mod2)
    
    outputs2 = interpreter2.execute(script)
    expected2 = ['字典使用者', '111111']
    
    if outputs2 == expected2:
        print("  ✓ Discord 模組（字典模式）正確")
    else:
        print(f"  ❌ Discord 模組（字典模式）錯誤: {outputs2}")
        return False
    
    return True


def test_module_not_registered():
    """測試未註冊模組的錯誤處理"""
    print("\n測試：未註冊模組錯誤處理")
    
    interpreter = CatInterpreter()
    
    script = """
    begin;
        #load nonexistent;
    end;
    """
    
    try:
        interpreter.execute(script)
        print("  ❌ 應該拋出 RuntimeError")
        return False
    except RuntimeError as e:
        print(f"  ✓ 正確捕獲錯誤: {e}")
        return True


def test_custom_module():
    """測試自訂模組"""
    print("\n測試：自訂模組")
    
    class TestModule(BaseModule):
        def __init__(self):
            super().__init__("testmod")
            self.data = {
                'value1': 'Hello',
                'value2': 100
            }
        
        def load(self, context):
            context['testmod'] = self.data
    
    interpreter = CatInterpreter()
    test_mod = TestModule()
    interpreter.register_module(test_mod)
    
    script = """
    begin;
        #load testmod;
        output{testmod.value1};
        output{testmod.value2};
    end;
    """
    
    outputs = interpreter.execute(script)
    expected = ['Hello', '100']
    
    if outputs == expected:
        print("  ✓ 自訂模組正確")
    else:
        print(f"  ❌ 自訂模組錯誤: {outputs}")
        return False
    
    return True


def run_all_tests():
    """執行所有測試"""
    print("=" * 60)
    print("Purrser 直譯器測試套件")
    print("=" * 60)
    
    tests = [
        test_basic_syntax,
        test_variable_assignment,
        test_arithmetic,
        test_string_concatenation,
        test_output,
        test_discord_module,
        test_module_not_registered,
        test_custom_module
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ❌ 測試發生異常: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"測試結果：{passed} 通過，{failed} 失敗")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
