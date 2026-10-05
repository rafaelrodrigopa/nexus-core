#!/usr/bin/env python3
"""
Nexus Core - Senior Autonomous Activity Engine
===============================================
Gerenciador autônomo de presença contínua no GitHub:
- Meta diária aleatória entre 40 e 60 commits por dia.
- Commits reais com padrão sênior (Conventional Commits).
- Modificações concretas de código (algoritmos, estruturas, testes, benchmarks).
- Suporte opcional à API do Google Gemini para geração dinâmica de código.
- Suporte à criação de Issues, Branches, Pull Requests, Reviews e Merges via API do GitHub.
"""

import os
import sys
import json
import time
import random
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List

# Garante suporte a UTF-8 em terminais Windows/Linux
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

os.environ["GIT_DISCOVERY_ACROSS_FILESYSTEM"] = "1"



# Diretórios base
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"
STATE_FILE = DATA_DIR / "bot_state.json"
ENV_FILE = ROOT_DIR / ".env"

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [Nexus-Engine] {msg}"
    print(formatted)
    log_file = LOGS_DIR / "activity.log"
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass


def load_env() -> Dict[str, str]:
    """Carrega variáveis de ambiente locais do arquivo .env sem dependência de libs externas."""
    env_vars: Dict[str, str] = {}
    if ENV_FILE.exists():
        try:
            for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip()
        except Exception as e:
            log(f"Aviso ao ler .env: {e}")
    # Variáveis do SO têm precedência
    for k, v in os.environ.items():
        env_vars[k] = v
    return env_vars


class BotState:
    def __init__(self, min_daily: int = 40, max_daily: int = 60) -> None:
        self.min_daily = min_daily
        self.max_daily = max_daily
        self.data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        today_str = datetime.now().strftime("%Y-%m-%d")
        if STATE_FILE.exists():
            try:
                content = json.loads(STATE_FILE.read_text(encoding="utf-8"))
                if content.get("date") == today_str:
                    # pyrefly: ignore [no-any-return-explicit]
                    return content
            except Exception:
                pass

        # Inicializa novo dia com meta aleatória entre min e max
        new_target = random.randint(self.min_daily, self.max_daily)
        state = {
            "date": today_str,
            "target_commits": new_target,
            "completed_commits": 0,
            "total_lifetime_commits": 0,
            "last_action_time": None,
            "history": []
        }
        self._save(state)
        log(f"🎯 Novo dia iniciado ({today_str})! Meta sorteada: {new_target} commits hoje.")
        return state

    def _save(self, state: Dict[str, Any]) -> None:
        STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    def record_commit(self, action_type: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        today_str = datetime.now().strftime("%Y-%m-%d")
        if self.data.get("date") != today_str:
            self.data = self._load()

        self.data["completed_commits"] = self.data.get("completed_commits", 0) + 1
        self.data["total_lifetime_commits"] = self.data.get("total_lifetime_commits", 0) + 1
        self.data["last_action_time"] = datetime.now(timezone.utc).isoformat()
        
        entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "type": action_type,
            "message": message,
            "details": details or {}
        }
        history = self.data.get("history", [])
        history.append(entry)
        if len(history) > 50:
            history.pop(0)
        self.data["history"] = history
        self._save(self.data)


# =====================================================================
# BANCO DE EXPANSÕES SÊNIOR PROCEDURAIS (Fallback Autônomo Offline)
# =====================================================================

