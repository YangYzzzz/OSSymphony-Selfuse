import re
from collections import defaultdict
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple

import pytesseract
from PIL import Image
from pytesseract import Output

from mm_agents.interngui.memory.procedural_memory import PROCEDURAL_MEMORY
from mm_agents.interngui.core.mllm import LMMAgent
from mm_agents.interngui.utils.common_utils import call_llm_safe, smart_resize
from mm_agents.interngui.agents.coder_agent import CoderAgent
from mm_agents.interngui.agents.grounder_agent import GrounderAgent
from mm_agents.interngui.agents.searcher_agent import SearcherAgent, VLMSearcherAgent
import logging

logger = logging.getLogger("desktopenv.agent")

# Agent action decorator
def agent_action(func):
    func.is_agent_action = True
    return func

UBUNTU_APP_SETUP = f"""import subprocess;
import difflib;
import pyautogui;
pyautogui.press('escape');
time.sleep(0.5);
output = subprocess.check_output(['wmctrl', '-lx']);
output = output.decode('utf-8').splitlines();
window_titles = [line.split(None, 4)[2] for line in output];
closest_matches = difflib.get_close_matches('APP_NAME', window_titles, n=1, cutoff=0.1);
if closest_matches:
    closest_match = closest_matches[0];
    for line in output:
        if closest_match in line:
            window_id = line.split()[0]
            break;
subprocess.run(['wmctrl', '-ia', window_id])
subprocess.run(['wmctrl', '-ir', window_id, '-b', 'add,maximized_vert,maximized_horz'])
"""


SET_CELL_VALUES_CMD = """import uno
import subprocess
import unicodedata, json

def identify_document_type(component):
    if component.supportsService("com.sun.star.sheet.SpreadsheetDocument"):
        return "Calc"

    if component.supportsService("com.sun.star.text.TextDocument"):
        return "Writer"

    if component.supportsService("com.sun.star.sheet.PresentationDocument"):
        return "Impress"

    return None

def _norm_name(s: str | None) -> str | None:
    if s is None:
        return None
    if "\\\\u" in s or "\\\\U" in s or "\\\\x" in s:
        try:
            # json.loads handles all the escape forms safely
            s = json.loads(f"{{s}}")
        except Exception:
            # fallback: best-effort
            try:
                s = s.encode("utf-8").decode("unicode_escape")
            except Exception:
                pass
    # Normalize (NFC works well across platforms)
    return unicodedata.normalize("NFC", s)

def cell_ref_to_indices(cell_ref):
    column_letters = ''.join(filter(str.isalpha, cell_ref))
    row_number = ''.join(filter(str.isdigit, cell_ref))

    col = sum((ord(char.upper()) - ord('A') + 1) * (26**idx) for idx, char in enumerate(reversed(column_letters))) - 1
    row = int(row_number) - 1
    return col, row

def set_cell_values(new_cell_values: dict[str, str], app_name: str = "Untitled 1", sheet_name: str = "Sheet1"):
    app_name  = _norm_name(app_name)
    sheet_name = _norm_name(sheet_name)

    new_cell_values_idx = {{}}
    for k, v in new_cell_values.items():
        try:
            col, row = cell_ref_to_indices(k)
        except:
            col = row = None

        if col is not None and row is not None:
            new_cell_values_idx[(col, row)] = v

    # Clean up previous TCP connections.
    subprocess.run(
        'echo \"password\" | sudo -S ss --kill --tcp state TIME-WAIT sport = :2002',
        shell=True,
        check=True,
        text=True,
        capture_output=True
    )

    # Dynamically allow soffice to listen on port 2002.
    subprocess.run(
        [
            "soffice",
            "--accept=socket,host=localhost,port=2002;urp;StarOffice.Service"
        ]
    )

    local_context = uno.getComponentContext()
    resolver = local_context.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_context
    )
    context = resolver.resolve(
        f"uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext"
    )
    desktop = context.ServiceManager.createInstanceWithContext(
        "com.sun.star.frame.Desktop", context
    )

    # Collect all LibreOffice-related opened windows.
    documents = []
    for i, component in enumerate(desktop.Components):
        title = component.Title
        doc_type = identify_document_type(component)
        documents.append((i, component, title, doc_type))

    # Find the LibreOffice Calc app and the sheet of interest.
    spreadsheet = [doc for doc in documents if doc[3] == "Calc"]
    selected_spreadsheet = [doc for doc in spreadsheet if doc[2] == app_name]
    if spreadsheet:
        try:
            if selected_spreadsheet:
                spreadsheet = selected_spreadsheet[0][1]
            else:
                spreadsheet = spreadsheet[0][1]

            sheet = spreadsheet.Sheets.getByName(sheet_name)
        except:
            raise ValueError(f"Could not find sheet {{sheet_name}} in {{app_name}}.")

        for (col, row), value in new_cell_values_idx.items():
            cell = sheet.getCellByPosition(col, row)

            # Set the cell value.
            if isinstance(value, (int, float)):
                cell.Value = value
            elif isinstance(value, str):
                if value.startswith("="):
                    cell.Formula = value
                else:
                    cell.String = value
            elif isinstance(value, bool):
                cell.Value = 1 if value else 0
            elif value is None:
                cell.clearContents(0)
            else:
                raise ValueError(f"Unsupported cell value type: {{type(value)}}")

    else:
        raise ValueError(f"Could not find LibreOffice Calc app corresponding to {{app_name}}.")

set_cell_values(new_cell_values={cell_values}, app_name="{app_name}", sheet_name="{sheet_name}")        
"""


