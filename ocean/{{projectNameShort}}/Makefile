.DEFAULT: help

help:
	@echo "\n     USAGE"
	@echo "===============\n"
	@echo "make -B all"
	@echo "       Build documentation and then install package to pip\n"
	@echo "make -B docs"
	@echo "       Build documentation for the project\n"
	@echo "make -B project"
	@echo "       Install src/-codebase to the pip\n"
	@echo "make -B experiment NAME=<EXP_NAME>\n"
	@echo "       Creates new experiment in the folder `experiments`\n"
	@echo "make -B log PASSWORD=<PASSWORD>\n"
	@echo "       Creates project log, adds it to zip archive and sets a password <PASSWORD> on it\n"

all: docs package log

docs:
	@cd utils/ && \
	python3 docs_index_generator.py --template docsIndexTemplate.jinja --save ../docs/index.rst && \
	cd ../docs/ && \
	$(MAKE) html

package:
	@pip install --upgrade .

experiment:
	@cd utils/ && \
	python3 experiment_creator.py -n $(NAME)

log:
  @python3 utils/log_generator.py && zip -P $(PASSWORD) -r project_log.zip project_log >>/dev/null
