import asyncio
from typing import List

import orjson
from fastapi import APIRouter
from fastapi import Depends
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect

from synctabs.application.check_user import AuthenticatedUser
from synctabs.application.ports.tabs_dao import TabsDAO
from synctabs.domain.tabs.tab import Tab
from synctabs.presentation import config
from synctabs.presentation.web.dependencies import On
from synctabs.presentation.web.dependencies import get_current_user
from synctabs.presentation.web.dependencies import templates

router = APIRouter()
WS_CLIENTS: List[WebSocket] = []


@router.get("/")
async def view_tabs(
    request: Request,
    user: AuthenticatedUser = Depends(get_current_user),
    tabs_dao: TabsDAO = Depends(On(TabsDAO)),
) -> Response:
    view = tabs_dao.get_view()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "view_json": orjson.dumps(view.dict()).decode("utf-8"),
            "config": config,
            "websocket_scheme": "wss" if request.url.scheme == "https" else "ws",
        },
    )


@router.post("/sync")
async def sync_tabs(
    tabs: List[Tab],
    user: AuthenticatedUser = Depends(get_current_user),
    tabs_dao: TabsDAO = Depends(On(TabsDAO)),
) -> None:
    tabs_dao.write(tabs)

    if WS_CLIENTS:
        payload = {"id": "new_view", "view": tabs_dao.get_view().dict()}
        await asyncio.wait(
            [ws.send_text(orjson.dumps(payload).decode("utf-8")) for ws in WS_CLIENTS]
        )


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    WS_CLIENTS.append(websocket)

    await websocket.accept()
    try:
        while True:
            try:
                _ = await websocket.receive_text()
            except WebSocketDisconnect:
                break
    finally:
        WS_CLIENTS.remove(websocket)
