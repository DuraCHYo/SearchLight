from opensearchpy import NotFoundError


class PoliciesService:
    def __init__(self, plugins, policy_name=None, body=None, index=None):
        self.plugins = plugins
        self.policy_name = policy_name
        self.body = body
        self.index = index

    def get_policy(self):
        return self.plugins.index_management.get_policy(policy=self.policy_name)

    def put_policy(self):
        return self.plugins.index_management.put_policy(
            policy=self.policy_name, body=self.body
        )

    def add_policy_to_index(self):
        return self.plugins.index_management.add_policy(
            index=self.index, body=self.body
        )

    def ensure_policy_exists(self):
        try:
            existing = self.get_policy()
            return existing, False
        except NotFoundError:
            new_policy = self.put_policy()
            return new_policy, True
