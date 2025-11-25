import requests

import requests
import os
from typing import Dict, Optional
from playwright.async_api import async_playwright
import cloudscraper
from requests.auth import HTTPBasicAuth

class ParserAgent:
    def __init__(self, parser_api):
        self.parser_api = parser_api

    def parse(self):
        pass
    
    def organize(self, result: dict):
        source = result.get("url", "No url")
        title = result.get("title", "No title")
        content = result.get("content", "")
        if not content:
            return "The page content is empty, please read another webpage."
        else:
            return (
                f"[Parse Result]\n"
                f"Title: {title}\n"
                f"URL: {source}\n"
                f"Content: {content}\n"
            )
        
    @staticmethod
    def create(engine_params: dict):
        if engine_params.get("parser_type") == "crawl4ai":
            return ParserAgentCrawl4AI(engine_params=engine_params)
        elif engine_params.get("parser_type") == "readerlmv2":
            return ParserAgentReaderLMV2(engine_params=engine_params)
        else:
            return ParserAgentJinaAI(engine_params=engine_params)

# Local
async def get_html_with_browser(url):
    async with async_playwright() as p:
        # 启动 Chromium 浏览器
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("尝试访问页面...")
        await page.goto(url)
        # 等待 Cloudflare 挑战完成（如果需要，设置一个等待时间）
        await page.wait_for_timeout(5000)

        # 获取最终渲染的 HTML 内容
        html_content = await page.content()
        await browser.close()
        return html_content
    
def get_html_with_cloudscraper(url):
    print("尝试使用 cloudscraper 访问...")
    # 1. 创建一个 scraper 实例。它会像一个 requests.Session 一样工作。
    scraper = cloudscraper.create_scraper(
        # 可选：可以传递一个 User-Agent 字典来模拟浏览器
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        }
    )

    try:
        # 2. 发起 GET 请求
        response = scraper.get(url)

        if response.status_code == 200:
            print("成功获取 HTML 内容！状态码: 200")
            return response.text
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None
       
class ParserAgentReaderLMV2(ParserAgent):
    def __init__(self, engine_params: Dict[str, str]):
        parser_api = engine_params.get("parser_api")
        if not parser_api:
            raise ValueError("The 'parser_api' is missing from the 'engine_params' configuration.")
        super().__init__(parser_api=parser_api)
        username = "5ad34100ee055a4bae66370a5e683bac"
        password = "607de8249657a3b3bd036dc96d4c0b2f"
        self.auth = HTTPBasicAuth(username, password)

    def parse(self, source):
        html_content = get_html_with_cloudscraper(source)
        if not html_content:
            raise ValueError(f"Fail to get html from {source}")
        html_content = html_content[:40000]
        messages = [
            {"role": "system", "content": "Convert the HTML to Markdown."},
            {"role": "user", "content": html_content}
        ]

        data = {
            "model": "ReaderLM-v2",  
            "messages": messages,
            "temperature": 0,
            "max_new_tokens": 4096 * 16
        }
        try:
            response = requests.post(self.parser_api, json=data, auth=self.auth, timeout=600)
            response.raise_for_status()
            markdown_output = response.json()["choices"][0]["message"]["content"].strip()
            return f"[Parse Result]\nContent: " + markdown_output
        
        except requests.exceptions.RequestException as e:
            return f"Error: ReaderLM-v2 request failed. Details: {e}"
        
class ParserAgentJinaAI(ParserAgent):
    def __init__(self, engine_params: Dict[str, str]) -> None:
        super().__init__(parser_api="https://r.jina.ai/")
        self.parser_api_key = engine_params.get("parser_api_key")
        if not self.parser_api_key:
            raise ValueError("The 'parser_api_key' is missing from the 'engine_params' configuration.")

        print(f'Proxy: {os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")}')
        self.parser_headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.parser_api_key}',
            'Content-Type': 'application/json',
            'X-Base': 'final',
            'X-Proxy-Url': os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY"),
            'X-With-Iframe': 'true',
            'X-With-Images-Summary': 'true',
            'X-With-Links-Summary': 'true',
            "X-With-Shadow-Dom": "true"
        }
            
    def parse(self, source):
        data = {
            'url': source
        }

        try:
            response = requests.post(self.parser_api, headers=self.parser_headers, json=data)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            result = response.json().get("data", [])
            print(result)
            return self.organize(result=result)

        except requests.exceptions.RequestException as e:
            return f"Error: Jina AI search request failed. Details: {e}"

