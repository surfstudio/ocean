from multiprocessing import Pool, cpu_count
import numpy as np


def parallelize(data, func, n_threads: int = None) -> np.array:
    """
        **Applies function to an array in multithreads**

        :param data: np.array or pd.Series of data.
        :param func: function to apply on batches. Input param of the func is array's part.
        :param n_threads: number of parallel threads.
    """
    if n_threads is None:
        partitions = cores = cpu_count()
    else:
        partitions = cores = n_threads
    data_split = np.array_split(data, partitions)
    pool = Pool(cores)
    data = np.concatenate(list(pool.imap(func, data_split)))
    pool.close()
    pool.join()
    return data
