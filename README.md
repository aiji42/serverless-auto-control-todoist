Serverless Todoist Vacation Mode Controller
====

## Description

祝日情報を取得し、TodoistのバケーションモードのON/OFFを自動切り替えを行う、ServerlessApplication(Python3.6)

ON/OFFが行われるとLINEに通知を送る

## Requirement

- https://github.com/Doist/todoist-python
- https://github.com/golbin/line-notify

## Usage

- 一度デプロイすれば、スケジュールに従って定期実行してくれます
    - 初期値は毎日午前9時(UTC00:00)
    - 祝日情報は都度googleに問い合わせるので、アップデートは不要

## Install

1. `pip install`
2. https://serverless.com/ に従ってAWSにデプロイできる準備をしておく
    - credentialsとか
3. Todoistの自分のAPIトークンを取得(マイページにある)
4. [LineNotify](https://notify-bot.line.me/my/)のトークンを取得
5. `cp ./config.json.local ./config.json`
6. `config.json`にLINEのトークンとTodoistのトークンを記載
7. `serverless deploy`

## Licence

[MIT](https://github.com/aiji42/)

## Author

[aiji42](https://github.com/aiji42)
