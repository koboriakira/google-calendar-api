# My Google Calendar API

## 使用例

access-token(GASのDEPLOY_ID)をヘッダーにつけて、下記のAPIを呼び出す。

https://alh2lfk4dc35fg5dbgdanp2y2y0xdrze.lambda-url.ap-northeast-1.on.aws/list?start_date=2024-01-10&end_date=2024-01-10&achievement=false

## デプロイ

GitHub Actionsのdeployワークフローを利用。

## ローカル開発

Dev Containerも準備済。

```shell
make run
```