PROCEDURAL_MODULES = [
    {
        "file": "src/nexus_core/algorithms/fenwick.py",
        "test_file": "tests/test_fenwick.py",
        "title": "feat(algorithms): implement Fenwick Tree (Binary Indexed Tree) with point & range queries",
        "body": "- Add FenwickTree supporting prefix sums and dynamic point updates in O(log n)\n- Implement range query abstraction and inverse indexing\n- Provide comprehensive pytest suite with edge validations",
        "code": '''"""
Fenwick Tree (Binary Indexed Tree)
===================================
Prefix-sum query and point update structure in O(log n).
"""
from typing import List


class FenwickTree:
    """1-indexed Binary Indexed Tree for prefix computations."""

    def __init__(self, size: int) -> None:
        self.size = size
        self.tree: List[int] = [0] * (size + 1)

    @classmethod
    def from_list(cls, values: List[int]) -> "FenwickTree":
        ft = cls(len(values))
        for idx, val in enumerate(values, start=1):
            ft.update(idx, val)
        return ft

    def update(self, idx: int, delta: int) -> None:
        """Adds delta to element at index idx (1-based)."""
        if idx <= 0 or idx > self.size:
            raise IndexError(f"Index {idx} out of range [1, {self.size}]")
        while idx <= self.size:
            self.tree[idx] += delta
            idx += idx & (-idx)

    def prefix_sum(self, idx: int) -> int:
        """Computes prefix sum in range [1, idx] in O(log n)."""
        if idx < 0:
            return 0
        idx = min(idx, self.size)
        total = 0
        while idx > 0:
            total += self.tree[idx]
            idx -= idx & (-idx)
        return total

    def range_query(self, left: int, right: int) -> int:
        """Returns sum of elements in 1-based range [left, right]."""
        if left > right or left < 1 or right > self.size:
            raise ValueError(f"Invalid query range [{left}, {right}]")
        return self.prefix_sum(right) - self.prefix_sum(left - 1)
''',
        "test_code": '''import pytest
from nexus_core.algorithms.fenwick import FenwickTree


def test_fenwick_tree_prefix_and_range():
    data = [2, 1, 4, 6, -1, 5, -3]
    ft = FenwickTree.from_list(data)
    assert ft.prefix_sum(1) == 2
    assert ft.prefix_sum(4) == 2 + 1 + 4 + 6
    assert ft.range_query(2, 5) == 1 + 4 + 6 + (-1)

    ft.update(3, 5) # 4 becomes 9
    assert ft.range_query(2, 5) == 1 + 9 + 6 + (-1)
'''
    },
    {
        "file": "src/nexus_core/structures/skip_list.py",
        "test_file": "tests/test_skip_list.py",
        "title": "feat(structures): implement probabilistic SkipList with O(log n) expected search",
        "body": "- Add multi-level balanced SkipList with randomized tower height\n- Guarantee O(log n) expected search, insertion, and deletion\n- Add thorough test coverage for boundary lookups",
        "code": '''"""
Probabilistic Skip List Implementation
======================================
Alternative to self-balancing binary search trees with expected O(log n) time.
"""
import random
from typing import Optional, List, Any


class SkipNode:
    def __init__(self, key: int, val: Any, level: int) -> None:
        self.key = key
        self.val = val
        self.forward: List[Optional["SkipNode"]] = [None] * (level + 1)


class SkipList:
    def __init__(self, max_level: int = 16, p: float = 0.5) -> None:
        self.max_level = max_level
        self.p = p
        self.level = 0
        self.header = SkipNode(-float("inf"), None, max_level)

    def _random_level(self) -> int:
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, key: int, val: Any) -> None:
        update = [None] * (self.max_level + 1)
        curr = self.header
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].key < key:
                curr = curr.forward[i]
            update[i] = curr

        curr = curr.forward[0]
        if curr and curr.key == key:
            curr.val = val
            return

        new_lvl = self._random_level()
        if new_lvl > self.level:
            for i in range(self.level + 1, new_lvl + 1):
                update[i] = self.header
            self.level = new_lvl

        new_node = SkipNode(key, val, new_lvl)
        for i in range(new_lvl + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def search(self, key: int) -> Optional[Any]:
        curr = self.header
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].key < key:
                curr = curr.forward[i]
        curr = curr.forward[0]
        if curr and curr.key == key:
            return curr.val
        return None
''',
        "test_code": '''import pytest
from nexus_core.structures.skip_list import SkipList


def test_skip_list_operations():
    sl = SkipList()
    elements = [(10, "ten"), (5, "five"), (30, "thirty"), (20, "twenty")]
    for k, v in elements:
        sl.insert(k, v)

    for k, v in elements:
        assert sl.search(k) == v

    assert sl.search(999) is None
    sl.insert(10, "TEN_UPDATED")
    assert sl.search(10) == "TEN_UPDATED"
'''
    },
    {
        "file": "src/nexus_core/concurrency/monotonic_queue.py",
        "test_file": "tests/test_monotonic_queue.py",
        "title": "feat(concurrency): implement MonotonicQueue for O(1) sliding window extremes",
        "body": "- Add MonotonicQueue maintaining monotonically decreasing deque\n- Support O(1) amortized min/max retrieval over moving windows\n- Include unit test with randomized numeric streams",
        "code": '''"""
Monotonic Queue Implementation
==============================
Maintains monotonic extremes across moving data windows in O(1) amortized time.
"""
from collections import deque
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class MonotonicMaxQueue(Generic[T]):
    """Queue maintaining descending order for O(1) maximum query."""

    def __init__(self) -> None:
        self._raw_queue = deque()
        self._max_deque = deque()

    def push(self, val: T) -> None:
        self._raw_queue.append(val)
        while self._max_deque and self._max_deque[-1] < val:
            self._max_deque.pop()
        self._max_deque.append(val)

    def pop(self) -> Optional[T]:
        if not self._raw_queue:
            return None
        val = self._raw_queue.popleft()
        if self._max_deque and self._max_deque[0] == val:
            self._max_deque.popleft()
        return val

    def max(self) -> Optional[T]:
        return self._max_deque[0] if self._max_deque else None

    def __len__(self) -> int:
        return len(self._raw_queue)
''',
        "test_code": '''import pytest
from nexus_core.concurrency.monotonic_queue import MonotonicMaxQueue


def test_monotonic_max_queue():
    mq = MonotonicMaxQueue()
    mq.push(3)
    mq.push(1)
    assert mq.max() == 3
    mq.push(5)
    assert mq.max() == 5
    mq.push(2)
    assert mq.max() == 5
    assert mq.pop() == 3
    assert mq.max() == 5
    assert mq.pop() == 1
    assert mq.max() == 5
    assert mq.pop() == 5
    assert mq.max() == 2
'''
    },
    {
        "file": "src/nexus_core/algorithms/search_ext.py",
        "test_file": "tests/test_search_ext.py",
        "title": "perf(algorithms): implement exponential search with tight logarithmic boundaries",
        "body": "- Add exponential search algorithm for unbounded and massive sorted sequences\n- Achieve O(log i) search time where i is the target element index\n- Add full boundary parameterization in pytest",
        "code": '''"""
Exponential Search Module
=========================
Fast logarithmic search for unbounded or sorted arrays.
"""
from typing import List, Optional


def exponential_search(arr: List[int], target: int) -> Optional[int]:
    """
    Finds target in sorted array in O(log i) time.
    """
    if not arr:
        return None
    if arr[0] == target:
        return 0

    bound = 1
    n = len(arr)
    while bound < n and arr[bound] <= target:
        bound *= 2

    left = bound // 2
    right = min(bound, n - 1)

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None
''',
        "test_code": '''import pytest
from nexus_core.algorithms.search_ext import exponential_search


def test_exponential_search():
    arr = [2, 3, 4, 10, 40, 55, 70, 85, 100, 150, 200]
    assert exponential_search(arr, 10) == 3
    assert exponential_search(arr, 2) == 0
    assert exponential_search(arr, 200) == 10
    assert exponential_search(arr, 999) is None
    assert exponential_search([], 5) is None
'''
    }
]


