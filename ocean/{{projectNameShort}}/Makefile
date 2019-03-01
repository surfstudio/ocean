.DEFAULT: help

help:
	@echo "\n     USAGE"
	@echo "===============\n"
	@echo "make -B all"
	@echo "       Build documentation and then install package to pip\n"
	@echo "make -B project"
	@echo "       Install src/-codebase to the pip\n"

all: package

package:
	@python3 -m pip install --upgrade .
