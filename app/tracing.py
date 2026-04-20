from __future__ import annotations

import os
from typing import Any


try:
    from langfuse import observe, get_client as _get_client

    class _LangfuseContext:
        """Shim mapping v2 langfuse_context API to langfuse v3 get_client()."""

        def update_current_trace(self, **kwargs: Any) -> None:
            _get_client().update_current_trace(**kwargs)

        def update_current_observation(self, **kwargs: Any) -> None:
            # v3: update_current_generation accepts usage_details
            _get_client().update_current_generation(**kwargs)

    langfuse_context = _LangfuseContext()

except Exception:
    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def update_current_observation(self, **kwargs: Any) -> None:
            return None

    langfuse_context = _DummyContext()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
