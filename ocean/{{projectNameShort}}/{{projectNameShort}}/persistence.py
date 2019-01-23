"""
.. module:: src.persistence
   :synopsis: The module contains a few shortcuts for working with Pickle.
"""
import pickle


def save(obj, path):
    """
        **Saves object to pickle**

        :param obj: Object to serialize
        :param path: String path to the file
    """
    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load(path):
    """
        **Loads object from pickle**

        :param path: String path to the file

        :rtype: Object that was loaded
    """
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj
