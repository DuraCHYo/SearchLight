class CatService:
    def __init__(self, client, name=None, verbose=False, index=None, field_name=None):
        self.client = client
        self.name = name
        self.verbose = verbose
        self.index = index
        self.field_name = field_name

    def cat_alias(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-aliases/
        return self.client.cat.aliases(
            params={"v": str(self.verbose).lower()}, name=self.name
        )

    def cat_allocation(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-allocation/
        return self.client.cat.allocation(
            params={"v": str(self.verbose).lower()}, node_id=self.name
        )

    def cat_count(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-count/
        return self.client.cat.count(
            params={"v": str(self.verbose).lower()}, index=self.index
        )

    def cat_fielddata(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-field-data/
        return self.client.cat.fielddata(
            params={"v": str(self.verbose).lower()}, fields=self.field_name
        )

    def cat_health(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-health/
        return self.client.cat.health(
            params={
                "v": "true",
                "h": "cluster,status,node.total,node.data,shards,pri,relo,init,unassign,pending_tasks,max_task_wait_time,active_shards_percent",
            }
        )
