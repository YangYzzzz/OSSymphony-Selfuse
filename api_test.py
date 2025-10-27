# 导入 openai 库
import openai
import os

# --- 1. 配置您的 API 信息 ---
# 请在这里填入您的 API Key。
# 强烈建议使用环境变量来存储 API Key，而不是直接写在代码里。
# 例如: API_KEY = os.getenv("OPENAI_API_KEY")


def test_openai_api():
    """
    一个简单的函数，用于测试 OpenAI API 的连通性和有效性。
    """
    API_KEY = "sk-lZYCt4IDPC0kBJU3wO03KjmNhgE5f4p5MsZQvYBpw2A4i64D" 

    # 请在这里填入您的 API Base URL。
    # 对于官方 API，通常是 "https://api.openai.com/v1"
    # 如果您使用代理或第三方服务，请填写对应的地址。
    BASE_URL = "https://api.boyuerichdata.opensphereai.com/v1"
    print("--- 开始测试 OpenAI API ---")
    
    # 检查占位符是否已修改
    if "sk-xxxxxxxx" in API_KEY or API_KEY == "":
        print("\n[错误]：请在代码中填入您的真实 API Key！")
        return
    if "api.openai.com/v1" in BASE_URL and BASE_URL == "https://api.openai.com/v1":
         print("[提示]：您正在使用 OpenAI 官方地址。如果需要使用代理，请修改 BASE_URL。")


    try:
        # --- 2. 初始化 OpenAI 客户端 ---
        # 使用您提供的 Key 和 Base URL 创建客户端实例
        print("\n正在初始化 OpenAI 客户端...")
        client = openai.OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
        )
        print("客户端初始化成功！")

        # --- 3. 发送测试请求 ---
        # 我们将向 gpt-3.5-turbo 模型发送一个简单的问题
        print("\n正在向模型发送测试消息...")
        completion = client.chat.completions.create(
            model="gpt-5-2025-08-07",  # 您可以换成您想测试的其他模型，如 "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! Please say 'Test successful' in English."}
            ]
        )
        print("成功接收到模型的回复！")

        # --- 4. 打印回复 ---
        # 提取并打印出模型回复的内容
        response_message = completion.choices[0].message.content
        print("\n--- 测试结果 ---")
        print(f"模型回复: {response_message}")
        
        if "test successful" in response_message.lower():
            print("\n[成功] API 工作正常！")
        else:
            print("\n[警告] API 调用成功，但回复内容非预期，请检查回复。")

    except openai.AuthenticationError as e:
        print("\n--- 测试失败 ---")
        print("[错误类型]: 认证失败 (AuthenticationError)")
        print("[可能原因]: 您的 API Key 无效、已过期、被禁用或不正确。")
        print(f"[详细信息]: {e}")
    except openai.APIConnectionError as e:
        print("\n--- 测试失败 ---")
        print("[错误类型]: 连接失败 (APIConnectionError)")
        print("[可能原因]: 无法连接到您提供的 Base URL。请检查网络、代理设置或 Base URL 地址是否正确。")
        print(f"[详细信息]: {e}")
    except openai.RateLimitError as e:
        print("\n--- 测试失败 ---")
        print("[错误类型]:速率限制 (RateLimitError)")
        print("[可能原因]: 您的 API Key 已达到请求频率限制或已用完额度。")
        print(f"[详细信息]: {e}")
    except Exception as e:
        print("\n--- 测试失败 ---")
        print(f"[错误类型]: 发生未知错误 ({type(e).__name__})")
        print(f"[详细信息]: {e}")
    finally:
        print("\n--- 测试结束 ---")

def test_h_cluster_api():
    """
    一个简单的函数，用于测试 OpenAI API 的连通性和有效性。
    """

    API_KEY = "11" 

    # 请在这里填入您的 API Base URL。
    # 对于官方 API，通常是 "https://api.openai.com/v1"
    # 如果您使用代理或第三方服务，请填写对应的地址。
    BASE_URL = "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework-mmpxn-470377-worker-0.yangbowen/8000/v1"
    MODEL_NAME = "ui-tars-1.5-7b"
    
    print("--- 开始测试 H Cluster API ---")
    # 检查占位符是否已修改
    if "sk-xxxxxxxx" in API_KEY or API_KEY == "":
        print("\n[错误]：请在代码中填入您的真实 API Key！")
        return
    if "api.openai.com/v1" in BASE_URL and BASE_URL == "https://api.openai.com/v1":
         print("[提示]：您正在使用 OpenAI 官方地址。如果需要使用代理，请修改 BASE_URL。")


    try:
        # --- 2. 初始化 OpenAI 客户端 ---
        # 使用您提供的 Key 和 Base URL 创建客户端实例
        print("\n正在初始化 OpenAI 客户端...")
        custom_headers = {
            "Authorization": "Basic NWFkMzQxMDBlZTA1NWE0YmFlNjYzNzBhNWU2ODNiYWM6NjA3ZGU4MjQ5NjU3YTNiM2JkMDM2ZGM5NmQ0YzBiMmY="
        }
        client = openai.OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
            default_headers=custom_headers
        )
        print("客户端初始化成功！")

        # --- 3. 发送测试请求 ---
        # 我们将向 gpt-3.5-turbo 模型发送一个简单的问题
        print("\n正在向模型发送测试消息...")
        completion = client.chat.completions.create(
            model=MODEL_NAME,  # 您可以换成您想测试的其他模型，如 "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! Please say 'Test successful' in English."}
            ]
        )
        print("成功接收到模型的回复！")

        # --- 4. 打印回复 ---
        # 提取并打印出模型回复的内容
        response_message = completion.choices[0].message.content
        print("\n--- 测试结果 ---")
        print(f"模型回复: {response_message}")
        
        if "test successful" in response_message.lower():
            print("\n[成功] API 工作正常！")
        else:
            print("\n[警告] API 调用成功，但回复内容非预期，请检查回复。")

    except openai.AuthenticationError as e:
        print("\n--- 测试失败 ---")
        print("[错误类型]: 认证失败 (AuthenticationError)")
        print("[可能原因]: 您的 API Key 无效、已过期、被禁用或不正确。")
        print(f"[详细信息]: {e}")
    except openai.APIConnectionError as e:
        print("\n--- 测试失败 ---")
        print("[错误类型]: 连接失败 (APIConnectionError)")
        print("[可能原因]: 无法连接到您提供的 Base URL。请检查网络、代理设置或 Base URL 地址是否正确。")
        print(f"[详细信息]: {e}")
    except openai.RateLimitError as e:
        print("\n--- 测试失败 ---")
        print("[错误类型]:速率限制 (RateLimitError)")
        print("[可能原因]: 您的 API Key 已达到请求频率限制或已用完额度。")
        print(f"[详细信息]: {e}")
    except Exception as e:
        print("\n--- 测试失败 ---")
        print(f"[错误类型]: 发生未知错误 ({type(e).__name__})")
        print(f"[详细信息]: {e}")
    finally:
        print("\n--- 测试结束 ---")

# 当直接运行此脚本时，执行测试函数
if __name__ == "__main__":
    test_openai_api()
    test_h_cluster_api()