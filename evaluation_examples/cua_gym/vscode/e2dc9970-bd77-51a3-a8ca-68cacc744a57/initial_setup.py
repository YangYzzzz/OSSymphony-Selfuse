"""
Initial Setup: VSCode Git Branch Comparison - Parser Regression
Task ID: vscode_git_074
Domain: vs_code

Creates a Python project in /home/user/project with:
- A git repository containing parser.py on multiple branches
- The parse_data() function works on main and develop
- The function is broken on feature/v2-parser (return type changed in second commit)
- hotfix/parser-fix branch with a partial fix attempt
- Opens VSCode with the project folder for the agent to investigate
"""

import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_074'
PROJECT_DIR = f'{WORKDIR}/project'


def run_cmd(cmd, cwd=None, env=None):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd, env=env
    )
    if result.returncode != 0:
        print(f'CMD ERROR: {cmd}')
        print(f'STDERR: {result.stderr}')
    return result


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


PARSER_MAIN = '''\
"""
Parser module for data processing pipeline.
Handles multiple data formats and returns structured results.
"""

import json
import csv
import io
from typing import List, Dict, Any, Optional


class ParseError(Exception):
    """Raised when input data cannot be parsed."""
    pass


def parse_data(raw_input: str, format: str = 'auto') -> List[Dict[str, Any]]:
    """
    Parse raw input data into a list of structured records.

    Args:
        raw_input: String containing the data to parse
        format: One of 'json', 'csv', or 'auto' (auto-detect)

    Returns:
        List of dicts, one per record

    Raises:
        ParseError: If the data cannot be parsed
    """
    if not raw_input or not raw_input.strip():
        return []

    detected = format
    if format == 'auto':
        stripped = raw_input.strip()
        if stripped.startswith('[') or stripped.startswith('{'):
            detected = 'json'
        else:
            detected = 'csv'

    if detected == 'json':
        try:
            data = json.loads(raw_input)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                raise ParseError(f'Expected list or dict, got {type(data).__name__}')
        except json.JSONDecodeError as e:
            raise ParseError(f'JSON parse error: {e}')

    elif detected == 'csv':
        reader = csv.DictReader(io.StringIO(raw_input))
        records = []
        for row in reader:
            records.append(dict(row))
        if not records:
            raise ParseError('CSV contains no data rows')
        return records

    else:
        raise ParseError(f'Unknown format: {format}')


def validate_records(records: List[Dict[str, Any]],
                     required_fields: Optional[List[str]] = None) -> bool:
    """
    Validate that all records contain required fields.

    Args:
        records: List of record dicts from parse_data()
        required_fields: Fields that must be present in each record

    Returns:
        True if all records are valid
    """
    if not records:
        return True
    if required_fields is None:
        return True
    for i, record in enumerate(records):
        for field in required_fields:
            if field not in record:
                raise ValueError(f'Record {i} missing required field: {field}')
    return True


def transform_record(record: Dict[str, Any],
                     field_map: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Transform a record by renaming fields according to field_map.

    Args:
        record: Single record dict
        field_map: Mapping of old field names to new field names

    Returns:
        Transformed record dict
    """
    if not field_map:
        return record.copy()
    result = {}
    for key, value in record.items():
        new_key = field_map.get(key, key)
        result[new_key] = value
    return result
'''

