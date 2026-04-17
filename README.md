# bob-hands-on

Python（Flask）製の簡易メモ管理Webアプリです。

## セットアップ

```bash
pip install -r requirements.txt
```

## 起動

```bash
python app.py
```

ブラウザで `http://localhost:5000` を開くとメモ管理画面が表示されます。

## API

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/api/memos` | メモ一覧取得 |
| GET | `/api/memos/<id>` | メモ詳細取得 |
| GET | `/api/memos/stats` | メモ統計情報取得 |
| POST | `/api/memos` | メモ新規作成 |

## テスト

```bash
python -m pytest
```
