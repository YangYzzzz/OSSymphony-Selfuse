from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


@dataclass
class AppMemoryRecentTask:
    task_id: str | None = None
    feature_tags: List[str] = field(default_factory=list)
    category: str | None = None
    instruction_summary: str = ""
    preflight_passed: bool = True

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppMemoryRecentTask":
        feature_tags = data.get("feature_tags") if isinstance(data.get("feature_tags"), list) else []
        return cls(
            task_id=str(data["task_id"]) if data.get("task_id") is not None else None,
            feature_tags=[str(tag) for tag in feature_tags],
            category=str(data["category"]) if data.get("category") is not None else None,
            instruction_summary=str(data.get("instruction_summary") or ""),
            preflight_passed=bool(data.get("preflight_passed", True)),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "feature_tags": self.feature_tags,
            "category": self.category,
            "instruction_summary": self.instruction_summary,
            "preflight_passed": self.preflight_passed,
        }


@dataclass
class AppMemory:
    app: str
    covered_features: Dict[str, int] = field(default_factory=dict)
    recent_tasks: List[AppMemoryRecentTask] = field(default_factory=list)
    verification_experience: Dict[str, Any] = field(default_factory=dict)
    next_generation_bias: Dict[str, Any] = field(default_factory=dict)
    co_use_counts: Dict[str, int] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, app: str, data: Dict[str, Any] | None) -> "AppMemory":
        data = data or {}
        covered_features = data.get("covered_features") if isinstance(data.get("covered_features"), dict) else {}
        recent_tasks = data.get("recent_tasks") if isinstance(data.get("recent_tasks"), list) else []
        verification_experience = data.get("verification_experience") if isinstance(data.get("verification_experience"), dict) else {}
        next_generation_bias = data.get("next_generation_bias") if isinstance(data.get("next_generation_bias"), dict) else {}
        co_use_counts = data.get("co_use_counts") if isinstance(data.get("co_use_counts"), dict) else {}
        return cls(
            app=str(data.get("app") or app),
            covered_features={str(key): cls._int_or_default(value, 0) for key, value in covered_features.items()},
            recent_tasks=[AppMemoryRecentTask.from_dict(item) for item in recent_tasks if isinstance(item, dict)],
            verification_experience=verification_experience,
            next_generation_bias=next_generation_bias,
            co_use_counts={str(key): cls._int_or_default(value, 0) for key, value in co_use_counts.items()},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "app": self.app,
            "covered_features": self.covered_features,
            "recent_tasks": [task.to_dict() for task in self.recent_tasks],
            "verification_experience": self.verification_experience,
            "next_generation_bias": self.next_generation_bias,
            "co_use_counts": self.co_use_counts,
        }

    def proposal_summary(self) -> Dict[str, Any]:
        return {
            "covered_features": self.covered_features,
            "next_generation_bias": self.next_generation_bias,
            "recent_tasks": [task.to_dict() for task in self.recent_tasks[-8:]],
        }

    def evaluator_summary(self) -> Dict[str, Any]:
        return {"verification_experience": self.verification_experience}

    def record_finalized(self, task: Dict[str, Any]) -> None:
        feature_tags = task.get("feature_tags") or task.get("target_features") or []
        feature_tags = feature_tags if isinstance(feature_tags, list) else []
        normalized_tags = [str(tag) for tag in feature_tags]
        for tag in normalized_tags:
            self.covered_features[tag] = int(self.covered_features.get(tag, 0)) + 1
        self.recent_tasks.append(
            AppMemoryRecentTask(
                task_id=str(task["id"]) if task.get("id") is not None else None,
                feature_tags=normalized_tags,
                category=str(task["category"]) if task.get("category") is not None else None,
                instruction_summary=str(task.get("instruction") or task.get("description") or "")[:180],
                preflight_passed=True,
            )
        )
        self.recent_tasks = self.recent_tasks[-30:]
        self.record_co_use(task.get("related_apps") if isinstance(task.get("related_apps"), list) else [])
        self.update_bias()

    def record_co_use(self, related_apps: List[str]) -> None:
        for app in related_apps:
            app = str(app)
            if app and app != self.app:
                self.co_use_counts[app] = int(self.co_use_counts.get(app, 0)) + 1

    def update_bias(self) -> None:
        if not self.covered_features:
            self.next_generation_bias = {}
            return
        ordered = sorted(self.covered_features.items(), key=lambda item: item[1])
        self.next_generation_bias = {
            "undercovered_features": [key for key, _ in ordered[:5]],
            "overcovered_features": [key for key, _ in ordered[-5:]],
        }

    @staticmethod
    def _int_or_default(value: Any, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default


@dataclass
class WorkflowSharedState:
    rollout_id: str
    sampled_apps: List[str]
    app_file_support: Dict[str, List[str]]
    sampled_files: List[Dict[str, Any]]
    app_tutorials: Dict[str, str]
    app_memory: Dict[str, Any]
    app_versions: Dict[str, str]
    app_open_commands: Dict[str, List[List[str]]]
    input_screen_size: Tuple[int, int]
    initial_config: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def candidate_file_paths(self) -> List[str]:
        paths: List[str] = []
        for item in self.sampled_files:
            if isinstance(item, dict) and item.get("path"):
                paths.append(str(item["path"]))
        return paths




@dataclass
class VerificationSpec:
    need_rule_judge: bool = False
    need_vlm_judge: bool = False
    vlm_desc: str = ""
    rule_items: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any] | None) -> "VerificationSpec":
        data = data or {}
        rule_items = data.get("rule_items") or []
        return cls(
            need_rule_judge=bool(data.get("need_rule_judge")),
            need_vlm_judge=bool(data.get("need_vlm_judge")),
            vlm_desc=str(data.get("vlm_desc", "")),
            rule_items=rule_items if isinstance(rule_items, list) else [],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "need_rule_judge": self.need_rule_judge,
            "need_vlm_judge": self.need_vlm_judge,
            "vlm_desc": self.vlm_desc,
            "rule_items": self.rule_items,
        }


