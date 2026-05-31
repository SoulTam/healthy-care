from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_answers() -> dict[int, int]:
    return {
        1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
        6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
    }


@pytest.fixture
def sample_recipe() -> dict:
    return {
        "id": 1,
        "name": "百合莲子银耳羹",
        "category": "甜品",
        "constitutions": ["阴虚质", "气虚质"],
        "seasons": ["秋季", "冬季"],
        "ingredients": ["百合", "莲子", "银耳", "冰糖"],
        "effects": ["滋阴润肺", "清心安神"],
        "natures": {"百合": "甘微寒"},
        "symptoms": ["干咳", "失眠", "口干"],
        "contraindications": ["风寒咳嗽"],
        "steps": "1.银耳泡发 2.加冰糖 3.炖煮",
        "nutrition": {"calories": 120},
        "source": "《随息居饮食谱》",
    }