class ParserAgentCrawl4AI(ParserAgent):
    """
    An agent responsible for parsing content from various sources (URLs or local files)
    and returning a text description suitable for a Large Language Model (LLM).
    """

    def __init__(self, engine_params: Dict[str, str]) -> None:
        """
        Initializes the ParseAgent.

        Args:
            api_params (dict): A dictionary containing configuration for APIs.
                Expected keys:
                - "parser_api_endpoint" (str): The URL of the content parsing API (like crawl4ai).
        """
        parser_api = engine_params.get("parser_api")
        if not parser_api:
            raise ValueError("The 'parser_api' is missing from the 'engine_params' configuration.")
        super().__init__(parser_api=parser_api)
            
        self.headers: Dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }

    def _is_url(self, path: str) -> bool:
        """Checks if the given string is a URL."""
        return path.lower().startswith(('http://', 'https://'))

    def _parse_url(self, source: str) -> str:
        """
        Parses content from a URL using the configured API endpoint.
        This is the initial implementation based on the user's request.
        """
        print(f"-> Visiting URL: {source} using API: {self.parser_api}")
        try:
            # 使用 GET 请求，并通过 params 传递 source
            response = requests.get(self.parser_api, params={"url": source}, headers=self.headers, timeout=30)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            # 假设 API 返回的 JSON 中有一个 'markdown' 字段owenY
            data = response.json()
            content = data.get("markdown")

            if content is None:
                return f"Error: The parsing API did not return a 'markdown' field for URL: {source}. Response: {data}"

            # 格式化为 LLM 友好的输出
            return (
                f'--- PARSED CONTENT FROM URL: "{source}" ---\n\n'
                f'{content.strip()}\n\n'
                f'--- END OF CONTENT ---'
            )

        except requests.exceptions.RequestException as e:
            return f"Error: Failed to fetch content from URL '{source}'. Details: {e}"

    def _parse_local_file(self, file_path: str) -> str:
        """
        Parses content from a local file. This is a placeholder for future extensions.
        It dispatches to specific methods based on file extension.
        """
        print(f"-> Parsing local file: {file_path}")
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()

        if extension == '.txt' or extension == '.md':
            # 这是一个可以立即实现的简单例子
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return (
                    f'--- PARSED CONTENT FROM LOCAL FILE: "{file_path}" ---\n\n'
                    f'{content.strip()}\n\n'
                    f'--- END OF CONTENT ---'
                )
            except Exception as e:
                return f"Error: Failed to read local file '{file_path}'. Details: {e}"
        
        # --- 扩展点 ---
        # 在这里可以添加对其他文件类型的支持
        elif extension == '.pdf':
            # 未来可以使用 PyMuPDF/pdfplumber 等库
            return f"Info: Parsing for '{extension}' files is not yet implemented."
        elif extension == '.docx':
            # 未来可以使用 python-docx 库
            return f"Info: Parsing for '{extension}' files is not yet implemented."
        else:
            return f"Error: Unsupported file type '{extension}' for local file parsing."

    def parse(self, source: str) -> str:
        """
        Parses content from a given source (URL or local file path).
        This function acts as a dispatcher, directing the input to the appropriate
        parsing method.

        Args:
            source (str): The URL or local file path to parse.

        Returns:
            str: A formatted string containing the textual description of the source,
                 ready to be consumed by an LLM.
        """
        if self._is_url(source):
            # 如果是 URL，调用 URL 解析器
            return self._parse_url(source)
        elif os.path.exists(source):
            # 如果是存在的本地路径，调用本地文件解析器
            return self._parse_local_file(source)
        else:
            # 如果都不是，返回错误信息
            return f"Error: Source '{source}' is not a valid URL or an existing local file path."

