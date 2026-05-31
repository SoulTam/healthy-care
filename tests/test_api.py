from __future__ import annotations

import pytest


class TestAuthAPI:
    @pytest.mark.asyncio
    async def test_health_endpoint(self, client):
        resp = await client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"

    @pytest.mark.asyncio
    async def test_send_code(self, client):
        resp = await client.post(
            "/api/v1/auth/send-code",
            json={"phone": "13800138000"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == "OK"

    @pytest.mark.asyncio
    async def test_register_login_flow(self, client):
        reg_resp = await client.post(
            "/api/v1/auth/register",
            json={
                "phone": "13900139000",
                "code": "123456",
                "password": "test123456",
                "nickname": "测试用户",
            },
        )
        assert reg_resp.status_code == 200

    @pytest.mark.asyncio
    async def test_protected_route_without_token(self, client):
        resp = await client.get("/api/v1/user/profile")
        assert resp.status_code == 403

    @pytest.mark.asyncio
    async def test_questions_endpoint(self, client):
        resp = await client.get("/api/v1/constitution/questions")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["data"]) == 10


class TestSearchAPI:
    @pytest.mark.asyncio
    async def test_search_recipes(self, client):
        resp = await client.get("/api/v1/search/recipes?q=阴虚")
        assert resp.status_code == 200


class TestFeedbackAPI:
    @pytest.mark.asyncio
    async def test_feedback_history_no_auth(self, client):
        resp = await client.get("/api/v1/feedback/history")
        assert resp.status_code == 403
