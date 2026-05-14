from flask import Blueprint, jsonify, request
import db
from models.memo import create_memo, validate_memo

memos_bp = Blueprint("memos", __name__)


@memos_bp.route("/api/memos", methods=["GET"])
def get_memos():
    """メモの一覧を取得する。"""
    return jsonify(db.memos)


@memos_bp.route("/api/memos/stats", methods=["GET"])
def memo_stats():
    """メモの統計情報を取得する。"""
    stats = get_memo_stats(db.memos)
    return jsonify(stats)


@memos_bp.route("/api/memos/<int:memo_id>", methods=["GET"])
def get_memo(memo_id):
    """指定されたIDのメモを取得する。"""
    memo = next((m for m in db.memos if m["id"] == memo_id), None)
    if memo is None:
        return jsonify({"error": "メモが見つかりません"}), 404
    return jsonify(memo)


@memos_bp.route("/api/memos", methods=["POST"])
def create_memo_route():
    """新しいメモを作成する。"""
    data = request.get_json()
    is_valid, error_message = validate_memo(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400
    memo = create_memo(data["title"], data["content"])
    return jsonify(memo), 201


# TODO: DELETE /api/memos/<id> を実装する


def get_memo_stats(memo_list):
    """メモの統計情報を取得する。

    この関数はメモのリストを受け取り、様々な統計情報を計算して返す。
    タイトルの長さ、コンテンツの長さ、特定の文字の出現回数、
    カテゴリ別の分類などを行う。
    """
    if memo_list is None:
        return {"error": "メモリストがNoneです"}

    if len(memo_list) == 0:
        return {"total": 0, "average_title_length": 0, "average_content_length": 0}

    total = len(memo_list)
    total_title_length = 0
    total_content_length = 0
    longest_title = ""
    shortest_title = memo_list[0]["title"]
    has_long_memo = False
    has_short_memo = False
    warning_memos = []

    for memo in memo_list:
        title_len = len(memo["title"])
        content_len = len(memo["content"])
        total_title_length = total_title_length + title_len
        total_content_length = total_content_length + content_len

        if title_len > len(longest_title):
            longest_title = memo["title"]

        if title_len < len(shortest_title):
            shortest_title = memo["title"]

        if content_len > 100:
            has_long_memo = True
            if content_len > 200:
                if content_len > 500:
                    warning_memos.append(
                        {
                            "id": memo["id"],
                            "title": memo["title"],
                            "level": "critical",
                        }
                    )
                else:
                    warning_memos.append(
                        {
                            "id": memo["id"],
                            "title": memo["title"],
                            "level": "warning",
                        }
                    )
            else:
                warning_memos.append(
                    {"id": memo["id"], "title": memo["title"], "level": "info"}
                )
        else:
            has_short_memo = True

    avg_title = total_title_length / total
    avg_content = total_content_length / total

    result = {
        "total": total,
        "average_title_length": avg_title,
        "average_content_length": avg_content,
        "longest_title": longest_title,
        "shortest_title": shortest_title,
        "has_long_memo": has_long_memo,
        "has_short_memo": has_short_memo,
        "warning_memos": warning_memos,
    }
    return result
