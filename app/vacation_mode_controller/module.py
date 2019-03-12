import json
import datetime
import requests
from line_notify import LineNotify
from todoist.api import TodoistAPI

class Controller:
    def __init__(self, token_line, token_todoist, vacation_mode_pj = None):
        self._holidays = requests.get("https://holidays-jp.github.io/api/v1/date.json").json()
        self._line_notify = LineNotify(token_line, name="todoist")
        self._todoist_api = TodoistAPI(token_todoist, cache="/tmp/")
        self._todoist_vacation_mode_pj = vacation_mode_pj

    def _is_vacation_mode_on(self):
        return self._todoist_api.completed.get_stats()['goals']['vacation_mode'] == 1

    def _is_today_holiday(self):
        today = datetime.date.today().strftime("%Y-%m-%d")
        return today in self._holidays.keys()

    def _get_custom_date_tasks(self):
        today = datetime.date.today().strftime("%a %d %b")
        tasks = []
        if self._todoist_vacation_mode_pj is None:
            return tasks

        for item in self._todoist_api.projects.get_data(self._todoist_vacation_mode_pj)['items']:
            due = item['due_date_utc']
            # Slicing :10 gives us the relevant parts
            if due and due[:10] == today:
                tasks.append(item)
        return tasks

    def _has_any_custom_date_tasks(self):
        return len(self._get_custom_date_tasks()) > 0

    def _should_change_vacation_mode_on(self):
        return not self._is_vacation_mode_on() and (self._is_today_holiday() or self._has_any_custom_date_tasks())

    def _should_change_vacation_mode_off(self):
        return self._is_vacation_mode_on() and not self._is_today_holiday() and not self._has_any_custom_date_tasks()

    def _complete_custom_date_tasks(self):
        if not self._has_any_custom_date_tasks():
            return
        for item in self._get_custom_date_tasks():
            self._todoist_api.items.get_by_id(item['id']).complete()
        self._todoist_api.commit()

    def execute(self):
        if self._should_change_vacation_mode_on():
            vacation = 1
            notify_message = "バケーションモードをONにしました。"
        elif self._should_change_vacation_mode_off():
            vacation = 0
            notify_message = "バケーションモードをOFFにしました。"
        else:
            return

        before_vacation_mode = self._is_vacation_mode_on()

        self._todoist_api.user.update_goals(vacation_mode=vacation)
        self._todoist_api.commit()

        if self._is_vacation_mode_on() == before_vacation_mode:
            notify_message = "バケーションモードの変更に失敗しました。"

        self._line_notify.send(notify_message)
