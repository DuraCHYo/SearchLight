class NodeService:
    def __init__(self, client, node_id=None, metric=None):
        self.client = client
        self.node_id = node_id
        self.metric = metric

    def get_hot_threads(self):
        return self.client.nodes.hot_threads(node_id=self.node_id)

    def get_node_info(self):
        return self.client.nodes.info(node_id=self.node_id, metric=self.metric)

    def get_stats(self):
        return self.client.nodes.stats(node_id=self.node_id)
