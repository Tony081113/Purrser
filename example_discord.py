#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
範例：使用 Purrser 直譯器
展示如何整合 Discord 模組
"""

from core.interpreter import CatInterpreter
from mods.discord_mod import DiscordModule


def run_example(message_data):
    """
    執行範例腳本
    :param message_data: 包含 username 和 id 的字典
    """
    # 建立直譯器實例
    interpreter = CatInterpreter()
    
    # 建立並註冊 Discord 模組
    discord_mod = DiscordModule(message_data)
    interpreter.register_module(discord_mod)
    
    # 定義腳本
    script = """
    begin;
        #load message;
        greeting = "嗨，";
        welcome_msg = greeting + message.username + "！";
        output{welcome_msg};
        id_msg = "你的 ID 是：";
        output{id_msg};
        output{message.id};
    end;
    """
    
    # 執行腳本
    try:
        outputs = interpreter.execute(script)
        print("執行結果：")
        for output in outputs:
            print(f"  {output}")
    except Exception as e:
        print(f"執行錯誤：{e}")


if __name__ == "__main__":
    # 模擬 Discord 訊息資料
    message = {
        'username': '小貓咪',
        'id': 99887766
    }
    
    print("=== Purrser Discord 整合範例 ===\n")
    run_example(message)
