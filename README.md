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

1. AWSにて、severless deploy用のIAMを作成し、keyとaccess tokenを取得 
2. Todoistの自分のAPIトークンを取得(マイページにある)
3. [LineNotify](https://notify-bot.line.me/my/)のトークンを取得
4. `.env`に上記の各種key,tokenを記載
5. `cp ./.env.local ./.env`
6. `docker-compose build`
7. `docker-compose up -d`
8. `docker-compose exec serverless bash`
9. `sls deploy`

## TODO

- 祝日だけでなく、自身のスケジュールを取得できるようにしたい
    - GoogleCalendarでなく、timetreeから取得したい…

## Licence

[MIT](https://github.com/aiji42/serverless-auto-control-todoist/blob/master/LICENSE)

## Author

[AijiUejima](https://github.com/aiji42)
