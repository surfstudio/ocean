.DEFAULT: help

help:
	@echo "     USAGE"
	@echo "==============="
	@echo "make -B train"
	@echo "       Starts train.py"
	@echo "make -B dashboard"
	@echo "       Starts MLFlow UI on 0.0.0.0, port 8011"

train:
	@python3 scripts/train.py #-c <some_path> \
#                             -d <some_path> \
#                             -s <some_path> \
#                             -u <username>

dashboard:
	@mlflow ui -h 0.0.0.0 -p 8011
