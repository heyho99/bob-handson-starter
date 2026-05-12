# サーバー起動中のAPIテスト方法

## 短時間起動による動作確認（PowerShell）

APIの疎通確認など、サーバを一時的に起動して即停止したい場合は `Start-Process` を使う。

```powershell
$proc = Start-Process -FilePath ".\venv\Scripts\python.exe" -ArgumentList "app.py" -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 3          # Flask 起動完了を待つ
Invoke-WebRequest -Uri "http://localhost:<ポート>/<確認したいパス>" -UseBasicParsing
$proc.Kill()                    # 確認後に停止
```

- `-PassThru` でプロセスオブジェクトを受け取り、最後に `Kill()` で確実に終了させる。
- `activate` は使わず、`venv\Scripts\python.exe` をフルパス指定する。

