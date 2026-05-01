class CatService:
    def __init__(
        self,
        client,
        name=None,
        verbose=False,
        index=None,
        field_name=None,
        node_id=None,
        is_active=None,
    ):
        self.client = client
        self.name = name
        self.verbose = verbose
        self.index = index
        self.field_name = field_name
        self.node_id = node_id
        self.verbose_selector = str(self.verbose).lower()
        self.is_active = is_active

    def cat_alias(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-aliases/
        return self.client.cat.aliases(
            params={"v": self.verbose_selector}, name=self.name
        )

    def cat_allocation(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-allocation/
        return self.client.cat.allocation(
            params={"v": self.verbose_selector}, node_id=self.node_id
        )

    def cat_count(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-count/
        return self.client.cat.count(
            params={"v": self.verbose_selector}, index=self.index
        )

    def cat_fielddata(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-field-data/
        return self.client.cat.fielddata(
            params={"v": self.verbose_selector}, fields=self.field_name
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

    def cat_indices(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-indices/
        return self.client.cat.indices(
            params={"v": self.verbose_selector}, index=self.index
        )

    def cat_cluster_manager(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-cluster_manager/
        return self.client.cat.cluster_manager(
            params={"v": self.verbose_selector},
        )

    def cat_nodeattrs(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-nodeattrs/
        return self.client.cat.nodeattrs(
            params={"v": self.verbose_selector},
        )

    def cat_nodes(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-nodes/
        return self.client.cat.nodes(
            params={"v": self.verbose_selector},
        )

    def cat_pending_tasks(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-pending-tasks/
        return self.client.cat.pending_tasks(
            params={"v": self.verbose_selector},
        )

    def cat_pit_segments(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-pit-segments/
        return self.client.cat.all_pit_segments(
            params={"v": self.verbose_selector},
        )

    def cat_plugins(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-plugins/
        return self.client.cat.plugins(
            params={
                "v": self.verbose_selector,
                "h": "name,component,version,description",
            },
        )

    def cat_recovery(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-recovery/
        active_recovery_tasks = "false" if self.is_active else "true"
        return self.client.cat.recovery(
            index=self.index,
            params={
                "v": self.verbose_selector,
                "active_only": active_recovery_tasks,
                "detailed": self.verbose_selector,
            },
        )

    def cat_repositories(
        self,
    ):  # https://docs.opensearch.org/latest/api-reference/cat/cat-repositories/
        return self.client.cat.repositories(
            params={
                "v": self.verbose_selector,
            },
        )
