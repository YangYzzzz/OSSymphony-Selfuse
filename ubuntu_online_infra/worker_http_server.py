#!/usr/bin/env python3

import subprocess
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

REMOTE_START_SCRIPT = "/nvme/yangbowen/OSSymphony/scripts/rl_env/run_worker_envs.sh"
REMOTE_STOP_SCRIPT = "/nvme/yangbowen/OSSymphony/scripts/rl_env/stop_worker_envs.sh"

app = FastAPI(title="Worker Env HTTP Server")


class StartRequest(BaseModel):
    NUM_ENVS: Optional[int] = 1  # 可选，默认 1
    WORKER_URL: Optional[str]
    WORKER_ID: Optional[str]

class CmdResult(BaseModel):
    cmd: str
    returncode: int
    stdout: str
    stderr: str


def run_cmd(cmd: List[str]) -> CmdResult:
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = proc.communicate()
        return CmdResult(
            cmd=" ".join(cmd),
            returncode=proc.returncode,
            stdout=stdout.decode("utf-8", errors="ignore"),
            stderr=stderr.decode("utf-8", errors="ignore"),
        )
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Failed to run cmd: {e}")


@app.post("/start", response_model=CmdResult)
def start_workers(req: StartRequest):
    print(f'Request: {req}')
    num_envs = req.NUM_ENVS or 1
    worker_url = req.WORKER_URL
    worker_id = req.WORKER_ID
    
    if num_envs <= 0:
        raise HTTPException(status_code=400, detail="NUM_ENVS must be positive")

    cmd = ["bash", REMOTE_START_SCRIPT, str(num_envs), str(worker_id), str(worker_url)]
    result = run_cmd(cmd)
    if result.returncode != 0:
        # 启动失败也返回 500，便于客户端感知
        raise HTTPException(
            status_code=500,
            detail={
                "message": "start script failed",
                "cmd": result.cmd,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )
    return result


@app.post("/stop", response_model=CmdResult)
def stop_workers():
    cmd = ["bash", REMOTE_STOP_SCRIPT]
    result = run_cmd(cmd)
    if result.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "stop script failed",
                "cmd": result.cmd,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )
    return result


# 方便直接 python 运行调试
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10001)

