"""メモAPIのテスト"""
import sys
import os
import pytest

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app


@pytest.fixture
def client():
    """テスト用クライアントを作成する。"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestGetMemos:
    """GET /api/memos のテスト"""

    def test_メモ一覧を取得できる(self, client):
        response = client.get("/api/memos")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_メモにtitleとcontentが含まれる(self, client):
        response = client.get("/api/memos")
        data = response.get_json()
        memo = data[0]
        assert "title" in memo
        assert "content" in memo


class TestGetMemo:
    """GET /api/memos/<id> のテスト"""

    def test_存在するメモを取得できる(self, client):
        response = client.get("/api/memos/1")
        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == 1

    def test_存在しないメモで404が返る(self, client):
        response = client.get("/api/memos/9999")
        assert response.status_code == 404


class TestCreateMemo:
    """POST /api/memos のテスト"""

    def test_新しいメモを作成できる(self, client):
        response = client.post(
            "/api/memos",
            json={"title": "テストメモ", "content": "テスト内容"},
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["title"] == "テストメモ"

    def test_titleなしで400が返る(self, client):
        response = client.post(
            "/api/memos",
            json={"content": "内容のみ"},
        )
        assert response.status_code == 400

    def test_メモにcategoryが含まれる(self, client):
        """カテゴリ付きでメモを作成できることを確認する。"""
        response = client.post(
            "/api/memos",
            json={
                "title": "カテゴリテスト",
                "content": "カテゴリ付きメモ",
                "category": "仕事",
            },
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["category"] == "仕事"


class TestDeleteMemo:
    """DELETE /api/memos/<id> のテスト"""

    def test_メモを削除できる(self, client):
        response = client.delete("/api/memos/1")
        assert response.status_code == 200

    def test_存在しないメモの削除で404が返る(self, client):
        response = client.delete("/api/memos/9999")
        assert response.status_code == 404