PARSER_DEVELOP = '''\
"""
Parser module for data processing pipeline.
Handles multiple data formats and returns structured results.
"""

import json
import csv
import io
from typing import List, Dict, Any, Optional


class ParseError(Exception):
    """Raised when input data cannot be parsed."""
    pass


def parse_data(raw_input: str, format: str = 'auto') -> List[Dict[str, Any]]:
    """
    Parse raw input data into a list of structured records.

    Args:
        raw_input: String containing the data to parse
        format: One of 'json', 'csv', or 'auto' (auto-detect)

    Returns:
        List of dicts, one per record

    Raises:
        ParseError: If the data cannot be parsed
    """
    if not raw_input or not raw_input.strip():
        return []

    detected = format
    if format == 'auto':
        stripped = raw_input.strip()
        if stripped.startswith('[') or stripped.startswith('{'):
            detected = 'json'
        else:
            detected = 'csv'

    if detected == 'json':
        try:
            data = json.loads(raw_input)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                raise ParseError(f'Expected list or dict, got {type(data).__name__}')
        except json.JSONDecodeError as e:
            raise ParseError(f'JSON parse error: {e}')

    elif detected == 'csv':
        reader = csv.DictReader(io.StringIO(raw_input))
        records = []
        for row in reader:
            records.append(dict(row))
        if not records:
            raise ParseError('CSV contains no data rows')
        return records

    else:
        raise ParseError(f'Unknown format: {format}')


def validate_records(records: List[Dict[str, Any]],
                     required_fields: Optional[List[str]] = None) -> bool:
    """Validate that all records contain required fields."""
    if not records:
        return True
    if required_fields is None:
        return True
    for i, record in enumerate(records):
        for field in required_fields:
            if field not in record:
                raise ValueError(f'Record {i} missing required field: {field}')
    return True


def transform_record(record: Dict[str, Any],
                     field_map: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Transform a record by renaming fields according to field_map."""
    if not field_map:
        return record.copy()
    result = {}
    for key, value in record.items():
        new_key = field_map.get(key, key)
        result[new_key] = value
    return result


def batch_parse(inputs: List[str], format: str = 'auto') -> List[List[Dict[str, Any]]]:
    """
    Parse a list of raw inputs in batch.

    Args:
        inputs: List of raw input strings
        format: Format hint for all inputs

    Returns:
        List of parsed record lists
    """
    results = []
    for raw in inputs:
        try:
            results.append(parse_data(raw, format))
        except ParseError:
            results.append([])
    return results
'''

PARSER_FEATURE_V1 = '''\
"""
Parser module for data processing pipeline - v2 refactor.
Handles multiple data formats and returns structured results.
Enhanced with streaming support and new output modes.
"""

import json
import csv
import io
from typing import List, Dict, Any, Optional, Union


class ParseError(Exception):
    """Raised when input data cannot be parsed."""
    pass


def parse_data(raw_input: str, format: str = 'auto') -> List[Dict[str, Any]]:
    """
    Parse raw input data into a list of structured records.

    Args:
        raw_input: String containing the data to parse
        format: One of 'json', 'csv', 'tsv', or 'auto' (auto-detect)

    Returns:
        List of dicts, one per record

    Raises:
        ParseError: If the data cannot be parsed
    """
    if not raw_input or not raw_input.strip():
        return []

    detected = format
    if format == 'auto':
        stripped = raw_input.strip()
        if stripped.startswith('[') or stripped.startswith('{'):
            detected = 'json'
        elif '\\t' in stripped.split('\\n')[0]:
            detected = 'tsv'
        else:
            detected = 'csv'

    if detected == 'json':
        try:
            data = json.loads(raw_input)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                raise ParseError(f'Expected list or dict, got {type(data).__name__}')
        except json.JSONDecodeError as e:
            raise ParseError(f'JSON parse error: {e}')

    elif detected in ('csv', 'tsv'):
        delimiter = '\\t' if detected == 'tsv' else ','
        reader = csv.DictReader(io.StringIO(raw_input), delimiter=delimiter)
        records = []
        for row in reader:
            records.append(dict(row))
        if not records:
            raise ParseError(f'{detected.upper()} contains no data rows')
        return records

    else:
        raise ParseError(f'Unknown format: {format}')


def validate_records(records: List[Dict[str, Any]],
                     required_fields: Optional[List[str]] = None) -> bool:
    """Validate that all records contain required fields."""
    if not records:
        return True
    if required_fields is None:
        return True
    for i, record in enumerate(records):
        for field in required_fields:
            if field not in record:
                raise ValueError(f'Record {i} missing required field: {field}')
    return True


def transform_record(record: Dict[str, Any],
                     field_map: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Transform a record by renaming fields according to field_map."""
    if not field_map:
        return record.copy()
    result = {}
    for key, value in record.items():
        new_key = field_map.get(key, key)
        result[new_key] = value
    return result


def batch_parse(inputs: List[str], format: str = 'auto') -> List[List[Dict[str, Any]]]:
    """Parse a list of raw inputs in batch."""
    results = []
    for raw in inputs:
        try:
            results.append(parse_data(raw, format))
        except ParseError:
            results.append([])
    return results


def stream_parse(file_path: str, format: str = 'auto',
                 chunk_size: int = 1000) -> List[List[Dict[str, Any]]]:
    """
    Stream-parse a large file in chunks.

    Args:
        file_path: Path to input file
        format: Format hint
        chunk_size: Number of records per chunk

    Returns:
        List of chunks, each chunk being a list of records
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    all_records = parse_data(content, format)
    chunks = []
    for i in range(0, len(all_records), chunk_size):
        chunks.append(all_records[i:i + chunk_size])
    return chunks
'''

