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


all: docs package


docs:
	@cd utils/ && \
	python3 docs_index_generator.py --template docsIndexTemplate.jinja --save ../docs/source/index.rst && \
	cd ../docs/ && \
	$(MAKE) html && \
	sphinx-build -b rinoh source _build/rinoh


package:
	@pip install --upgrade .
