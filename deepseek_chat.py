import os
from pathlib import Path

import requests
from dotenv import load_dotenv


def main():
    # 读取脚本旁边的 .env；已有的系统环境变量优先。
    load_dotenv(Path(__file__).with_name(".env"))
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        print("请先在 .env 中填写 DEEPSEEK_API_KEY，再运行程序。")
        return 1

    question = input("请输入你的问题：").strip()
    if not question:
        print("问题不能为空。")
        return 1

    try:
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "deepseek-flash",
                "messages": [{"role": "user", "content": question}],
                "thinking": {"type": "disabled"},
                "max_tokens": 4096,
                "stream": False,
            },
            timeout=60,
        )
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]
        if not isinstance(answer, str) or not answer.strip():
            print("API 没有返回文本回答，请稍后重试。")
            return 1
    except requests.HTTPError as error:
        status = error.response.status_code
        tips = {
            400: "请求参数有误，请检查 model、max_tokens 等设置。",
            401: "请检查 API Key。",
            402: "请检查 DeepSeek 账户余额。",
        }
        print(f"调用失败（HTTP {status}）。" + tips.get(status, "请稍后重试。"))
        return 1
    except requests.RequestException:
        print("连接失败或请求超时，请检查网络后重试。")
        return 1
    except (ValueError, KeyError, IndexError, TypeError):
        print("API 返回了无法解析的数据，请稍后重试。")
        return 1

    print("\nDeepSeek：")
    print(answer)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyboardInterrupt, EOFError):
        print("\n已退出。")
