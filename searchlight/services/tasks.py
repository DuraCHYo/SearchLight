class TasksService:
    def __init__(self, client, task_id=None):
        self.client = client
        self.task_id = task_id

    def get_task_info(self, task_id):
        return self.client.tasks.get(task_id=task_id)

    def get_tasks_list(self):
        return self.client.tasks.list()

    def cancel_task(self, task_id):
        return self.client.tasks.cancel(task_id=task_id)
