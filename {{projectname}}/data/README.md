# Data structure

## Raw

Raw is for raw client's data, and nothing more.

## Interim

Preprocessed raw data: subsampled and/or data format checked. Data might be serialized with Pickle or Dill for faster reading from disk.

__NB__: No feature encoding or `nan` values inputing is done here!

## Features

Computed statistics, embedded vectors and other stuff that could be easily joined to the rest of the data.

## Processed

Processed must contain only the data that is ready to be put in models. Is used for quality and performance comparison of different models.

## External

External data from the Internet, like weather, calendars with holidays or maps.
