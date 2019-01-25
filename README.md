# Ocean

A template creation tool for Machine Learning and Data Science projects.

[Здесь](README_ru.md) лежит русскоязычная версия этого README.

## История и главные особенности

### Cookiecutter-data-science

The project is based on [cookiecutter-data-science](https://drivendata.github.io/cookiecutter-data-science/) template, but is a modification of it. Before continue reading, I highly recommend you to follow the given link and take a look, because many key points listed there are important.

Let's see how the original cookiecutter is structured:

<details>
    <summary>Структура `cookiecutter-data-science`</summary>

```
├── LICENSE
├── Makefile           <- Makefile with commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default Sphinx project; see sphinx-doc.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.py           <- Make this project pip installable with `pip install -e`
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   │
│   ├── data           <- Scripts to download or generate data
│   │   └── make_dataset.py
│   │
│   ├── features       <- Scripts to turn raw data into features for modeling
│   │   └── build_features.py
│   │
│   ├── models         <- Scripts to train models and then use trained models to make
│   │   │                 predictions
│   │   ├── predict_model.py
│   │   └── train_model.py
│   │
│   └── visualization  <- Scripts to create exploratory and results oriented visualizations
│       └── visualize.py
│
└── tox.ini            <- tox file with settings for running tox; see tox.testrun.org

```
</details>

It can be upgraded at once:
1. we added `make docs` command for automatic generation of Sphinx documentation based on a whole `src` module's docstrings;
2. we added a conveinient file logger (and `logs` folder, respectivelly);
3. we added a coordinator entity for an easy navigation throughout the project, taking off the necessity of writing `os.path.join`, `os.path.abspath` или `os.path.dirname` every time.

But what problems are there?

* The folder `data` could grow significantly, but what script/notebook generated each file is a mystery. The amount of different files stored there can be misleading. Also it is not clear whether any of them is useful for a new feature implementation, because there is no place to contain descriptions and explanations.
* The folder `data` lacks the `features` submodule which could be a good use: the one can store calculated statistics, embeddings and other features. There is [a nice writing](https://www.logicalclocks.com/feature-store/) about this which I strongly recommend.
* The `src` folder is an another problem. It contains both functionality that is relevant project-wise (like `src.data` submodule) and functionality relevant to concrete and often small sub-tasks (like `src.models`).
* The folder `references` exists, but there is an opened question, who, when and how has to put some records there. And there is a lot to explain during the development process: which experiments have been done, what were the results, what are we doing next.

For a sake of solving listed problems I introduce the _experiment_ entity.


### Experiments

So, the _experiment_ is a place which contains all the data relevant to some hypothesis checking.

Including:
* What data was used
* What data (or artefacts) was produced
* Code version
* Timestamp of beginning and ending of an experiment
* Source file
* Parameters
* Metrics
* Logs

Many things can be logged via tracker utilities like [mlflow](https://mlflow.org/docs/latest/tracking.html), but it is not enough. We can improve our workflow.

This is what an example experiment looks like:

```
<project_root>
    └── experiments
        ├── exp-001-Tree-models
        │   ├── config          <- yaml-files with grid search parameters or just model parameters
        │   ├── models          <- dumped models
        │   ├── notebooks       <- notebooks for research
        │   ├── scripts         <- scripts like train.py or predict.py
        │   ├── Makefile        <- for handling experiment with just few words put in console
        │   └── log.md          <- logs of how the experiment is going
        │
        ├── exp-002-Gradient-boosting
       ...
```

Let's take a look at the workflow for one experiment.
1. The notebooks are created where data is being prepared for a model, and model's structure is being introduced.
2. Once the code is ready, it is moved to `train.py`
    - Use might track model parameters from there (for instance, with `mlflow`)
    - Create a relevant `config`-file for a training configuration
    - The code should has the possibility to be called from the console
    - It could take paths to the data, the `config`-file, and the directory to dump model to.
3. Then, Makefile is modified to start the training process via console. Provide a command like `make train`.
4. Many models are trained, all the metrics and parameters are sent to `mlflow`. The one can use `mlflow ui` to check the results.
5. Finally, all results are being recorded into `log.md`. It has some [impact analysis](https://en.wikipedia.org/wiki/Change_impact_analysis) elements: the developer needs to point out what data was used and what data was generated. This clarification can be used to generate automatically a readme file for a `data` folder and clarify where which file is used.