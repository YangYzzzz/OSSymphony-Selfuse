import argparse
import json
import math
import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from tqdm import tqdm

import numpy as np
from openai import OpenAI


###############################################################################
# 文本预处理与相似度计算（基于 Embedding）
###############################################################################


def _normalize_text(s: str) -> str:
    """简单归一化：小写、去首尾空白、合并空白。"""

    if not s:
        return ""
    s = s.lower().strip()
    # 统一空白
    return " ".join(s.split())


def _cosine_sim_vec(a: np.ndarray, b: np.ndarray) -> float:
    """余弦相似度，输入为 numpy 向量。"""

    if a.size == 0 or b.size == 0:
        return 0.0
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0.0 or nb == 0.0:
        return 0.0
    return float(a.dot(b) / (na * nb))


###############################################################################
# 数据结构
###############################################################################


@dataclass
class TaskRecord:
    domain: str
    file_path: Path
    instruction: str
    embedding: np.ndarray | None = None


###############################################################################
# 加载任务
###############################################################################


def _iter_task_json_files(root_dir: Path) -> Iterable[Tuple[str, Path]]:
    """遍历 root_dir 下所有 domain 子目录的 .json 任务文件。

    返回 (domain_name, json_file_path)。
    """

    if not root_dir.exists() or not root_dir.is_dir():
        return

    for domain_dir in sorted(p for p in root_dir.iterdir() if p.is_dir()):
        domain = domain_dir.name
        for json_path in sorted(domain_dir.glob("*.json")):
            if json_path.is_file():
                yield domain, json_path


def _load_tasks(root_dir: Path) -> List[TaskRecord]:
    records: List[TaskRecord] = []
    for domain, path in _iter_task_json_files(root_dir):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        inst = data.get("instruction") or data.get("description") or ""
        if not isinstance(inst, str):
            inst = str(inst)
        # 这里只做归一化，不做本地向量化，embedding 在后面统一批量计算
        norm = _normalize_text(inst)
        records.append(
            TaskRecord(
                domain=domain,
                file_path=path,
                instruction=norm,
            )
        )
    return records


###############################################################################
# 过滤逻辑（使用 doubao-embedding-large-text-240915）
###############################################################################


def _build_embeddings(records: List[TaskRecord], model: str = "doubao-embedding-large-text-240915", base_url: str = None, api_key: str = None) -> None:
    """调用 OpenAI 兼容接口，使用 embedding 模型，为所有任务计算向量。"""
    assert base_url and api_key
    if not records:
        return

    client = OpenAI(base_url=base_url, api_key=api_key)

    batch_size = 128
    for i in tqdm(range(0, len(records), batch_size)):
        batch = records[i : i + batch_size]
        texts = [r.instruction for r in batch]
        for _ in range(10):
            try:
                resp = client.embeddings.create(model=model, input=texts)
                break
            except Exception:
                continue
        for item, rec in zip(resp.data, batch):
            rec.embedding = np.array(item.embedding, dtype=np.float32)


def filter_duplicates(
    tasks: List[TaskRecord],
    domain_sim_threshold: float = 0.7,
    overall_sim_threshold: float = 0.9,
    model: str = "doubao-embedding-large-text-240915",
    base_url: str = None,
    api_key: str = None,
) -> List[TaskRecord]:
    """两阶段基于 embedding 的去重。

    1. 先在 domain 内部用较低阈值过滤（更严格）；
       - 使用“代表样本”策略：一个簇中只保留一个代表，其余视作重复；
    2. 再在全局用较高阈值过滤跨 domain 的重复；
       - 同样使用代表样本；

    这样每个最终簇只会保留 1 条指令，更符合“高相似度就压缩掉”的需求，
    并且顺序影响只体现在“谁当代表”，不影响“删掉哪些语义簇”。
    """

    if not tasks:
        return []

    # 先算 embedding
    _build_embeddings(tasks, model=model, base_url=base_url, api_key=api_key)

    # 过滤掉没 embedding 的（直接全部保留），避免误删
    tasks_with_emb = [t for t in tasks if t.embedding is not None]
    tasks_no_emb = [t for t in tasks if t.embedding is None]

    if not tasks_with_emb:
        return tasks_no_emb

    # --------------- 第一阶段：按 domain 内部代表式去重 ---------------
    # domain -> List[TaskRecord]
    domain_buckets: Dict[str, List[TaskRecord]] = defaultdict(list)
    for t in tasks_with_emb:
        domain_buckets[t.domain].append(t)

    # 第一阶段结果：每个 domain 内部保留的代表样本
    domain_stage_kept: List[TaskRecord] = []

    for d, recs in domain_buckets.items():
        # 为了稳定性，可以固定顺序：按指令长度从短到长
        recs_sorted = sorted(recs, key=lambda r: len(r.instruction or ""))
        kept_in_domain: List[TaskRecord] = []
        for r in recs_sorted:
            is_dup = False
            for k in kept_in_domain:
                sim = _cosine_sim_vec(r.embedding, k.embedding)
                if sim >= domain_sim_threshold:
                    # 与已有代表高度相似 => 视为重复，不再保留
                    is_dup = True
                    break
            if not is_dup:
                kept_in_domain.append(r)
        domain_stage_kept.extend(kept_in_domain)

    # --------------- 第二阶段：跨 domain 代表之间再做去重 ---------------
    # 作用对象是“domain 内部已去重后的代表集合”
    reps_sorted = sorted(domain_stage_kept, key=lambda r: len(r.instruction or ""))
    final_kept_reps: List[TaskRecord] = []
    for r in reps_sorted:
        is_dup = False
        for k in final_kept_reps:
            sim = _cosine_sim_vec(r.embedding, k.embedding)
            if sim >= overall_sim_threshold:
                is_dup = True
                break
        if not is_dup:
            final_kept_reps.append(r)

    # 最终：只保留代表样本，加上所有没 embedding 的
    kept: List[TaskRecord] = []
    kept.extend(final_kept_reps)
    kept.extend(tasks_no_emb)

    return kept


