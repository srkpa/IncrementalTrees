from incremental_trees.trees import StreamingRFC
import dask_ml.datasets
import dask_ml.cluster
from dask_ml.wrappers import Incremental
import dask as dd
from dask.distributed import Client, LocalCluster


def run_on_blobs():

    x, y = dask_ml.datasets.make_blobs(n_samples=1e6,
                                       chunks=1e4,
                                       random_state=0,
                                       centers=3)

    x = dd.dataframe.from_array(x)
    y = dd.dataframe.from_array(y)

    print(f"Rows: {x.shape[0].compute()}")

    ests_per_chunk = 2
    chunks = len(x.divisions)

    srfc = Incremental(StreamingRFC(n_estimators=ests_per_chunk,
                                    max_n_estimators=chunks * ests_per_chunk))
    srfc.fit(x, y)


# Create, connect, and run on local cluster.
with LocalCluster(processes=False,
                  n_workers=2,
                  threads_per_worker=2,
                  scheduler_port=8080,
                  diagnostics_port=8081) as cluster, Client(cluster) as client:

        print(client)
        run_on_blobs()