# THE REGRESSION: return type changed from List[Dict] to Dict wrapping records
PARSER_FEATURE_V2_BROKEN = '''\
"""
Parser module for data processing pipeline - v2 refactor.
Handles multiple data formats and returns structured results.
Enhanced with streaming support, new output modes, and schema inference.
"""

import json
import csv
import io
from typing import List, Dict, Any, Optional, Union


class ParseError(Exception):
    """Raised when input data cannot be parsed."""
    pass


def parse_data(raw_input: str, format: str = 'auto') -> Dict[str, Any]:
    """
    Parse raw input data into a structured record or collection.

    Args:
        raw_input: String containing the data to parse
        format: One of 'json', 'csv', 'tsv', or 'auto' (auto-detect)

    Returns:
        Dict with 'records' key containing parsed data and 'count' key

    Raises:
        ParseError: If the data cannot be parsed
    """
    if not raw_input or not raw_input.strip():
        return {'records': [], 'count': 0}

    detected = format
    if format == 'auto':
        stripped = raw_input.strip()
        if stripped.startswith('[') or stripped.startswith('{'):
            detected = 'json'
        elif '\\t' in stripped.split('\\n')[0]:
            detected = 'tsv'
        else:
            detected = 'csv'

    if detected == 'json':
        try:
            data = json.loads(raw_input)
            if isinstance(data, list):
                records = data
            elif isinstance(data, dict):
                records = [data]
            else:
                raise ParseError(f'Expected list or dict, got {type(data).__name__}')
        except json.JSONDecodeError as e:
            raise ParseError(f'JSON parse error: {e}')

    elif detected in ('csv', 'tsv'):
        delimiter = '\\t' if detected == 'tsv' else ','
        reader = csv.DictReader(io.StringIO(raw_input), delimiter=delimiter)
        records = []
        for row in reader:
            records.append(dict(row))
        if not records:
            raise ParseError(f'{detected.upper()} contains no data rows')

    else:
        raise ParseError(f'Unknown format: {format}')

    return {'records': records, 'count': len(records)}


def validate_records(records: List[Dict[str, Any]],
                     required_fields: Optional[List[str]] = None) -> bool:
    """Validate that all records contain required fields."""
    if not records:
        return True
    if required_fields is None:
        return True
    for i, record in enumerate(records):
        for field in required_fields:
            if field not in record:
                raise ValueError(f'Record {i} missing required field: {field}')
    return True


def transform_record(record: Dict[str, Any],
                     field_map: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Transform a record by renaming fields according to field_map."""
    if not field_map:
        return record.copy()
    result = {}
    for key, value in record.items():
        new_key = field_map.get(key, key)
        result[new_key] = value
    return result


def batch_parse(inputs: List[str], format: str = 'auto') -> List[List[Dict[str, Any]]]:
    """Parse a list of raw inputs in batch."""
    results = []
    for raw in inputs:
        try:
            result = parse_data(raw, format)
            results.append(result.get('records', []))
        except ParseError:
            results.append([])
    return results


def stream_parse(file_path: str, format: str = 'auto',
                 chunk_size: int = 1000) -> List[List[Dict[str, Any]]]:
    """Stream-parse a large file in chunks."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    result = parse_data(content, format)
    all_records = result.get('records', [])
    chunks = []
    for i in range(0, len(all_records), chunk_size):
        chunks.append(all_records[i:i + chunk_size])
    return chunks


def infer_schema(records: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Infer field types from a list of records.

    Args:
        records: List of record dicts

    Returns:
        Dict mapping field names to inferred type strings
    """
    if not records:
        return {}

    schema = {}
    all_fields = set()
    for record in records:
        all_fields.update(record.keys())

    for field in all_fields:
        values = [r[field] for r in records if field in r]
        non_empty = [v for v in values if v is not None and v != '']

        if not non_empty:
            schema[field] = 'unknown'
            continue

        try:
            [float(str(v)) for v in non_empty]
            if all('.' not in str(v) for v in non_empty):
                schema[field] = 'integer'
            else:
                schema[field] = 'float'
        except (ValueError, TypeError):
            schema[field] = 'string'

    return schema
'''

