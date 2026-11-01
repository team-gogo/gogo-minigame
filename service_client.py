import os

import httpx
from fastapi import HTTPException


async def get_service_text(service: str, path: str) -> str:
    urls = {
        "gogo-user": os.environ.get(
            "USER_SERVICE_URL", "http://gogo-user.gogo.svc.cluster.local"
        ),
        "gogo-stage": os.environ.get(
            "STAGE_SERVICE_URL", "http://gogo-stage.gogo.svc.cluster.local"
        ),
    }
    if service not in urls:
        raise ValueError(f"Unknown service: {service}")
    if not path.startswith("/") or path.startswith("//"):
        raise ValueError("Service path must be an absolute path, not a URL")
    base = httpx.URL(urls[service])
    if base.scheme not in ("http", "https") or not base.host:
        raise ValueError(f"Invalid URL configured for {service}")
    try:
        async with httpx.AsyncClient(timeout=5.0, follow_redirects=False) as client:
            response = await client.get(str(base).rstrip("/") + path)
            response.raise_for_status()
            return response.text
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail=f"{service} timed out") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"{service} request failed") from exc
