from vacation_mode_controller import Controller
import os

def main(event, context):
    controller = Controller(os.environ['TOKEN_LINE'], os.environ['TOKEN_TODOIST'])
    controller.execute()
