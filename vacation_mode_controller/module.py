import json
import datetime
import requests
from line_notify import LineNotify
from todoist.api import TodoistAPI

class Controller:
    def __init__(self, token_line, token_todoist):
        self.holidays = requests.get("https://holidays-jp.github.io/api/v1/date.json").json()
        self.line_notify = LineNotify(token_line, name="todoist")
        self.todoist_api = TodoistAPI(token_todoist, cache="/tmp/")

    def _is_vacation_mode_on(self):
        return self.todoist_api.completed.get_stats()['goals']['vacation_mode'] == 1

    def _is_today_holiday(self):
        today = datetime.date.today().strftime("%Y-%m-%d")
        return today in self.holidays.keys()

    def execute(self):
        if not self._is_vacation_mode_on() and self._is_today_holiday():
            vacation = 1
            notify_message = "バケーションモードをONにしました。"
        elif self._is_vacation_mode_on() and not self._is_today_holiday():
            vacation = 0
            notify_message = "バケーションモードをOFFにしました。"
        else:
            return

        before_vacation_mode = self._is_vacation_mode_on()

        self.todoist_api.user.update_goals(vacation_mode=vacation)
        self.todoist_api.commit()

        if self._is_vacation_mode_on() == before_vacation_mode:
            notify_message = "バケーションモードの変更に失敗しました。"

        self.line_notify.send(notify_message)