# GrounderAgent primitives are parameterized by description, and coordinate generation uses a pretrained grounding model
class OSWorldACI:
    def __init__(
        self,
        env,
        search_env,
        platform: str,
        engine_params_for_ocr: Dict,
        engine_params_for_grounder: Dict,
        engine_params_for_coder: Dict,
        engine_params_for_searcher: Dict,
        width: int = 1920,
        height: int = 1080
    ):

        # 独属于 OSWorldACI 的主环境
        self.env = env
        self.platform = platform

        # 结果目录
        self.result_dir = ""
        
        self.grounder_agent = GrounderAgent(engine_params=engine_params_for_grounder, width=width, height=height)

        # Configure text grounding agent
        self.text_span_agent = LMMAgent(
            engine_params=engine_params_for_ocr,
            system_prompt=PROCEDURAL_MEMORY.PHRASE_TO_WORD_COORDS_PROMPT,
        )

        # Configure code agent
        self.coder_agent = CoderAgent(
            engine_params=engine_params_for_coder
        )

        # Configure search agent, TODO: @Yang
        self.searcher_agent = SearcherAgent.create(
            engine_params=engine_params_for_searcher, search_env=search_env, grounder_agent=self.grounder_agent, platform=self.platform
        )

        # Store task instruction for code agent
        self.current_task_instruction = None
        self.last_code_agent_result = None
        self.last_search_agent_result = None
        self.notes: List[str] = []
        # Tutorial should be a global info, not a local context, so how to add it to the global info
        self.tutorials = []


    def assign_screenshot(self, obs):
        self.obs = obs

    # Calls pytesseract to generate word level bounding boxes for text grounding
    def get_ocr_elements(self, b64_image_data: str) -> Tuple[str, List]:
        image = Image.open(BytesIO(b64_image_data))
        image_data = pytesseract.image_to_data(image, output_type=Output.DICT)

        # Clean text by removing leading and trailing spaces and non-alphabetical characters, but keeping punctuation
        for i, word in enumerate(image_data["text"]):
            image_data["text"][i] = re.sub(
                r"^[^a-zA-Z\s.,!?;:\-\+]+|[^a-zA-Z\s.,!?;:\-\+]+$", "", word
            )

        ocr_elements = []
        ocr_table = "Text Table:\nWord id\tText\n"
        # Obtain the <id, text, group number, word number> for each valid element
        grouping_map = defaultdict(list)
        ocr_id = 0
        for i in range(len(image_data["text"])):
            block_num = image_data["block_num"][i]
            if image_data["text"][i]:
                grouping_map[block_num].append(image_data["text"][i])
                ocr_table += f"{ocr_id}\t{image_data['text'][i]}\n"
                ocr_elements.append(
                    {
                        "id": ocr_id,
                        "text": image_data["text"][i],
                        "group_num": block_num,
                        "word_num": len(grouping_map[block_num]),
                        "left": image_data["left"][i],
                        "top": image_data["top"][i],
                        "width": image_data["width"][i],
                        "height": image_data["height"][i],
                    }
                )
                ocr_id += 1

        return ocr_table, ocr_elements

    # Given the state and worker's text phrase, generate the coords of the first/last word in the phrase
    def generate_text_coords(
        self, phrase: str, obs: Dict, alignment: str = ""
    ) -> List[int]:

        ocr_table, ocr_elements = self.get_ocr_elements(obs["screenshot"])

        alignment_prompt = ""
        if alignment == "start":
            alignment_prompt = "**Important**: Output the word id of the FIRST word in the provided phrase.\n"
        elif alignment == "end":
            alignment_prompt = "**Important**: Output the word id of the LAST word in the provided phrase.\n"

        # Load LLM prompt
        self.text_span_agent.reset()
        self.text_span_agent.add_message(
            alignment_prompt + "Phrase: " + phrase + "\n" + ocr_table, role="user"
        )
        self.text_span_agent.add_message(
            "Screenshot:\n", image_content=obs["screenshot"], role="user"
        )

        # Obtain the target element
        response = call_llm_safe(self.text_span_agent)
        print("TEXT SPAN AGENT RESPONSE:", response)
        numericals = re.findall(r"\d+", response)
        if len(numericals) > 0:
            text_id = int(numericals[-1])
        else:
            text_id = 0
        elem = ocr_elements[text_id]

        # Compute the element coordinates
        if alignment == "start":
            coords = [elem["left"], elem["top"] + (elem["height"] // 2)]
        elif alignment == "end":
            coords = [elem["left"] + elem["width"], elem["top"] + (elem["height"] // 2)]
        else:
            coords = [
                elem["left"] + (elem["width"] // 2),
                elem["top"] + (elem["height"] // 2),
            ]
        return coords

    def set_task_instruction(self, task_instruction: str):
        """Set the current task instruction for the code agent."""
        self.current_task_instruction = task_instruction

    @agent_action
    def click(
        self,
        element_description: str,
        num_clicks: int = 1,
        button_type: str = "left",
        hold_keys: List = []
    ):
        """Click on the element
        Args:
            element_description:str, a detailed descriptions of which element to click on. This description needs to be VERY unambiguous. If the page contains many similar elements, ensure the description uniquely identifies the target element.
            num_clicks:int, number of times to click the element
            button_type:str, which mouse button to press can be "left", "middle", or "right"
            hold_keys:List, list of keys to hold while clicking
        """
        coords1 = self.grounder_agent.generate_coords(element_description, self.obs)
        x, y = self.grounder_agent.resize_coordinates(coords1)
        command = "import pyautogui; "

        # TODO: specified duration?
        for k in hold_keys:
            command += f"pyautogui.keyDown({repr(k)}); "
        command += f"""import pyautogui; pyautogui.click({x}, {y}, clicks={num_clicks}, button={repr(button_type)}); """
        for k in hold_keys:
            command += f"pyautogui.keyUp({repr(k)}); "
        # Return pyautoguicode to click on the element
        return (command, [x, y])

    # @agent_action
    # def switch_applications(self, app_code):
    #     """Switch to a different application that is already open
    #     Args:
    #         app_code:str the code name of the application to switch to from the provided list of open applications
    #     """
    #     if self.platform == "darwin":
    #         return f"import pyautogui; import time; pyautogui.hotkey('command', 'space', interval=0.5); pyautogui.typewrite({repr(app_code)}); pyautogui.press('enter'); time.sleep(1.0)"
    #     elif self.platform == "linux":
    #         return UBUNTU_APP_SETUP.replace("APP_NAME", app_code)
    #     elif self.platform == "windows":
    #         return f"import pyautogui; import time; pyautogui.hotkey('win', 'd', interval=0.5); pyautogui.typewrite({repr(app_code)}); pyautogui.press('enter'); time.sleep(1.0)"
    #     else:
    #         assert (
    #             False
    #         ), f"Unsupported platform: {self.platform}. Supported platforms are: darwin, linux, windows."

    @agent_action
    def open(self, app_or_filename: str):
        """Open any application or file with name app_or_filename. Use this action to open applications or files on the desktop, do not open manually.
        Args:
            app_or_filename:str, the name of the application or filename to open
        
        **Important**: 
        Provide only the name of the application or file. Do not include the full path (e.g., "/home/user/Desktop/my_report.docx"). The function works by searching for the name, not by accessing a file path directly.
        """
        if self.platform == "linux":
            return f"import pyautogui; pyautogui.hotkey('win'); time.sleep(1.0); pyautogui.write({repr(app_or_filename)}); time.sleep(1.0); pyautogui.hotkey('enter'); time.sleep(1.0)"
        elif self.platform == "darwin":
            return f"import pyautogui; import time; pyautogui.hotkey('command', 'space', interval=0.5); pyautogui.typewrite({repr(app_or_filename)}); pyautogui.press('enter'); time.sleep(1.0)"

    @agent_action
    def type(
        self,
        element_description: Optional[str] = None,
        text: str = "",
        overwrite: bool = False,
        enter: bool = False,
        is_terminal = False
    ):
        """Type text/unicode into a specific element
        Args:
            element_description:str, a detailed description of which element to enter text in. This description should be at least a full sentence.
            text:str, the text to type
            overwrite:bool, Default is False, assign it to True if the text should overwrite the existing text. Using this argument clears all text in an element.
            enter:bool, Assign it to True if the enter key should be pressed after typing the text, otherwise assign it to False.
            is_terminal:bool, Assign it to True if the target is a terminal. Defaults to False. If True, uses the 'Shift+Ctrl+V' paste shortcut common in terminals. If False, uses the standard 'Ctrl+V' shortcut.
        """
        commands = [
            "import pyautogui",
            "import pyperclip",
            "import subprocess",
            # 注意：这个安装命令每次执行都会尝试运行，可能效率不高且需要sudo权限
            # 最好确保环境已经预先配置好
            "subprocess.run('echo \"password\" | sudo -S apt-get install -y xclip xsel', shell=True, check=True, env={\"http_proxy\": \"http://10.1.8.5:23128\", \"https_proxy\": \"http://10.1.8.5:23128\"})",
            # 存储原始剪贴板
            "original_clipboard = pyperclip.paste()"
        ]
        
        click_coords = None
        if element_description is not None:
            coords1 = self.grounder_agent.generate_coords(element_description, self.obs)
            x, y = self.grounder_agent.resize_coordinates(coords1)
            commands.append(f"pyautogui.click({x}, {y})")
            click_coords = [x, y]

        if overwrite:
            if not is_terminal:
                # 使用 repr() 来确保 'command' 或 'ctrl' 字符串被正确引用
                hotkey_mod = repr('command' if self.platform == 'darwin' else 'ctrl')
                commands.append(f"pyautogui.hotkey({hotkey_mod}, 'a')")
                commands.append("pyautogui.press('backspace')")
            else:
                # 在终端中，Ctrl+A/Backspace 可能不总是清空行，Ctrl+U 更常用
                # 但 Ctrl+C 是中断，这里可能有逻辑错误，假设意图是清空行
                commands.append("pyautogui.hotkey('ctrl', 'u')") # Ctrl+U 通常用于清空光标前的内容

        # 使用剪贴板方法进行输入
        # repr(text) 会正确处理文本中的引号和特殊字符
        commands.append(f"pyperclip.copy({repr(text)})")
        
        if not is_terminal or self.platform == 'darwin':
            hotkey_mod = repr('command' if self.platform == 'darwin' else 'ctrl')
            commands.append(f"pyautogui.hotkey({hotkey_mod}, 'v')")
        else:
            # Linux 终端的粘贴
            commands.append("pyautogui.hotkey('shift', 'ctrl', 'v')")

        # 恢复原始剪贴板
        commands.append("pyperclip.copy(original_clipboard)")
        
        if enter:
            commands.append("pyautogui.press('enter')")

        # 最后，将所有命令用分号和空格连接成一个最终的字符串
        final_command = "; ".join(commands)

        if click_coords is not None:
            return (final_command, click_coords)
        else:
            return final_command
        
    # @agent_action
    # def save_to_knowledge(self, text: List[str]):
    #     """Save facts, elements, texts, etc. to a long-term knowledge bank for reuse during this task. Can be used for copy-pasting text, saving elements, etc.
    #     Args:
    #         text:List[str] the text to save to the knowledge
    #     """
    #     self.notes.extend(text)
    #     return """WAIT"""

    @agent_action
    def drag_and_drop(
        self, starting_description: str, ending_description: str, hold_keys: List = []
    ):
        """Drag from the starting description to the ending description
        Args:
            starting_description:str, a very detailed description of where to start the drag action. This description should be at least a full sentence.
            ending_description:str, a very detailed description of where to end the drag action. This description should be at least a full sentence.
            hold_keys:List list of keys to hold while dragging
        """
        coords1 = self.grounder_agent.generate_coords(starting_description, self.obs)
        coords2 = self.grounder_agent.generate_coords(ending_description, self.obs)
        x1, y1 = self.grounder_agent.resize_coordinates(coords1)
        x2, y2 = self.grounder_agent.resize_coordinates(coords2)

        command = "import pyautogui; "

        command += f"pyautogui.moveTo({x1}, {y1}); "
        # TODO: specified duration?
        for k in hold_keys:
            command += f"pyautogui.keyDown({repr(k)}); "
        command += f"pyautogui.dragTo({x2}, {y2}, duration=1., button='left'); pyautogui.mouseUp(); "
        for k in hold_keys:
            command += f"pyautogui.keyUp({repr(k)}); "

        # Return pyautoguicode to drag and drop the elements

        return (command, [x1, y1, x2, y2])

    # TODO: @Yang 如何消除重复字符的歧义? 对于复杂的Grounding任务，使用 CodeAgent 处理
    @agent_action
    def highlight_text_span(
        self, starting_phrase: str, ending_phrase: str, button: str = "left"
    ):
        """Highlight a text span between a provided starting phrase and ending phrase. Use this to highlight words, lines, and paragraphs.
        Args:
            starting_phrase:str, the phrase that denotes the start of the text span you want to highlight. If you only want to highlight one word, just pass in that single word.
            ending_phrase:str, the phrase that denotes the end of the text span you want to highlight. If you only want to highlight one word, just pass in that single word.
            button:str, the button to use to highlight the text span. Defaults to "left". Can be "left", "right", or "middle".
        """
        coords1 = self.generate_text_coords(
            starting_phrase, self.obs, alignment="start"
        )
        coords2 = self.generate_text_coords(
            ending_phrase, self.obs, alignment="end"
        )
        x1, y1 = coords1
        x2, y2 = coords2

        command = "import pyautogui; "
        command += f"pyautogui.moveTo({x1}, {y1}); "
        command += f"pyautogui.dragTo({x2}, {y2}, duration=1., button='{button}'); pyautogui.mouseUp(); "

        # Return pyautoguicode to drag and drop the elements
        return (command, [x1, y1, x2, y2])
    
    # TODO: @Yang, locate the cursor in a specified location
    @agent_action
    def locate_cursor(
        self,
        phrase: str,
        start_or_end: str="start"
    ):
        """Click at the beginning or end of a specific text phrase to precisely control cursor positioning.
        Please prefer using the "click" action in general situations, and use this action only in text-intensive software such as libreoffice_writer, impress, etc.

        Args:
            phrase: str, The text phrase where you want to position the cursor. Provide enough context to make the phrase unambiguous. If there are multiple instances of the same phrase, use a longer or more specific text segment to ensure accurate targeting.
            start_or_end: str, Whether to click at the "start" (beginning) or "end" (trailing edge) of the identified text phrase. Use "start" to position before the text, "end" to position after it.
        """
        coords = self.generate_text_coords(
            phrase, self.obs, alignment=start_or_end
        )
        x, y = coords
        command = "import pyautogui; "
        command += f"pyautogui.click({x}, {y}, button='left'); "
        return (command, [x, y])

    @agent_action
    def set_cell_values(
        self, cell_values: Dict[str, Any], app_name: str, sheet_name: str
    ):
        """Use this to set individual cell values in a spreadsheet. For example, setting A2 to "hello" would be done by passing {"A2": "hello"} as cell_values. The sheet must be opened before this command can be used.
        Args:
            cell_values: Dict[str, Any], A dictionary of cell values to set in the spreadsheet. The keys are the cell coordinates in the format "A1", "B2", etc.
                Supported value types include: float, int, string, bool, formulas.
            app_name: str, The name of the spreadsheet application. For example, "Some_sheet.xlsx".
            sheet_name: str, The name of the sheet in the spreadsheet. For example, "Sheet1".
        """
        return SET_CELL_VALUES_CMD.format(
            cell_values=cell_values, app_name=app_name, sheet_name=sheet_name
        )


    @agent_action
    def call_code_agent(self, task: str):
        """Calls the code agent to execute a well-defined, self-contained goal that can be completed with code.

        Args:
            task: str, A specific, self-contained goal that the code agent can work on until completion.

        **🚨 CRITICAL GUIDELINES:**

        **Decompose the Main Objective into Logical Goals:**
        - You **MUST** break down the overall mission into distinct, logical goals or stages.
        - Your role is to define *what* needs to be done for a specific stage. The code agent's role is to figure out *how* to do it with code.
        - Pass only one logical goal at a time. The `task` parameter is **REQUIRED**.

        **Define a Self-Contained, Continuous Goal:**
        - The `task` you provide should be a single, continuous goal. The code agent is capable of handling a multi-step process internally (e.g., opening a file, processing its data, and then saving it) to achieve this one goal.
        - **Crucially, do not pass a task that combines multiple distinct objectives.** For example, instead of passing "Analyze the sales data, create a chart, AND email the result," you should first pass the self-contained goal: "Analyze the sales data and create a chart." After that goal is complete, you can proceed with the next logical goal (e.g., emailing the result) in a subsequent step.
        - **If unsure, err on the side of caution.** If a task feels like it has two separate parts, break it down and pass only the first part.

        **Instruction Purity is Essential:**
        - **NEVER** rephrase, paraphrase, or modify the subtask instruction you have decided on. Pass the exact, original wording of the subtask to prevent instruction drift and hallucination.

        Use this for tasks that can be fully accomplished through code execution, particularly for:
        - Spreadsheet applications (LibreOffice Calc, Excel): data processing, filtering, sorting, calculations, formulas, data analysis
        - Document editors (LibreOffice Writer, Word): text processing, content editing, formatting, document manipulation
        - Code editors (VS Code, text editors): code editing, file processing, text manipulation, configuration
        - Data analysis tools: statistical analysis, data transformation, reporting
        - File management: bulk operations, file processing, content extraction
        - System utilities: configuration, setup, automation
        """
        logger.info("=" * 50)
        logger.info("ACI: Calling Code Agent")
        logger.info("=" * 50)

        # **CRITICAL**: Only use provided task for specific subtasks, otherwise use original task instruction
        if task is not None:
            # This is a subtask - use the provided task
            task_to_execute = task
            logger.info(f"Executing SUBTASK: {task_to_execute}")
        else:
            # This is a full task - use the original task instruction to prevent hallucination
            task_to_execute = self.current_task_instruction
            logger.info(f"Executing FULL TASK: {task_to_execute}")

        if task_to_execute:
            print("obs keys: ", self.obs.keys())
            screenshot = self.obs.get("screenshot", "") if self.obs else ""
            logger.info(f"Screenshot available: {'Yes' if screenshot else 'No'}")

            logger.info("Executing code agent...")

            # 在一个动作内部能够执行
            result = self.coder_agent.execute(
                task_to_execute, screenshot, self.env.controller
            )

            # Store the result for the worker to access
            self.last_code_agent_result = result

            logger.info("Code agent execution completed")
            logger.info(f"Result - Completion reason: {result['completion_reason']}")
            logger.info(f"Steps executed: {result['steps_executed']}")
            logger.info(f"Summary: {result['summary']}")

            logger.info("=" * 50)
            logger.info("GROUNDING AGENT: Code Agent Call Finished")
            logger.info("=" * 50)

            # Return code to be executed in the environment
            return "import time; time.sleep(2.222)"
        else:
            logger.warning("No task instruction available for code agent call")
            return "import time; time.sleep(1.111)"

    @agent_action
    def scroll(self, element_description: str, clicks: int, shift: bool = False):
        """Scroll the element in the specified direction
        Args:
            element_description:str, a very detailed description of which element to enter scroll in. This description should be at least a full sentence.
            clicks:int, the number of clicks to scroll can be positive (up) or negative (down).
            shift:bool, whether to use shift+scroll for horizontal scrolling
        """
        coords1 = self.grounder_agent.generate_coords(element_description, self.obs)
        x, y = self.grounder_agent.resize_coordinates(coords1)

        if shift:
            return (f"import pyautogui; import time; pyautogui.moveTo({x}, {y}); time.sleep(0.5); pyautogui.hscroll({clicks})", [x, y])
        else:
            return (f"import pyautogui; import time; pyautogui.moveTo({x}, {y}); time.sleep(0.5); pyautogui.vscroll({clicks})", [x, y])

    @agent_action
    def hotkey(self, keys: List):
        """Press a hotkey combination (can press a single key as well)
        Args:
            keys:List the keys to press in combination in a list format (e.g. ['ctrl', 'c'], ['enter'])
        """
        # add quotes around the keys
        keys = [f"'{key}'" for key in keys]
        return f"import pyautogui; pyautogui.hotkey({', '.join(keys)})"

    @agent_action
    def hold_and_press(self, hold_keys: List, press_keys: List):
        """Hold a list of keys and press a list of keys
        Args:
            hold_keys:List, list of keys to hold
            press_keys:List, list of keys to press in a sequence
        """

        press_keys_str = "[" + ", ".join([f"'{key}'" for key in press_keys]) + "]"
        command = "import pyautogui; "
        for k in hold_keys:
            command += f"pyautogui.keyDown({repr(k)}); "
        command += f"pyautogui.press({press_keys_str}); "
        for k in hold_keys:
            command += f"pyautogui.keyUp({repr(k)}); "

        return command

    @agent_action
    def wait(self, time: float):
        """Wait for a specified amount of time
        Args:
            time:float, the amount of time to wait in seconds
        """
        return f"""import time; time.sleep({time})"""

    @agent_action
    def done(
        self,
    ):
        """End the current task with a success. Use this when you believe the entire task has been fully completed."""
        return """DONE"""

    @agent_action
    def fail(self):
        """End the current task with a failure. Use this when you believe the entire task is impossible to complete."""
        return """FAIL"""
    
    @agent_action
    def call_search_agent(
        self, 
        query: str,
    ):
        """
        Calls a specialized 'Searcher Agent' to find a detailed, step-by-step tutorial on the internet for a specific GUI action.
        Args:
            query:str, the search phrase or question for the tutorial. The formulation of this query is critical for success and must follow the guidelines below.

        **Query Formulation Guidelines:**

        Your query must be a well-defined question targeting a **single, specific action** within a **specific application**. To get the best results, adhere to these rules:

        1.  **Start with "How to":** Your query must begin with the phrase "How to" to frame it as a request for instructions.
        2.  **Include the Application Name:** Always specify the name of the software you are working in (e.g., "GIMP", "Google Chrome", "Libreoffice Writer").
        3.  **Focus on a Single Intent:** The query should represent one clear goal. Do not combine multiple steps or tasks into one query.
        4.  **Be Specific, Not Abstract:** Ask a concrete question. Avoid repeating the user's high-level or abstract instructions.
        5.  **Decompose Complex Tasks:** If the user's overall instruction involves multiple actions (e.g., "download a file and then email it"), and you are stuck on one part, search *only for that specific part*.

        **Examples:**

        *   **User's Overall Instruction:** "Please help me download my latest bank statement and then send it to my accountant."
            *   **Correct Query (if stuck on downloading):** "How to download a bank statement from the Bank of America website?"
            *   **Correct Query (if stuck on attaching a file):** "How to attach a file to an email in Gmail?"
            *   **Incorrect Query:** "Download my bank statement and email it to my accountant" *(This query is too broad, contains multiple sub-tasks, and does not start with "How to".)*

        **Interpreting the Returned Tutorial:**

        The Searcher Agent aims to find a *complete* tutorial, often starting from the very beginning. This means the returned guide may contain steps you have already completed.
        It is **your responsibility** to analyze the tutorial in conjunction with your current screen context to determine the correct step to begin with. **Do not blindly follow the tutorial from step 1.**

        **Execution Effect:**
        This action pauses the current agent's execution and delegates the search task to an independent Searcher Agent. The resulting tutorial will be made available to you as context to guide your subsequent actions.
        """
        logger.info("=" * 50)
        logger.info(f"ACI: Calling Search Agent(query={query})")
        logger.info("=" * 50)
        if isinstance(self.searcher_agent, VLMSearcherAgent):
            self.searcher_agent.result_dir = self.result_dir
            result = self.searcher_agent.search(query=query, main_obs=self.obs)
            self.last_search_agent_result = result
            if result["completion_reason"] == "DONE":
                self.tutorials.append(result["final_answer"])
        return "import time; time.sleep(2.222)"
    