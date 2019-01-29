# Ocean

Утилита для создания шаблонов проектов по машинному обучению и анализу данных.

## Содержание

* [tldr](#tldr)
    * [Установка](#Установка)
    * [Использование](#Использование)
* [История и главные особенности](#История-и-главные-особенности)
    * [Cookiecutter-data-science](#Cookiecutter-data-science)
    * [Эксперименты](#Эксперименты)

## tldr

### Установка

1) Установите Sphinx для генерации документации.

[Ссылка](http://www.sphinx-doc.org/en/1.4/install.html) на страничку с инструкцией установки.

2) Выполните эти команды в терминале:

```
sudo -i
git clone https://github.com/EnlightenedCSF/Ocean.git
cd <cloned repo>
pip install --upgrade .
```

### Использование

Создание нового проекта:
```
ocean new -n "<project_name>" \    # must be provided
          -a "<author>" \          # default is `Surf`
          -v "<version>" \         # default is `0.0.1`
          -d "<description>" \     # default is ``
          -l "<licence>" \         # default is `MIT`
          -p "<path>"              # default is `.`
```

Создание нового эксперимента в проекте:
```
make -B experiment name="<exp_name>"
```

## История и главные особенности

### Cookiecutter-data-science

За основу построения Ocean был взял шаблон [cookiecutter-data-science](https://drivendata.github.io/cookiecutter-data-science/) и модифицирован. Прежде чем продолжить чтение, я настоятельно рекомендую взглянуть на него в рамках приведенной статьи, так как многие аспекты философии и подхода к организации проекта взяты оттуда.

---

<details>
    <summary>Давайте взглянем на структуру оригинального шаблона:</summary>

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

---

Взяв такой подход за основу в проекте, мы немного улучшили его сразу:
1. добавили команду `make docs` для автоматической генерации документации по всем docstrings модуля `src`;
2. добавили логгер для удобного файлового логирования (и, соответственно, добавили папку `logs` в корне проекта);
3. добавили сущность координатора для удобной навигации по проекту из скриптов и тетрадей без боязни опечататься в пути или без необходимости утомительно писать каждый раз `os.path.join`, `os.path.abspath` или `os.path.dirname`.

С какими проблемами столкнулись, применив cookiecutter-data-science?

* Папка `data` может разростаться, но какой скрипт/тетрадь порождает очередной файл - не совсем ясно. В большом количестве легко запутаться. Не ясно, нужно ли в рамках реализации новой фичи использовать какие-то файлы из существующих, так как нигде не хранится описание/документация по их предназначению.
* В `data` не хватает подпапки `features`, в которую можно было бы складировать признаки: посчитанные статистики, эмбеддинги и другие характеристики, из которых можно было бы собрать разные конечные представления данных. Об этом было уже замечательно написано в [этом блог-посте](https://www.logicalclocks.com/feature-store/).
* `src` - другая папка-проблема. В ней смешаны в одной большой куче как функциональность, актуальная в рамках проекта в целом (например, подготовка и чистка данных из подмодуля `src.data`), так и очень частные вещи вроде `src.models`: каждая модель может решать, возможно, узкую подзадачу, и в итоге получаем такую же свалку файлов.
* `references` представлен, но все ещё стоит открытый вопрос, кто, когда и в каком виде должен заносить туда материалы. А рассказать можно много по ходу проекта: какие эксперименты проведены, каков их результат, каковы дальнейшие планы.

Для решения вышеперечисленых проблем и была выделена следующая сущность: _эксперимент_.


### Эксперименты

Назовем _экспериментом_ сущность, которая является хранилищем всех данных, участвовавших в проверке некоторой гипотезы.

К их числу относятся:
* Какие данные были использованы.
* Какие данные (артефакты) были порождены в результате.
* Версия кода.
* Время начала и завершения эксперимента.
* Исполняемый файл.
* Параметры.
* Метрики.
* Логи.

Многие перечисленные пункты могут быть реализованы с помощью утилит-трекеров, например, [mlflow](https://mlflow.org/docs/latest/tracking.html), но этого не достаточно. Хотелось бы улучшить workflow, решив проблемы с организацией проекта, выделенные выше.

Модуль одного эксперимента выглядит следующим образом:

```
<project_root>
    └── experiments
        ├── exp-001-Tree-models
        │   ├── config            <- yaml-файлы с настройками grid search или просто конфигурацией модели
        │   ├── models            <- сохраненные модели
        │   ├── notebooks         <- ноутбуки для экспериментов
        │   ├── scripts           <- скрипты, например, train.py или predict.py
        │   ├── Makefile          <- для управления экспериментом из консоли
        │   ├── requirements.txt  <- список зависимых библиотек
        │   └── log.md            <- лог проведения эксперимента
        │
        ├── exp-002-Gradient-boosting
       ...
```

Рассмотрим подробнее workflow при проведении одного эксперимента.
1. Создаются ноутбуки, в них подготавливаются данные, создается структура модели.
2. Как только код подготовки модели завершен, он переносится в `train.py`.
    - В коде должен присутствовать трекинг параметров, например, с помощью `mlflow`.
    - В `config` создается файл с конфигурацией `train.py`.
    - Обязательно должен управляться из консоли и принимать пути к необходимым данным, `config`-файлу и локации последующего сохранения готовой модели.
3. Корректируется `Makefile` для последующего многократного запуска обучения. Итоговая команда должна быть без параметров вроде `make train`.
4. Прогоняется множество моделей, все метрики и параметры попадают в `mlflow`. А через `mlflow ui` можно посмотреть на результаты.
5. В завершении результаты пишутся в `log.md`. В нем предусмотрены элементы [impact-анализа](https://en.wikipedia.org/wiki/Change_impact_analysis): необходимо пояснить, какие данные были использованы и какие были созданы в процессе. В последствии это поможет объединить все такие логи и сформировать единый readme в папке `data`, и пояснить, где-что используется, автоматически.