# ==============================================================================
# ============================  示例使用  ======================================
# ==============================================================================

def crawlai_test():
    # 假设您的 crawl4ai 服务正在本地 9000 端口运行
    # 如果服务在别处，请修改此处的 URL
    crawl4ai_api_endpoint = "http://0.0.0.0:9000/visit"

    # 1. 初始化 ParseAgent
    agent_params = {
        "parser_type": "crawl4ai",
        "parser_api": crawl4ai_api_endpoint,
        "parser_api_key": "none"
    }
    try:
        parser = ParserAgent.create(agent_params)
        print("ParseAgent initialized successfully.\n")

        # 2. 示例 1: 解析一个 URL
        print("="*30 + " 1. Parsing a URL " + "="*30)
        # 使用一个稳定的、内容丰富的维基百科页面作为示例
        test_url = "https://docs.searxng.org/admin/settings/settings_search.html"
        parsed_url_content = parser.parse(test_url)
        print(parsed_url_content)
        
        # 3. 示例 2: 解析一个本地文件 (已支持的 .txt)
        # print("\n" + "="*30 + " 2. Parsing a local .txt file " + "="*30)
        # # 创建一个临时的 .txt 文件用于演示
        # temp_txt_path = "sample_document.txt"
        # with open(temp_txt_path, "w", encoding="utf-8") as f:
        #     f.write("This is a test document.\nIt contains multiple lines of text.\nLLMs can easily process this.")
        
        # parsed_txt_content = parser.parse(temp_txt_path)
        # print(parsed_txt_content)
        
        # # 清理临时文件
        # os.remove(temp_txt_path)

        # # 4. 示例 3: 尝试解析一个尚不支持的本地文件类型 (.pdf)
        # print("\n" + "="*30 + " 3. Parsing an unsupported file type " + "="*30)
        # # 这只是一个虚拟路径，文件不需要实际存在，因为 `os.path.exists` 会先失败
        # # 如果文件存在，它会进入 `_parse_local_file` 并返回 "not yet implemented"
        # unsupported_file = "mydocument.pdf"
        # parsed_unsupported_content = parser.parse(unsupported_file)
        # print(parsed_unsupported_content)

        # # 5. 示例 4: 提供一个无效的输入
        # print("\n" + "="*30 + " 4. Handling an invalid input " + "="*30)
        # invalid_source = "not_a_url_or_a_file"
        # error_message = parser.parse(invalid_source)
        # print(error_message)

    except (ValueError, requests.exceptions.ConnectionError) as e:
        print(f"An error occurred during setup or execution: {e}")
        print("Please ensure the 'crawl4ai' API server is running at the specified endpoint.")

def jina_test():
    agent_params = {
        "parser_type": "jina_ai",
        "parser_api_key": "jina_1fcf08bf8acc48e583c182c814333614txS2oROhmHe-4SMKeuHWtkVe8WP4"
    }

    agent = ParserAgent.create(agent_params)
    print(agent.parse(source="https://support.google.com/chrome/answer/15085120?hl=zh-Hans&co=GENIE.Platform%3DDesktop"))

def readerlmv2_test():
    agent_params = {
        "parser_type": "readerlmv2",
        "parser_api": "https://h.pjlab.org.cn/kapi/workspace.kubebrain.io/ailab-intern11/ybw-gui-framework-jrnjs-606527-worker-0.yangbowen/8001/v1/chat/completions"
    }
    agent = ParserAgent.create(agent_params)
    print(agent.parse(source="https://support.google.com/chrome/answer/15085120?hl=zh-Hans&co=GENIE.Platform%3DDesktop"))

if __name__ == "__main__":
    # jina_test()
    # readerlmv2_test()
    crawlai_test()
