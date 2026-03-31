from opensearchpy import NotFoundError


class PoliciesService:
    def __init__(self, plugins):
        self.plugins = plugins

    def get_policy(self, policy_name=None):
        return self.plugins.index_management.get_policy(policy=policy_name)

    def add_policy(self, policy_name, body):
        return self.plugins.index_management.add_policy(policy=policy_name, body=body)

    def change_policy(self):
        return self.plugins.index_management.change_policy()

    def delete_policy(self):
        return self.plugins.index_management.delete_policy()

    def put_policy(self):
        return self.plugins.index_management.put_policy()

    def remove_policy_from_index(self):
        return self.plugins.index_management.remove_policy_from_index()

    def retry(self):
        return self.plugins.index_management.retry()

    def ensure_policy_exists(self, policy_name, body):
        try:
            existing = self.get_policy(policy_name=policy_name)
            return existing, False
        except NotFoundError:
            new_policy = self.add_policy(policy_name=policy_name, body=body)
            return new_policy, True
        except Exception as e:
            raise e
