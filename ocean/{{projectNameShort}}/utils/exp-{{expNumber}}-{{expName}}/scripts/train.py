# import your model from somewhere
from sklearn.dummy import DummyClassifier

# import some metrics
from sklearn.metrics import accuracy_score


from tqdm import tqdm

import janus
import mlflow
import pickle
import yaml


def train(config_path: str, data_path: str, save_path: str):
    with open(config_path) as f:
        config = yaml.load(f)

    with open(data_path, 'rb') as f:
        data = pickle.load(f)
        X = data['X']
        y = data['y']

    with mlflow.start_experiment(experiment_id={{expId}}):

        clf = DummyClassifier()
        mlflow.log_param('param_name', 4)

        clf.fit(X, y)
        y_hat = clf.predict(X)

        mlflow.log_metric('accuracy', accuracy_score(y, y_hat))


if __name__ == '__main__':
    p = janus.ArgParser()
    p.new_str('c config')
    p.new_str('d data')
    p.new_str('s save')
    p.parse()
    train(config_path=p['c'],
          data_path=p['d'],
          save_path=p['s'])

