from opensearchpy import NotFoundError


class PoliciesService:
    def __init__(self, plugins):
        self.plugins = plugins

    def get_policy(self, policy_name=None):
        return self.plugins.index_management.get_policy(policy=policy_name)

    def put_policy(self, policy_name, body):
        return self.plugins.index_management.put_policy(policy=policy_name, body=body)

    def add_policy_to_index(self, index_name, body):
        return self.plugins.index_management.add_policy(index=index_name, body=body)

    def ensure_policy_exists(self, policy_name, body):
        try:
            existing = self.get_policy(policy_name=policy_name)
            return existing, False
        except NotFoundError:
            new_policy = self.put_policy(policy_name=policy_name, body=body)
            return new_policy, True