@dataclass
class ProposalCandidate:
    proposal_id: str = ""
    instruction: str = ""
    config: List[Dict[str, Any]] = field(default_factory=list)
    related_apps: List[str] = field(default_factory=list)
    used_files: List[str] = field(default_factory=list)
    category: str = "mixed"
    complexity: str = "medium"
    estimated_steps: int = -1
    target_features: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    evaluation_requirements_text: List[str] = field(default_factory=list)
    verification_plan_hint: Dict[str, Any] = field(default_factory=dict)
    risk_notes: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any] | None) -> "ProposalCandidate":
        data = data or {}
        return cls(
            proposal_id=str(data.get("proposal_id") or ""),
            instruction=str(data.get("instruction") or data.get("description") or ""),
            config=cls._list_of_dicts(data.get("config")),
            related_apps=[str(app) for app in cls._list_or_default(data.get("related_apps"))],
            used_files=[str(path) for path in cls._list_or_default(data.get("used_files"))],
            category=str(data.get("category") or "mixed"),
            complexity=str(data.get("complexity") or "medium"),
            estimated_steps=cls._int_or_default(data.get("estimated_steps"), -1),
            target_features=[str(tag) for tag in cls._list_or_default(data.get("target_features") or data.get("feature_tags"))],
            success_criteria=[str(item) for item in cls._list_or_default(data.get("success_criteria"))],
            evaluation_requirements_text=[str(item) for item in cls._list_or_default(data.get("evaluation_requirements_text"))],
            verification_plan_hint=data.get("verification_plan_hint") if isinstance(data.get("verification_plan_hint"), dict) else {},
            risk_notes=[str(item) for item in cls._list_or_default(data.get("risk_notes"))],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "instruction": self.instruction,
            "config": self.config,
            "related_apps": self.related_apps,
            "used_files": self.used_files,
            "category": self.category,
            "complexity": self.complexity,
            "estimated_steps": self.estimated_steps,
            "target_features": self.target_features,
            "success_criteria": self.success_criteria,
            "evaluation_requirements_text": self.evaluation_requirements_text,
            "verification_plan_hint": self.verification_plan_hint,
            "risk_notes": self.risk_notes,
        }

    @staticmethod
    def _list_or_default(value: Any) -> List[Any]:
        return value if isinstance(value, list) else []

    @staticmethod
    def _list_of_dicts(value: Any) -> List[Dict[str, Any]]:
        return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []

    @staticmethod
    def _int_or_default(value: Any, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default


@dataclass
class TaskCandidate:
    instruction: str
    config: List[Dict[str, Any]] = field(default_factory=list)
    complexity: str = "medium"
    category: str = "mixed"
    estimated_steps: int = -1
    related_apps: List[str] = field(default_factory=list)
    used_files: List[str] = field(default_factory=list)
    feature_tags: List[str] = field(default_factory=list)
    verification: VerificationSpec = field(default_factory=VerificationSpec)

    @classmethod
    def from_proposal(cls, proposal: Dict[str, Any] | ProposalCandidate, verification: Dict[str, Any] | None = None) -> "TaskCandidate":
        proposal_model = proposal if isinstance(proposal, ProposalCandidate) else ProposalCandidate.from_dict(proposal)
        return cls(
            instruction=proposal_model.instruction,
            config=proposal_model.config,
            complexity=proposal_model.complexity,
            category=proposal_model.category,
            estimated_steps=proposal_model.estimated_steps,
            related_apps=proposal_model.related_apps,
            used_files=proposal_model.used_files,
            feature_tags=proposal_model.target_features,
            verification=VerificationSpec.from_dict(verification),
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any], proposal: Dict[str, Any] | ProposalCandidate | None = None) -> "TaskCandidate":
        base = cls.from_proposal(proposal or {}, data.get("verification"))
        merged = base.to_dict()
        merged.update(data)
        return cls(
            instruction=str(merged.get("instruction") or ""),
            config=cls._list_or_default(merged.get("config")),
            complexity=str(merged.get("complexity", "medium")),
            category=str(merged.get("category", "mixed")),
            estimated_steps=cls._int_or_default(merged.get("estimated_steps"), -1),
            related_apps=[str(app) for app in cls._list_or_default(merged.get("related_apps"))],
            used_files=[str(path) for path in cls._list_or_default(merged.get("used_files"))],
            feature_tags=[str(tag) for tag in cls._list_or_default(merged.get("feature_tags"))],
            verification=VerificationSpec.from_dict(merged.get("verification")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instruction": self.instruction,
            "config": self.config,
            "complexity": self.complexity,
            "category": self.category,
            "estimated_steps": self.estimated_steps,
            "related_apps": self.related_apps,
            "used_files": self.used_files,
            "feature_tags": self.feature_tags,
            "verification": self.verification.to_dict(),
        }


@dataclass
class ProposalSelectionInput:
    target_count: int
    sampled_apps: List[str]
    app_file_support: Dict[str, List[str]]
    sampled_files: List[Dict[str, Any]]
    app_memory_summary: Dict[str, Any]
    proposals: List[ProposalCandidate]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_count": self.target_count,
            "sampled_apps": self.sampled_apps,
            "app_file_support": self.app_file_support,
            "sampled_files": self.sampled_files,
            "app_memory_summary": self.app_memory_summary,
            "proposals": [proposal.to_dict() for proposal in self.proposals],
        }


