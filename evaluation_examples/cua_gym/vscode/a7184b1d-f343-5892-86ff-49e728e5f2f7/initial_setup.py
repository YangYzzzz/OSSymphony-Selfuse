"""
Initial Setup: Create long_function.py for VSCode fold/unfold task
Task ID: vscode_edit_087
Domain: vs_code
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_edit_087'
DESKTOP = f'{WORKDIR}/Desktop'
OUTPUT = f'{DESKTOP}/long_function.py'


def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_initial():
    os.makedirs(DESKTOP, exist_ok=True)

    # Build a 100-line Python file with one main function 'process_all' (lines 1-100)
    # Structure (matching task context exactly):
    #   Lines 1-4:   function definition + docstring
    #   Lines 5-25:  for-loop block (21 lines including header)
    #   Line 26:     blank
    #   Lines 27-50: if-block (24 lines including header)
    #   Line 51:     blank
    #   Lines 52-75: try-except block (24 lines including header)
    #   Line 76:     blank
    #   Lines 77-98: while-loop block (22 lines including header)
    #   Line 99:     blank
    #   Line 100:    return statement closing function

    lines = [
        # 1-4: function header + docstring
        "def process_all(data_list, config=None):",
        '    """Process a list of data items with optional configuration.',
        "    Yields result dicts for each processed item.",
        '    """',
        # 5-25: for-loop block (line 5 = header, lines 6-25 = body = 20 lines)
        "    for item in data_list:",
        '        name = item.get("name", "unknown")',
        '        status = item.get("status", "pending")',
        '        priority = item.get("priority", 1)',
        '        category = item.get("category", "general")',
        "        score = priority * 10",
        '        if status == "active":',
        "            score += 50",
        '        elif status == "archived":',
        "            score -= 5",
        "        result_label = f\"{category}/{name}\"",
        "        entry = {",
        '            "label": result_label,',
        '            "score": score,',
        '            "status": status,',
        "        }",
        "        yield entry",
        "        score = max(0, score)",
        "        result_label = result_label.lower()",
        "        name = name.strip()",
        "        continue",
        # 26: blank
        "",
        # 27-50: if-block (line 27 = header, lines 28-50 = body = 23 lines)
        "    if config is not None:",
        '        mode = config.get("mode", "default")',
        '        verbose = config.get("verbose", False)',
        '        max_retries = config.get("max_retries", 3)',
        '        timeout = config.get("timeout", 30)',
        '        output_format = config.get("output_format", "json")',
        '        allowed_formats = ["json", "csv", "xml", "tsv"]',
        "        if output_format not in allowed_formats:",
        '            output_format = "json"',
        '        if mode == "strict":',
        "            max_retries = min(max_retries, 1)",
        "        config_summary = {",
        '            "mode": mode,',
        '            "output_format": output_format,',
        '            "max_retries": max_retries,',
        '            "timeout": timeout,',
        '            "verbose": verbose,',
        "        }",
        '        yield {"config_summary": config_summary}',
        '        yield {"mode_active": mode}',
        '        yield {"format_active": output_format}',
        '        yield {"timeout_active": timeout}',
        "        max_retries = max(1, max_retries)",
        "        timeout = min(300, timeout)",
        # 51: blank
        "",
        # 52-75: try-except block (line 52 = header, lines 53-75 = body = 23 lines)
        "    try:",
        "        sentinel = object()",
        "        first = next(iter(data_list), sentinel)",
        "        if first is sentinel:",
        "            return",
        '        validate_fields = ["name", "status", "priority"]',
        "        if isinstance(first, dict):",
        "            missing = [f for f in validate_fields if f not in first]",
        "            if missing:",
        "                raise ValueError(f\"Missing required fields: {missing}\")",
        '        chunk_size = (config or {}).get("chunk_size", 100)',
        "        checksum = sum(len(str(item)) for item in data_list)",
        '        yield {"validation": "ok", "checksum": checksum}',
        '        yield {"chunk_size": chunk_size}',
        "    except StopIteration:",
        '        yield {"validation": "skipped"}',
        "    except (TypeError, AttributeError) as exc:",
        '        yield {"validation": "error", "detail": str(exc)}',
        "    except ValueError as exc:",
        '        yield {"validation": "invalid", "detail": str(exc)}',
        "    except Exception as exc:",
        '        yield {"validation": "unknown_error", "detail": str(exc)}',
        "    finally:",
        "        pass",
        # 76: blank
        "",
        # 77-98: while-loop block (line 77 = header, lines 78-98 = body = 21 lines)
        "    while True:",
        "        retry_count = 0",
        '        max_attempts = (config or {}).get("max_retries", 3)',
        "        backoff = 0.1",
        "        while retry_count < max_attempts:",
        "            retry_count += 1",
        "            backoff = min(backoff * 2, 2.0)",
        "            if retry_count == max_attempts:",
        '                yield {"retry_final": retry_count}',
        "            else:",
        '                yield {"retry": retry_count}',
        "            accumulated = retry_count * backoff",
        "            if accumulated > 10:",
        "                break",
        "            if backoff >= 2.0:",
        "                backoff = 0.1",
        "            if retry_count > 100:",
        "                break",
        "        del retry_count, backoff, max_attempts",
        "        break",
        "        yield",
        "        continue",
        # 99: blank
        "",
        # 100: closing yield
        '    yield {"status": "complete"}',
    ]

    assert len(lines) == 100, f'Expected 100 lines, got {len(lines)}'

    content = "\n".join(lines) + "\n"
    with open(OUTPUT, 'w') as f:
        f.write(content)

    actual_count = len(content.rstrip('\n').split('\n'))
    print(f'File written: {OUTPUT}  ({actual_count} lines)')
    assert actual_count == 100, f'Expected 100 lines, got {actual_count}'

    # GUI-ready startup: open VSCode with the file
    launch_gui(f'code "{OUTPUT}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
