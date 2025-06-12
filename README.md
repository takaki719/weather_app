# Weather App

天気情報を取得してLINEに通知するAWS Lambda関数です。OpenWeatherMap APIを使用して天気予報を取得し、指定した日の天気情報をフォーマットしてLINE Botを通じて配信します。

## 機能

- 今日・明日の天気予報を取得
- 天気情報を日本語でフォーマット（温度、降水確率、天気アイコン含む）
- LINE Botを通じてブロードキャスト配信
- AWS EventBridgeからのスケジュール実行に対応

## アーキテクチャ

```
EventBridge → Lambda → OpenWeatherMap API
                   ↓
              LINE Messaging API
```

## 必要な環境変数

- `LAT`: 緯度（デフォルト: 東京駅）
- `LON`: 経度（デフォルト: 東京駅）

## 必要なAWS SSM Parameters

- `OWM_API_KEY`: OpenWeatherMap API キー（暗号化推奨）
- `LINE_ACCESS_TOKEN`: LINE Bot アクセストークン（暗号化推奨）

## セットアップ

1. 依存関係のインストール:
```bash
pip install -r requirements.txt
```

2. AWS SSMにAPIキーを設定:
```bash
aws ssm put-parameter --name "OWM_API_KEY" --value "your-openweathermap-api-key" --type "SecureString"
aws ssm put-parameter --name "LINE_ACCESS_TOKEN" --value "your-line-bot-token" --type "SecureString"
```

3. Lambda関数にデプロイ（パッケージ作成）:
```bash
zip -r weather.zip . -x "*.git*" "__pycache__/*" "*.pyc"
```

## 使用方法

EventBridgeから以下のイベントでLambda関数を呼び出します：

```json
{
  "target_day": "today"
}
```

または

```json
{
  "target_day": "tomorrow"
}
```

## プロジェクト構成

```
weather_app/
├── handler.py              # Lambda エントリーポイント
├── domain/
│   ├── weather_client.py   # OpenWeatherMap API クライアント
│   └── formatter.py        # メッセージフォーマッター
├── adapters/
│   └── line.py            # LINE Messaging API アダプター
├── requirements.txt        # Python依存関係
└── scheduler.tf           # Terraform設定ファイル
```

## Terraform設定

`scheduler.tf`にはAWS EventBridgeスケジューラーの設定が含まれており、定期的な天気通知の自動実行が可能です。

## 動作例
![IMG_7641](https://github.com/user-attachments/assets/354aee3d-34d2-422c-b2de-5d27ee8a4294)