PARSER_HOTFIX = '''\
"""
Parser module for data processing pipeline.
Handles multiple data formats and returns structured results.
[HOTFIX] Added input sanitization and better error messages.
"""

import json
import csv
import io
import re
from typing import List, Dict, Any, Optional


class ParseError(Exception):
    """Raised when input data cannot be parsed."""
    pass


def _sanitize_input(raw_input: str) -> str:
    """Remove null bytes and normalize line endings."""
    cleaned = raw_input.replace('\\x00', '')
    cleaned = cleaned.replace('\\r\\n', '\\n').replace('\\r', '\\n')
    return cleaned


def parse_data(raw_input: str, format: str = 'auto') -> List[Dict[str, Any]]:
    """
    Parse raw input data into a list of structured records.

    Args:
        raw_input: String containing the data to parse
        format: One of 'json', 'csv', or 'auto' (auto-detect)

    Returns:
        List of dicts, one per record

    Raises:
        ParseError: If the data cannot be parsed
    """
    if not raw_input or not raw_input.strip():
        return []

    raw_input = _sanitize_input(raw_input)

    detected = format
    if format == 'auto':
        stripped = raw_input.strip()
        if stripped.startswith('[') or stripped.startswith('{'):
            detected = 'json'
        else:
            detected = 'csv'

    if detected == 'json':
        try:
            data = json.loads(raw_input)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                raise ParseError(f'Expected list or dict, got {type(data).__name__}')
        except json.JSONDecodeError as e:
            raise ParseError(f'JSON parse error at position {e.pos}: {e.msg}')

    elif detected == 'csv':
        reader = csv.DictReader(io.StringIO(raw_input))
        records = []
        for row in reader:
            records.append(dict(row))
        if not records:
            raise ParseError('CSV input parsed successfully but contains no data rows. '
                             'Check that the CSV has a header row and at least one data row.')
        return records

    else:
        raise ParseError(f'Unknown format: {format!r}. Supported formats: json, csv, auto')


def validate_records(records: List[Dict[str, Any]],
                     required_fields: Optional[List[str]] = None) -> bool:
    """Validate that all records contain required fields."""
    if not records:
        return True
    if required_fields is None:
        return True
    for i, record in enumerate(records):
        for field in required_fields:
            if field not in record:
                raise ValueError(f'Record {i} missing required field: {field!r}')
    return True


def transform_record(record: Dict[str, Any],
                     field_map: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Transform a record by renaming fields according to field_map."""
    if not field_map:
        return record.copy()
    result = {}
    for key, value in record.items():
        new_key = field_map.get(key, key)
        result[new_key] = value
    return result
'''