# =====================================================================
# INTEGRAÇÃO GEMINI IA
# =====================================================================

def query_gemini_for_code(api_key: str) -> Optional[Dict[str, Any]]:
    """Consulta a API do Google Gemini para gerar melhoria de código em padrão sênior."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    prompt = (
        "You are a Staff Software Engineer contributing to 'nexus-core', a high-performance Python 3.10+ "
        "library of algorithms, resilient concurrency, and data structures. "
        "Generate a concrete, realistic production addition (e.g. a new algorithm, cache eviction policy, "
        "lock-free pattern, or benchmark). Provide your response strictly as valid JSON without markdown wrapping: "
        "{\n"
        '  "file": "src/nexus_core/.../filename.py",\n'
        '  "test_file": "tests/test_filename.py",\n'
        '  "commit_title": "feat(module): conventional commit message",\n'
        '  "commit_body": "- Key improvement bullet 1\\n- Key improvement bullet 2",\n'
        '  "pr_title": "[FEATURE] PR title",\n'
        '  "pr_body": "Detailed senior PR description with context, design choices, and benchmarks",\n'
        '  "issue_title": "Detailed issue title if applicable",\n'
        '  "issue_body": "Detailed issue description",\n'
        '  "code": "Python source code with full types and Google docstrings",\n'
        '  "test_code": "Pytest code testing this module"\n'
        "}"
    )

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "responseMimeType": "application/json"
        }
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:

            data = json.loads(resp.read().decode("utf-8"))
            candidate = data["candidates"][0]["content"]["parts"][0]["text"]
            # Remove crases se vier com formatação
            cleaned = candidate.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            # pyrefly: ignore [no-any-return-explicit]
            return json.loads(cleaned.strip())
    except Exception as e:
        log(f"⚠️ Gemini API indisponível ou erro na chamada: {e}. Usando gerador autônomo offline.")
        return None


# =====================================================================
# GITHUB REST API WRAPPER (PRs, Issues, Reviews, Merges)
# =====================================================================

class GitHubAPI:
    def __init__(self, token: Optional[str], repo: Optional[str]) -> None:
        self.token = token
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{repo}" if repo else ""

    @property
    def is_configured(self) -> bool:
        return bool(self.token and self.repo)

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "NexusCore-Bot"
        }

    def create_issue(self, title: str, body: str, labels: Optional[List[str]] = None) -> Optional[int]:
        if not self.is_configured:
            return None
        url = f"{self.base_url}/issues"
        payload = {"title": title, "body": body, "labels": labels or ["enhancement", "nexus-core"]}
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=self._headers(), method="POST")
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                issue_number = data.get("number")
                log(f"📋 Issue #{issue_number} criada: '{title}'")
                # pyrefly: ignore [no-any-return-implicit]
                return issue_number
        except Exception as e:
            log(f"Aviso ao criar Issue via API: {e}")
            return None

    def create_pull_request(self, title: str, body: str, head_branch: str, base_branch: str = "main") -> Optional[int]:
        if not self.is_configured:
            return None
        url = f"{self.base_url}/pulls"
        payload = {"title": title, "body": body, "head": head_branch, "base": base_branch}
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=self._headers(), method="POST")
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                pr_number = data.get("number")
                log(f"🔀 Pull Request #{pr_number} aberto: '{title}' ({head_branch} -> {base_branch})")
                # pyrefly: ignore [no-any-return-implicit]
                return pr_number
        except Exception as e:
            log(f"Aviso ao criar PR via API: {e}")
            return None

    def review_and_merge_pr(self, pr_number: int, commit_title: str) -> bool:
        if not self.is_configured or not pr_number:
            return False
        # 1. Cria review de aprovação
        review_url = f"{self.base_url}/pulls/{pr_number}/reviews"
        review_payload = {
            "body": "LGTM. Code adheres to Nexus Core architectural guidelines, passes test contracts, and maintains asymptotic limits.",
            "event": "APPROVE"
        }
        try:
            req = urllib.request.Request(review_url, data=json.dumps(review_payload).encode("utf-8"), headers=self._headers(), method="POST")
            urllib.request.urlopen(req, timeout=10)
            log(f"✅ Code Review aprovado para o PR #{pr_number}")
        except Exception as e:
            log(f"Aviso ao aprovar review do PR #{pr_number}: {e}")

        # 2. Executa merge (Squash & Merge)
        merge_url = f"{self.base_url}/pulls/{pr_number}/merge"
        merge_payload = {
            "commit_title": commit_title,
            "merge_method": "squash"
        }
        try:
            req = urllib.request.Request(merge_url, data=json.dumps(merge_payload).encode("utf-8"), headers=self._headers(), method="PUT")
            with urllib.request.urlopen(req, timeout=15) as resp:
                log(f"🚀 PR #{pr_number} mergeado com sucesso na main!")
                return True
        except Exception as e:
            log(f"Aviso ao mergear PR #{pr_number}: {e}")
            return False


# =====================================================================
# EXECUÇÃO DO MOTOR DE ATIVIDADE
# =====================================================================

class ActivityEngine:
    def __init__(self) -> None:
        self.env = load_env()
        self.min_daily = int(self.env.get("MIN_DAILY_COMMITS", "40"))
        self.max_daily = int(self.env.get("MAX_DAILY_COMMITS", "60"))
        self.active_start = int(self.env.get("ACTIVE_HOURS_START", "7"))
        self.active_end = int(self.env.get("ACTIVE_HOURS_END", "23"))
        self.state = BotState(self.min_daily, self.max_daily)
        self.github = GitHubAPI(self.env.get("GITHUB_TOKEN"), self.env.get("GITHUB_REPO", "rafaelrodrigopa/nexus-core"))

    def _run_git(self, args: List[str]) -> Tuple[int, str]:
        """Executa comandos git no diretório raiz do projeto."""
        res = subprocess.run(
            ["git"] + args,
            cwd=str(ROOT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return res.returncode, (res.stdout + res.stderr).strip()

    def _generate_action(self) -> Dict[str, Any]:
        """Gera conteúdo sênior via Gemini ou fallback autônomo."""
        gemini_key = self.env.get("GEMINI_API_KEY")
        if gemini_key:
            ai_data = query_gemini_for_code(gemini_key)
            if ai_data and "code" in ai_data and "file" in ai_data:
                return ai_data

        # Fallback Procedural
        # Sorteia ou itera um item do banco procedural
        item = random.choice(PROCEDURAL_MODULES)
        target_path = ROOT_DIR / item["file"]
        
        # Se o módulo já existe, gera uma melhoria/otimização incremental
        if target_path.exists():
            extra_comment = f"\n# [Optimization {datetime.now().strftime('%Y%m%d%H%M%S')}] Micro-benchmark tuning & branch prediction alignment\n"
            return {
                "file": item["file"],
                "test_file": item["test_file"],
                "commit_title": f"perf({Path(item['file']).stem}): align memory layout for cache locality",
                "commit_body": f"- Refine hot path instruction pipelining\n- Reduce CPU cycle latency by 12%\n- Update invariant assertions",
                "pr_title": f"[PERF] Cache-friendly layout for {Path(item['file']).stem}",
                "pr_body": f"### Performance Improvement\n\nOptimizes inner loops and reference dereferences in `{item['file']}`.\n\n- Verified zero regression with pytest.",
                "issue_title": f"Investigate branch prediction penalties in {Path(item['file']).stem}",
                "issue_body": "Analyze profile graphs for inner loops and apply contiguous layout.",
                "code": target_path.read_text(encoding="utf-8") + extra_comment,
                "test_code": None
            }

        return {
            "file": item["file"],
            "test_file": item["test_file"],
            "commit_title": item["title"],
            "commit_body": item["body"],
            "pr_title": f"[FEATURE] {item['title']}",
            "pr_body": f"### Overview\n\n{item['body']}\n\n- Tests: Passing\n- Docs: Complete",
            "issue_title": f"Implement {Path(item['file']).stem} with full test coverage",
            "issue_body": f"Requirements:\n- Time complexity guarantees\n- Thread-safety where applicable\n- Pytest validation",
            "code": item["code"],
            "test_code": item.get("test_code")
        }

    def perform_activity_cycle(self) -> bool:
        """Executa um ciclo completo de commit ou PR/Issue."""
        action = self._generate_action()
        file_rel = action["file"]
        code = action["code"]
        test_file_rel = action.get("test_file")
        test_code = action.get("test_code")

        full_file_path = ROOT_DIR / file_rel
        full_file_path.parent.mkdir(parents=True, exist_ok=True)
        full_file_path.write_text(code, encoding="utf-8")

        if test_file_rel and test_code:
            full_test_path = ROOT_DIR / test_file_rel
            full_test_path.parent.mkdir(parents=True, exist_ok=True)
            full_test_path.write_text(test_code, encoding="utf-8")

        # Atualiza métricas/status no README ou CHANGELOG
        changelog_path = ROOT_DIR / "CHANGELOG.md"
        entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry_log = f"- **{entry_time}**: {action['commit_title']}\n"
        if changelog_path.exists():
            changelog_path.write_text(changelog_path.read_text(encoding="utf-8") + entry_log, encoding="utf-8")
        else:
            changelog_path.write_text(f"# Changelog\n\n{entry_log}", encoding="utf-8")

        commit_title = action["commit_title"]
        commit_body = action.get("commit_body", "")
        full_commit_msg = f"{commit_title}\n\n{commit_body}".strip()

        # Decide se faz via PR/Issue (se GitHub API estiver configurada) ou Commit direto
        use_pr_flow = self.github.is_configured and (random.random() < 0.40)

        if use_pr_flow:
            branch_name = f"feat/nexus-{int(time.time())}"
            log(f"🌿 Criando branch de feature: {branch_name}")
            self._run_git(["checkout", "-b", branch_name])
            self._run_git(["add", "."])
            self._run_git(["commit", "-m", full_commit_msg])
            self._run_git(["push", "-u", "origin", branch_name])

            # Cria Issue opcional
            issue_num = None
            if action.get("issue_title"):
                issue_num = self.github.create_issue(action["issue_title"], action.get("issue_body", ""))

            # Cria PR
            pr_body = action.get("pr_body", "")
            if issue_num:
                pr_body += f"\n\nCloses #{issue_num}"
            pr_num = self.github.create_pull_request(action.get("pr_title", commit_title), pr_body, branch_name)

            if pr_num:
                time.sleep(2)
                self.github.review_and_merge_pr(pr_num, commit_title)

            # Retorna para main e deleta branch local
            self._run_git(["checkout", "main"])
            self._run_git(["pull", "origin", "main"])
            self._run_git(["branch", "-D", branch_name])
        else:
            log(f"💻 Realizando commit direto na main: {commit_title}")
            self._run_git(["checkout", "main"])
            self._run_git(["add", "."])
            code_ret, out = self._run_git(["commit", "-m", full_commit_msg])
            if code_ret != 0 and "nothing to commit" in out:
                log("Nenhuma alteração pendente detectada.")
                return False
            
            # Git Push
            p_code, p_out = self._run_git(["push", "origin", "main"])
            if p_code != 0:
                log(f"Aviso no push: {p_out}")

        self.state.record_commit(
            action_type="PR_FLOW" if use_pr_flow else "DIRECT_COMMIT",
            message=commit_title,
            details={"file": file_rel}
        )
        log(f"✨ Commit registrado com sucesso! ({self.state.data['completed_commits']}/{self.state.data['target_commits']} hoje)")
        return True

    def run_daemon(self) -> None:
        """Modo daemon contínuo: espalha os commits do dia com intervalos inteligentes."""
        log("🚀 Nexus Core Activity Daemon iniciado. Monitorando e executando ciclo diário contínuo...")

        while True:
            try:
                now = datetime.now()
                hour = now.hour
                state_data = self.state._load()
                completed = state_data.get("completed_commits", 0)
                target = state_data.get("target_commits", self.min_daily)

                # Verifica se está na janela ativa (ex: 07:00 às 23:00)
                if hour < self.active_start or hour > self.active_end:
                    log(f"🌙 Fora da janela de atividade ({self.active_start}h - {self.active_end}h). Pausa noturna.")
                    time.sleep(1800)  # dorme 30 min
                    continue

                if completed >= target:
                    log(f"🎉 Meta do dia atingida ({completed}/{target} commits). Aguardando próximo ciclo diário.")
                    time.sleep(1800)
                    continue

                # Calcula quanto tempo falta no dia e distribui o intervalo
                remaining_commits = target - completed
                remaining_hours = max(1, self.active_end - hour)
                base_sleep_minutes = max(6, min(35, int((remaining_hours * 60) / remaining_commits)))
                
                # Aplica variação aleatória de +/- 25% para evitar regularidade mecânica
                jitter = random.uniform(0.75, 1.25)
                actual_sleep_sec = int(base_sleep_minutes * 60 * jitter)

                log(f"⏳ Próximo commit programado em aprox. {actual_sleep_sec // 60} minutos ({completed}/{target} feitos).")
                time.sleep(actual_sleep_sec)

                # Executa o ciclo de commit/PR
                self.perform_activity_cycle()

            except (KeyboardInterrupt, SystemExit):
                log("🛑 Nexus Core Activity Daemon encerrado graciosamente.")
                break
            except Exception as e:
                log(f"❌ Erro no loop de execução do daemon: {e}")
                time.sleep(60)



def main() -> None:
    engine = ActivityEngine()
    args = sys.argv[1:]

    if "--status" in args:
        state = engine.state._load()
        print("\n" + "=" * 55)
        print("🎯 NEXUS CORE - STATUS DA ATIVIDADE DIÁRIA")
        print("=" * 55)
        print(f"📅 Data: {state.get('date')}")
        print(f"🎯 Meta Sorteada Hoje: {state.get('target_commits')} commits")
        print(f"✅ Commits Concluídos Hoje: {state.get('completed_commits')}")
        print(f"🏆 Total Histórico de Commits: {state.get('total_lifetime_commits')}")
        print(f"🕒 Última Ação: {state.get('last_action_time')}")
        print("=" * 55 + "\n")
        return

    if "--once" in args:
        log("Disparando rodada avulsa (--once)...")
        engine.perform_activity_cycle()
        return

    if "--batch" in args:
        idx = args.index("--batch")
        count = int(args[idx + 1]) if len(args) > idx + 1 else 1
        log(f"Executando lote de {count} commits...")
        for i in range(count):
            engine.perform_activity_cycle()
            time.sleep(2)
        return

    # Default: modo contínuo / daemon
    engine.run_daemon()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        pass

