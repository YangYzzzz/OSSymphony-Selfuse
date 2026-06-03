"""
Initial Setup: Add JSON schema validation for config.json
Task ID: vscode_lp_019
Domain: vscode
"""

import json
import os
import shlex
import subprocess
import time

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_019'
PROJECT_DIR = f'{WORKDIR}/{TASK_ID}'
CONFIG_PATH = f'{PROJECT_DIR}/config.json'
SCHEMA_DIR = f'{PROJECT_DIR}/schemas'
SCHEMA_PATH = f'{SCHEMA_DIR}/config-schema.json'


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
    # Create project directory structure
    os.makedirs(SCHEMA_DIR, exist_ok=True)

    # Create config.json — a realistic application config WITHOUT $schema
    config = {
        "appName": "DataPipeline Pro",
        "version": "2.4.1",
        "environment": "production",
        "server": {
            "host": "0.0.0.0",
            "port": 8080,
            "ssl": True,
            "certPath": "/etc/ssl/certs/app.pem"
        },
        "database": {
            "driver": "postgresql",
            "host": "db.internal.example.com",
            "port": 5432,
            "name": "pipeline_prod",
            "pool": {
                "min": 5,
                "max": 20,
                "idleTimeoutMs": 30000
            }
        },
        "logging": {
            "level": "info",
            "format": "json",
            "outputDir": "./logs",
            "rotateEveryMb": 50,
            "maxFiles": 10
        },
        "features": {
            "enableBetaUI": False,
            "maxUploadSizeMb": 100,
            "allowedOrigins": [
                "https://app.example.com",
                "https://admin.example.com"
            ],
            "rateLimiting": {
                "enabled": True,
                "requestsPerMinute": 120,
                "burstSize": 30
            }
        },
        "notifications": {
            "email": {
                "enabled": True,
                "smtpHost": "smtp.example.com",
                "smtpPort": 587,
                "fromAddress": "noreply@example.com"
            },
            "slack": {
                "enabled": False,
                "webhookUrl": ""
            }
        }
    }

    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
    print(f'Created config.json at {CONFIG_PATH}')

    # Create JSON schema that validates config.json
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "DataPipeline Pro Configuration",
        "description": "Schema for DataPipeline Pro application configuration",
        "type": "object",
        "required": ["appName", "version", "environment", "server", "database"],
        "properties": {
            "$schema": {
                "type": "string",
                "description": "Path to the JSON schema file"
            },
            "appName": {
                "type": "string",
                "minLength": 1
            },
            "version": {
                "type": "string",
                "pattern": "^\\d+\\.\\d+\\.\\d+$"
            },
            "environment": {
                "type": "string",
                "enum": ["development", "staging", "production"]
            },
            "server": {
                "type": "object",
                "required": ["host", "port"],
                "properties": {
                    "host": {"type": "string"},
                    "port": {"type": "integer", "minimum": 1, "maximum": 65535},
                    "ssl": {"type": "boolean"},
                    "certPath": {"type": "string"}
                },
                "additionalProperties": False
            },
            "database": {
                "type": "object",
                "required": ["driver", "host", "port", "name"],
                "properties": {
                    "driver": {
                        "type": "string",
                        "enum": ["postgresql", "mysql", "sqlite"]
                    },
                    "host": {"type": "string"},
                    "port": {"type": "integer"},
                    "name": {"type": "string"},
                    "pool": {
                        "type": "object",
                        "properties": {
                            "min": {"type": "integer", "minimum": 1},
                            "max": {"type": "integer", "minimum": 1},
                            "idleTimeoutMs": {"type": "integer", "minimum": 0}
                        }
                    }
                }
            },
            "logging": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "string",
                        "enum": ["debug", "info", "warn", "error"]
                    },
                    "format": {
                        "type": "string",
                        "enum": ["json", "text"]
                    },
                    "outputDir": {"type": "string"},
                    "rotateEveryMb": {"type": "integer", "minimum": 1},
                    "maxFiles": {"type": "integer", "minimum": 1}
                }
            },
            "features": {
                "type": "object",
                "properties": {
                    "enableBetaUI": {"type": "boolean"},
                    "maxUploadSizeMb": {"type": "integer", "minimum": 1},
                    "allowedOrigins": {
                        "type": "array",
                        "items": {"type": "string", "format": "uri"}
                    },
                    "rateLimiting": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "requestsPerMinute": {"type": "integer", "minimum": 1},
                            "burstSize": {"type": "integer", "minimum": 1}
                        }
                    }
                }
            },
            "notifications": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "smtpHost": {"type": "string"},
                            "smtpPort": {"type": "integer"},
                            "fromAddress": {"type": "string", "format": "email"}
                        }
                    },
                    "slack": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "webhookUrl": {"type": "string"}
                        }
                    }
                }
            }
        }
    }

    with open(SCHEMA_PATH, 'w') as f:
        json.dump(schema, f, indent=4)
    print(f'Created schema at {SCHEMA_PATH}')

    # Launch VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')


create_initial()
