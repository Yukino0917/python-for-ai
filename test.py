import os
from dotenv import load_dotenv

load_dotenv()  # 从 .env 读取配置，放入当前程序的环境变量

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("请先配置 DEEPSEEK_API_KEY")