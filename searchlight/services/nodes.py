class NodeService:
    def __init__(self, client, node_id=None, metric=None, doc_type=None):
        self.client = client
        self.node_id = node_id
        self.metric = metric
        self.doc_type = doc_type

    def get_hot_threads(self):
        return self.client.nodes.hot_threads(
            node_id=self.node_id, doc_type=self.doc_type
        )

    def get_node_info(self):
        return self.client.nodes.info(node_id=self.node_id, metric=self.metric)

    def get_node_stats(self):
        return self.client.nodes.stats(node_id=self.node_id, metric=self.metric)

    def get_node_usage(self):
        return self.client.nodes.stats(node_id=self.node_id, metric=self.metric)
