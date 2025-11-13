
from functools import partial
from mm_agents.interngui.agents.os_aci import OSWorldACI
from mm_agents.interngui.utils.common_utils import parse_code_from_string, create_pyautogui_code
from typing import Dict, Any
from mm_agents.interngui.utils.formatters import CODE_VALID_FORMATTER
class FakeAgent:
    def __init__(self) -> None:
        pass

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
        return "yes"
    
    def assign_screenshot(self, obs):
        pass

agent = FakeAgent()
coordinates = None
plan = """
The previous action successfully switched back to Sheet1. I can see the sales data with columns
■ Product (C), Quantity (E), and Discount (F), ready for adding the Revenue column.
■(Screenshot Analysis)
• LibreOffice Calc is open with BoomerangSales.xlsx, active on Sheet1. Columns A-F are populated;
column G is empty and suitable for adding a new "Revenue" column. The "Retail Price" sheet conta
■ins the lookup table (A2:B22) with Product and Retail Price.
(Next Action)
■Insert a new "Revenue" column header in G1 and add a formula in G2 that calculates revenue using
■ the retail price from the Retail Price sheet multiplied by Quantity and (1 - Discount). I will
set:
=VLOOKUP(C2; 'Retail Price'.$A$2:$B$22;2;0)*E2*(1-F2)
(Grounded Action)
```python
agent.set_cell_values(
{
    "G1": "Revenue",
    "G2": "=VLOOKUP(C2; 'Retail Price'.$A$2:$B$22;2;0)*E2*(1-F2)"
    },
    app_name="BoomerangSales.xlsx",
    sheet_name="Sheet1"
)
```
"""
format_checkers = [
    partial(CODE_VALID_FORMATTER, agent, None),
]
success, feedback = format_checkers[0](plan)
print(f'success: {success}, feedback: {feedback}')

plan_code = parse_code_from_string(plan)
print(f'plancode: {plan_code}')
# 此时的exec_code e.g. import pyautogui; pyautogui.click(1, 2);
exec_code, coordinates = create_pyautogui_code(agent, plan_code, None)
print(f'exec_code: {exec_code}')