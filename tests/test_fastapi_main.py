from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType
import types


def load_fastapi_main_module() -> ModuleType:
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / "server" / "fastapi-main.py"
    if "openai_harmony" not in sys.modules:
        harmony_stub = types.ModuleType("openai_harmony")

        class _HarmonyStub:
            def __init__(self, *args, **kwargs) -> None:
                pass

        class _HarmonyEncodingName:
            HARMONY_GPT_OSS = "HARMONY_GPT_OSS"

        harmony_stub.Author = _HarmonyStub
        harmony_stub.Conversation = _HarmonyStub
        harmony_stub.DeveloperContent = _HarmonyStub
        harmony_stub.HarmonyEncodingName = _HarmonyEncodingName
        harmony_stub.Message = _HarmonyStub
        harmony_stub.RenderConversationConfig = _HarmonyStub
        harmony_stub.Role = _HarmonyStub
        harmony_stub.SystemContent = _HarmonyStub
        harmony_stub.TextContent = _HarmonyStub
        harmony_stub.load_harmony_encoding = lambda *_args, **_kwargs: object()
        sys.modules["openai_harmony"] = harmony_stub

    spec = importlib.util.spec_from_file_location("fastapi_main_for_tests", module_path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_scan_local_codex_summaries_skips_malformed_files(tmp_path: Path) -> None:
    module = load_fastapi_main_module()
    codex_root = tmp_path / ".codex"
    archived_dir = codex_root / "archived_sessions"
    sessions_dir = codex_root / "sessions"
    archived_dir.mkdir(parents=True)
    sessions_dir.mkdir(parents=True)

    good_archived = archived_dir / "good.jsonl"
    good_archived.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "type": "session_meta",
                        "payload": {
                            "id": "archived-good",
                            "timestamp": "2026-04-23T10:00:00Z",
                            "cwd": str(tmp_path / "gitrepos" / "demo"),
                        },
                    }
                ),
                json.dumps(
                    {
                        "type": "message",
                        "role": "user",
                        "timestamp": "2026-04-23T10:00:01Z",
                        "content": [{"text": "Inspect the repo."}],
                    }
                ),
            ]
        ),
        encoding="utf-8",
    )
    (archived_dir / "bad.jsonl").write_text(
        '\n'.join(['{"type":"session_meta","payload":{"id":"bad"}}', '{"broken":']),
        encoding="utf-8",
    )

    good_legacy = sessions_dir / "rollout-legacy-good.json"
    good_legacy.write_text(
        json.dumps(
            {
                "session": {
                    "id": "legacy-good",
                    "timestamp": "2026-04-23T09:00:00Z",
                },
                "items": [{"role": "user", "content": [{"text": "hello"}]}],
            }
        ),
        encoding="utf-8",
    )
    (sessions_dir / "rollout-legacy-bad.json").write_text("{", encoding="utf-8")

    summaries = module._scan_local_codex_summaries(str(codex_root))
    session_ids = {str(item["session_id"]) for item in summaries}

    assert session_ids == {"archived-good", "legacy-good"}


def test_get_openai_api_key_prefers_standard_name(monkeypatch) -> None:
    module = load_fastapi_main_module()
    module._get_openai_client.cache_clear()

    monkeypatch.setenv("OPEN_AI_API_KEY", "legacy-key")
    monkeypatch.setenv("OPENAI_API_KEY", "standard-key")

    assert module._get_openai_api_key() == "standard-key"


def test_get_openai_api_key_uses_legacy_fallback(monkeypatch) -> None:
    module = load_fastapi_main_module()
    module._get_openai_client.cache_clear()

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPEN_AI_API_KEY", "legacy-key")

    assert module._get_openai_api_key() == "legacy-key"