UTILS = '''\
"""
Utility functions for the data processing pipeline.
"""

import hashlib
import datetime
from typing import Any, Dict, List


def compute_checksum(data: str) -> str:
    """Compute MD5 checksum of input string."""
    return hashlib.md5(data.encode('utf-8')).hexdigest()


def timestamp_now() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.datetime.utcnow().isoformat() + 'Z'


def flatten_dict(d: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
    """
    Flatten a nested dict into a single-level dict with dotted keys.

    Example:
        {\'a\': {\'b\': 1}} -> {\'a.b\': 1}
    """
    result = {}
    for key, value in d.items():
        full_key = f\'{prefix}.{key}\' if prefix else key
        if isinstance(value, dict):
            result.update(flatten_dict(value, full_key))
        else:
            result[full_key] = value
    return result


def chunk_list(lst: List[Any], size: int) -> List[List[Any]]:
    """Split list into chunks of given size."""
    return [lst[i:i + size] for i in range(0, len(lst), size)]
'''

README = '''\
# Data Parser Project

A lightweight Python library for parsing and transforming structured data.

## Features

- Supports JSON and CSV input formats
- Auto-detection of format
- Record validation and field transformation
- Comprehensive error handling

## Usage

```python
from parser import parse_data, validate_records

# Parse CSV data
csv_data = """name,age,department
Alice Wang,34,Engineering
Bob Martinez,28,Marketing
Carol Smith,41,Finance"""

records = parse_data(csv_data)
print(records)
# [{\'name\': \'Alice Wang\', \'age\': \'34\', \'department\': \'Engineering\'}, ...]

# Parse JSON data
json_data = \'[{"id": 1, "value": 42}, {"id": 2, "value": 17}]\'
records = parse_data(json_data, format=\'json\')
```

## API

### `parse_data(raw_input, format=\'auto\')`
Parse raw string into list of dicts.

### `validate_records(records, required_fields=None)`
Validate that all records contain required fields.

### `transform_record(record, field_map=None)`
Rename fields in a record according to field_map.
'''

TEST_PARSER = '''\
"""
Unit tests for parser module.
"""

import unittest
from parser import parse_data, validate_records, transform_record, ParseError


class TestParseData(unittest.TestCase):

    def test_parse_json_list(self):
        data = \'[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]\'
        result = parse_data(data)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][\'name\'], \'Alice\')

    def test_parse_json_dict(self):
        data = \'{"id": 1, "name": "Alice"}\'
        result = parse_data(data)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_parse_csv(self):
        data = "name,age\\\\nAlice,34\\\\nBob,28"
        result = parse_data(data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][\'name\'], \'Alice\')

    def test_empty_input(self):
        result = parse_data("")
        self.assertEqual(result, [])

    def test_invalid_json(self):
        with self.assertRaises(ParseError):
            parse_data("{invalid json}", format=\'json\')

    def test_validate_records_valid(self):
        records = [{\'id\': 1, \'name\': \'Alice\'}, {\'id\': 2, \'name\': \'Bob\'}]
        self.assertTrue(validate_records(records, [\'id\', \'name\']))

    def test_transform_record(self):
        record = {\'id\': 1, \'nm\': \'Alice\'}
        result = transform_record(record, {\'nm\': \'name\'})
        self.assertIn(\'name\', result)
        self.assertNotIn(\'nm\', result)


if __name__ == \'__main__\':
    unittest.main()
'''


