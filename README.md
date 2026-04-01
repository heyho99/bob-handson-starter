# bob-handson-starter

IBM Bob ハンズオン用のメモAPIプロジェクトです。

## 概要

Python（Flask）製の簡易メモAPIサーバーです。
CRUD機能が部分的に実装されています。

## セットアップ

```bash
pip install -r requirements.txt
```

## 起動

```bash
python app.py
```

サーバーが `http://localhost:5000` で起動します。

## API

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/api/memos` | メモ一覧取得 |
| GET | `/api/memos/<id>` | メモ詳細取得 |
| POST | `/api/memos` | メモ新規作成 |

## テスト

```bash
python -m pytest
```
