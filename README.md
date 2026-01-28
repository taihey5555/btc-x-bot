# BTC Analysis X Bot

BTCシグナルダッシュボードのデータを分析し、Xに自動投稿するBot。

## セットアップ

### 1. GitHubリポジトリ作成

```bash
cd btc-x-bot
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/btc-x-bot.git
git push -u origin main
```

### 2. X API認証情報の取得

1. https://developer.twitter.com/ でDeveloper Portalにアクセス
2. プロジェクト作成 → App作成
3. 「User authentication settings」で OAuth 1.0a を有効化
   - App permissions: **Read and write**
4. Keys and tokens から以下を取得:
   - API Key
   - API Key Secret
   - Access Token
   - Access Token Secret

### 3. GitHub Secrets設定

リポジトリの Settings → Secrets and variables → Actions で以下を追加:

| Secret名 | 値 |
|---|---|
| `DASHBOARD_URL` | `https://bitcoin-bunseki.onrender.com` |
| `X_API_KEY` | X API Key |
| `X_API_SECRET` | X API Key Secret |
| `X_ACCESS_TOKEN` | Access Token |
| `X_ACCESS_SECRET` | Access Token Secret |

### 4. 実行

- **自動**: 毎日 9:00 / 21:00 (JST) に自動投稿
- **手動**: Actions → Post BTC Analysis to X → Run workflow

## 投稿内容

```
📊 BTC市場分析レポート
2026/01/28 09:00

💰 BTC: $102,345
🟢 総合スコア: +25 (やや強気)

【シグナル】
🟢 USD流動性: $5.71T
🔴 DXY: 96.0
🟢 Fear & Greed: 29
...

#Bitcoin #BTC #仮想通貨 #投資
```

+ ダッシュボードのスクリーンショット画像