def create_initial():
    # Remove any existing project directory
    run_cmd(f'rm -rf "{PROJECT_DIR}"')
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Set up git environment variables
    git_env = os.environ.copy()
    git_env['GIT_AUTHOR_NAME'] = 'Dev Team'
    git_env['GIT_AUTHOR_EMAIL'] = 'dev@example.com'
    git_env['GIT_COMMITTER_NAME'] = 'Dev Team'
    git_env['GIT_COMMITTER_EMAIL'] = 'dev@example.com'

    def git(cmd, date='2025-01-10T09:00:00'):
        env = git_env.copy()
        env['GIT_AUTHOR_DATE'] = date
        env['GIT_COMMITTER_DATE'] = date
        return run_cmd(f'git {cmd}', cwd=PROJECT_DIR, env=env)

    def write_file(name, content):
        with open(f'{PROJECT_DIR}/{name}', 'w') as f:
            f.write(content)

    # ---- Initialize repo on main ----
    git('init')
    git('config user.email "dev@example.com"')
    git('config user.name "Dev Team"')

    # Write initial files
    write_file('parser.py', PARSER_MAIN)
    write_file('utils.py', UTILS)
    write_file('README.md', README)
    write_file('test_parser.py', TEST_PARSER)

    git('add .')
    git('commit -m "Initial commit: add parser module with JSON/CSV support"')

    # Rename branch to 'main' regardless of git default
    run_cmd('git branch -M main', cwd=PROJECT_DIR)

    write_file('requirements.txt',
               '# No external dependencies required\n# Standard library only\n')
    git('add requirements.txt', date='2025-01-12T10:30:00')
    git('commit -m "Add requirements.txt"', date='2025-01-12T10:30:00')

    # Save the main HEAD commit hash to branch hotfix from here later
    result = run_cmd('git rev-parse HEAD', cwd=PROJECT_DIR)
    main_head = result.stdout.strip()

    # ---- develop branch (from main) ----
    git('checkout -b develop', date='2025-01-13T11:00:00')
    write_file('parser.py', PARSER_DEVELOP)
    git('add parser.py', date='2025-01-13T11:00:00')
    git('commit -m "develop: add batch_parse() for bulk processing"',
        date='2025-01-13T11:00:00')

    # ---- feature/v2-parser branch (from develop) ----
    git('checkout -b feature/v2-parser', date='2025-01-15T09:00:00')

    # First commit on feature/v2-parser - still working
    write_file('parser.py', PARSER_FEATURE_V1)
    git('add parser.py', date='2025-01-15T09:00:00')
    git('commit -m "feature/v2-parser: add TSV support and stream_parse()"',
        date='2025-01-15T09:00:00')

    # Second commit on feature/v2-parser - THE REGRESSION
    write_file('parser.py', PARSER_FEATURE_V2_BROKEN)
    git('add parser.py', date='2025-01-16T14:30:00')
    git('commit -m "feature/v2-parser: refactor parse_data() to return metadata dict with records and count"',
        date='2025-01-16T14:30:00')

    # ---- hotfix/parser-fix branch (from main, not develop or feature) ----
    # Checkout the main HEAD commit hash directly, then create branch
    run_cmd(f'git checkout -b hotfix/parser-fix {main_head}', cwd=PROJECT_DIR)
    write_file('parser.py', PARSER_HOTFIX)
    git('add parser.py', date='2025-01-17T10:00:00')
    git('commit -m "hotfix/parser-fix: add input sanitization and improve error messages"',
        date='2025-01-17T10:00:00')

    # Return to main branch for the initial state the agent will see
    run_cmd('git checkout main', cwd=PROJECT_DIR)

    print(f'Project created: {PROJECT_DIR}')

    result = run_cmd('git branch -a', cwd=PROJECT_DIR)
    print(f'Branches:\n{result.stdout}')

    result = run_cmd('git log --oneline --all --graph', cwd=PROJECT_DIR)
    print(f'Git log:\n{result.stdout}')

    # GUI-ready startup: open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=3.0)
    print('GUI_READY: launched VSCode with project folder using DISPLAY=:0')


create_initial()
