# venv 確認方法

## 重要な注意事項

`list_files` コマンドは `.gitignore` に記載されたディレクトリを表示しません。

- venv ディレクトリは `.gitignore` に含まれているため、`list_files` では表示されない
- venv の存在確認には、PowerShell の `Get-ChildItem -Force` コマンドを使用すること
- `list_files` で venv が表示されないからといって、venv が存在しないと判断してはならない

## 確認手順

1. まず `Get-ChildItem -Force` で実際のディレクトリ構造を確認
2. venv が存在する場合は、既存の venv を使用
3. venv が存在しない場合のみ、学習者に確認してから新規作成