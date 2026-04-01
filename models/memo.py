"""メモのデータモデル定義"""


def create_memo(title: str, content: str) -> dict:
    """新しいメモを作成する。

    Args:
        title: メモのタイトル
        content: メモの内容

    Returns:
        作成されたメモの辞書
    """
    from db import memos, next_id
    import db

    memo = {
        "id": next_id,
        "title": title,
        "content": content,
    }
    memos.append(memo)
    db.next_id += 1
    return memo


def validate_memo(data: dict) -> tuple[bool, str]:
    """メモのバリデーションを行う。

    Args:
        data: バリデーション対象のデータ

    Returns:
        (有効かどうか, エラーメッセージ)
    """
    if not data:
        return False, "リクエストボディが空です"
    if "title" not in data:
        return False, "titleは必須です"
    if "content" not in data:
        return False, "contentは必須です"
    if not isinstance(data["title"], str):
        return False, "titleは文字列である必要があります"
    if not isinstance(data["content"], str):
        return False, "contentは文字列である必要があります"
    if len(data["title"]) == 0:
        return False, "titleは空にできません"
    if len(data["content"]) == 0:
        return False, "contentは空にできません"
    return True, ""
