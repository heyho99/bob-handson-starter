"""メモAPIのテスト"""
import sys
import os
import pytest

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app


@pytest.fixture(autouse=True)
def reset_db():
    """テストごとにデータベースを初期状態にリセットする。"""
    import db

    db.memos = [
        {"id": 1, "title": "買い物リスト", "content": "牛乳、卵、パン"},
        {"id": 2, "title": "会議メモ", "content": "次回の会議は金曜日14時から"},
        {"id": 3, "title": "アイデア", "content": "新しいプロジェクトの提案書を作成する"},
    ]
    db.next_id = 4


@pytest.fixture
def client():
    """テスト用クライアントを作成する。"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestGetMemos:
    """GET /api/memos のテスト"""

    def test_get_all_memos(self, client):
        response = client.get("/api/memos")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_memo_has_title_and_content(self, client):
        response = client.get("/api/memos")
        data = response.get_json()
        memo = data[0]
        assert "title" in memo
        assert "content" in memo


class TestGetMemo:
    """GET /api/memos/<id> のテスト"""

    def test_get_existing_memo(self, client):
        response = client.get("/api/memos/1")
        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == 1

    def test_get_nonexistent_memo_returns_404(self, client):
        response = client.get("/api/memos/9999")
        assert response.status_code == 404


class TestCreateMemo:
    """POST /api/memos のテスト"""

    def test_create_new_memo(self, client):
        response = client.post(
            "/api/memos",
            json={"title": "テストメモ", "content": "テスト内容"},
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["title"] == "テストメモ"

    def test_create_memo_without_title_returns_400(self, client):
        response = client.post(
            "/api/memos",
            json={"content": "内容のみ"},
        )
        assert response.status_code == 400

    def test_create_memo_with_category(self, client):
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

    def test_delete_memo(self, client):
        response = client.delete("/api/memos/1")
        assert response.status_code == 200

    def test_delete_nonexistent_memo_returns_404(self, client):
        response = client.delete("/api/memos/9999")
        assert response.status_code == 404
