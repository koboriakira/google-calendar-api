https://j5xbcoq5o2.execute-api.ap-northeast-1.amazonaws.com/hello

## デプロイ

### レイヤーの更新

`cdk deploy`の前に下記コマンドを実行して、必要なライブラリをローカルに用意しておく

```
pip install -r requirements.txt -t ../layer/python
```

## ローカル開発

```shell
make run
```
