#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purrser - 文藝復興風格的直譯器
主程式入口
"""

from core.interpreter import CatInterpreter
from mods.discord_mod import DiscordModule, MockDiscordMessage


def main():
    """主程式入口"""
    
    print("=== Purrser 文藝復興風格直譯器 ===\n")
    
    # 建立直譯器實例
    interpreter = CatInterpreter()
    
    # 範例 1: 基本運算與輸出
    print("範例 1: 基本運算與輸出")
    script1 = """
    begin;
        x = 10;
        y = 5;
        result = x + y;
        output{result};
    end;
    """
    
    try:
        outputs = interpreter.execute(script1)
        print(f"輸出: {outputs}")
    except Exception as e:
        print(f"錯誤: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 範例 2: 字串串接
    print("範例 2: 字串串接")
    interpreter2 = CatInterpreter()
    script2 = """
    begin;
        greeting = "Hello";
        name = "World";
        message = greeting + " " + name;
        output{message};
    end;
    """
    
    try:
        outputs = interpreter2.execute(script2)
        print(f"輸出: {outputs}")
    except Exception as e:
        print(f"錯誤: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 範例 3: Discord 模組使用
    print("範例 3: Discord 模組")
    interpreter3 = CatInterpreter()
    
    # 建立模擬的 Discord 訊息
    mock_message = MockDiscordMessage("貓貓使用者", 123456789)
    discord_mod = DiscordModule(mock_message)
    
    # 註冊模組
    interpreter3.register_module(discord_mod)
    
    script3 = """
    begin;
        #load message;
        greeting = "你好，";
        welcome = greeting + message.username;
        output{welcome};
        output{message.id};
    end;
    """
    
    try:
        outputs = interpreter3.execute(script3)
        print(f"輸出: {outputs}")
    except Exception as e:
        print(f"錯誤: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 範例 4: 減法運算
    print("範例 4: 減法運算")
    interpreter4 = CatInterpreter()
    script4 = """
    begin;
        a = 100;
        b = 30;
        diff = a - b;
        output{diff};
    end;
    """
    
    try:
        outputs = interpreter4.execute(script4)
        print(f"輸出: {outputs}")
    except Exception as e:
        print(f"錯誤: {e}")
    
    print("\n=== 執行完成 ===")


if __name__ == "__main__":
    main()