###############################################################################
# 主流程：读取 -> 去重 -> 复制到 filtered 目录
###############################################################################


def main():
    parser = argparse.ArgumentParser(
        description="Filter duplicated OS-Caliber tasks under root_dir"
    )
    parser.add_argument(
        "--root_dir",
        type=str,
        required=True,
        help=(
            "根目录，结构为 root_dir/domain/*.json，例如 "
            "evaluation_examples/ubuntu_online_rollout/synthesis/oscaliber_os-caliber-gemini-3.1-pro-preview-generate-multiapp-3000-0402"
        ),
    )
    parser.add_argument(
        "--domain-sim-threshold",
        type=float,
        default=0.7,
        help="Domain内部重复判定的相似度阈值, 范围 (0,1]，越高越严格，默认 0.7",
    )
    parser.add_argument(
        "--overall-sim-threshold",
        type=float,
        default=0.9,
        help="整体重复判定的相似度阈值, 范围 (0,1]，越高越严格，默认 0.9",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="doubao-embedding-large-text-240915"
    )
    parser.add_argument(
        "--base_url",
        type=str,
        required=True
    )
    parser.add_argument(
        "--api_key",
        type=str,
        required=True
    )

    args = parser.parse_args()
    root_dir = Path(args.root_dir).expanduser().resolve()

    tasks = _load_tasks(root_dir)
    total = len(tasks)
    if total == 0:
        print(f"[task_filter] No tasks found under {root_dir}")
        return

    kept = filter_duplicates(tasks, 
                             domain_sim_threshold=args.domain_sim_threshold, 
                             overall_sim_threshold=args.overall_sim_threshold, 
                             model=args.model, 
                             base_url=args.base_url, 
                             api_key=args.api_key
                            )

    # 统计每个 domain 的保留/删除数量
    domain_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: {"total": 0, "kept": 0, "removed": 0})
    for r in tasks:
        st = domain_stats[r.domain]
        st["total"] += 1
    for r in kept:
        st = domain_stats[r.domain]
        st["kept"] += 1
    for d, st in domain_stats.items():
        st["removed"] = st["total"] - st["kept"]

    print(f"[task_filter] Root dir: {root_dir}")
    print(f"[task_filter] Total tasks: {total}; kept: {len(kept)}; removed: {total - len(kept)}")
    print("[task_filter] Per-domain stats:")
    for d in sorted(domain_stats.keys()):
        st = domain_stats[d]
        print(
            f"  - {d}: total={st['total']}, kept={st['kept']}, removed={st['removed']}"
        )

    # 将保留的 json 拷贝到新的 filtered 目录结构中
    filtered_root = root_dir.parent / f"{root_dir.name}_filtered"
    filtered_root.mkdir(parents=True, exist_ok=True)

    copied = 0
    test_all_json = {}
    for r in kept:
        rel_domain = r.domain
        src = r.file_path
        dst_domain_dir = filtered_root / rel_domain
        dst_domain_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_domain_dir / src.name
        if rel_domain not in test_all_json:
            test_all_json[rel_domain] = []
        test_all_json[rel_domain].append(src.name.split(".")[0])
        try:
            # 使用二进制拷贝
            with src.open("rb") as f_src, dst.open("wb") as f_dst:
                f_dst.write(f_src.read())
            copied += 1
        except Exception as e:
            print(f"[task_filter] Failed to copy {src} -> {dst}: {e}")

    with open(os.path.join(filtered_root, "test_all.json"), "w") as f:
        json.dump(test_all_json, f, indent=4, ensure_ascii=False)
        
    print(f"[task_filter] Copied {copied} kept task files to {filtered_root}")


if __name__ == "__main__":
    main()
