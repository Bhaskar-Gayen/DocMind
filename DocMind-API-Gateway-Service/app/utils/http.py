import httpx
from typing import Optional, Dict, Any


async def forward_request(
    url: str,
    method: str = "GET",
    params: Optional[Dict] = None,
    json: Optional[Dict] = None,
    headers: Optional[Dict] = None
) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=url,
            params=params,
            json=json,
            headers=headers
        )
        return response.json()