@dataclass
class ExplorationResult:
    proposals: List[ProposalCandidate] = field(default_factory=list)
    generation_notes: List[str] = field(default_factory=list)
    trajectory: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any] | None) -> "ExplorationResult":
        data = data or {}
        proposals = data.get("proposals") if isinstance(data.get("proposals"), list) else []
        generation_notes = data.get("generation_notes") if isinstance(data.get("generation_notes"), list) else []
        trajectory = data.get("trajectory") if isinstance(data.get("trajectory"), dict) else {}
        return cls(
            proposals=[ProposalCandidate.from_dict(item) for item in proposals if isinstance(item, dict)],
            generation_notes=[str(item) for item in generation_notes],
            trajectory=trajectory,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposals": [proposal.to_dict() for proposal in self.proposals],
            "generation_notes": self.generation_notes,
            "trajectory": self.trajectory,
        }


@dataclass
class ExplorationContext:
    trajectory: Dict[str, Any] = field(default_factory=dict)
    generation_notes: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any] | None) -> "ExplorationContext":
        data = data or {}
        return cls(
            trajectory=data.get("trajectory") if isinstance(data.get("trajectory"), dict) else {},
            generation_notes=[str(item) for item in data.get("generation_notes", [])] if isinstance(data.get("generation_notes"), list) else [],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trajectory": self.trajectory,
            "generation_notes": self.generation_notes,
        }


@dataclass
class VerificationSynthesisInput:
    proposal: ProposalCandidate
    sampled_apps: List[str]
    app_versions: Dict[str, str]
    app_file_support: Dict[str, List[str]]
    sampled_files: List[Dict[str, Any]]
    app_tutorials: Dict[str, str]
    verification_experience: Dict[str, Any]
    exploration_context: ExplorationContext = field(default_factory=ExplorationContext)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal": self.proposal.to_dict(),
            "sampled_apps": self.sampled_apps,
            "app_versions": self.app_versions,
            "app_file_support": self.app_file_support,
            "sampled_files": self.sampled_files,
            "app_tutorials": self.app_tutorials,
            "verification_experience": self.verification_experience,
            "exploration_context": self.exploration_context.to_dict(),
        }


@dataclass
class VerificationRepairInput:
    candidate: TaskCandidate
    failure: Dict[str, Any]
    sampled_apps: List[str]
    app_file_support: Dict[str, List[str]]
    sampled_files: List[Dict[str, Any]]
    exploration_context: ExplorationContext = field(default_factory=ExplorationContext)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate": self.candidate.to_dict(),
            "failure": self.failure,
            "sampled_apps": self.sampled_apps,
            "app_file_support": self.app_file_support,
            "sampled_files": self.sampled_files,
            "exploration_context": self.exploration_context.to_dict(),
        }


@dataclass
class AcceptedProposalWorkItem:
    proposal: ProposalCandidate
    exploration_result: ExplorationResult


@dataclass
class GenerationRunLog:
    time: str
    rollout_id: str
    sampled_apps: List[str]
    app_file_support: Dict[str, List[str]]
    sampled_files: List[Dict[str, Any]]
    initial_config: List[Dict[str, Any]]
    exploration_result: Dict[str, Any]
    accepted_count: int
    generated_ids: List[str]
    failures: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "time": self.time,
            "rollout_id": self.rollout_id,
            "sampled_apps": self.sampled_apps,
            "app_file_support": self.app_file_support,
            "sampled_files": self.sampled_files,
            "initial_config": self.initial_config,
            "exploration_result": self.exploration_result,
            "accepted_count": self.accepted_count,
            "generated_ids": self.generated_ids,
            "failures": self.failures,
        }
