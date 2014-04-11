#!/usr/bin/env python

# -----------------------------------------------------------------------------
# This work is licensed under the Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License. To view a
# copy of this license, visit
# http://creativecommons.org/licenses/by-nc-sa/4.0/.
# -----------------------------------------------------------------------------

import logging
import os
import sys

from runipy.notebook_runner import NotebookRunner, NotebookError
from IPython.nbformat.current import read

# Taken and modified from
# https://github.com/paulgb/runipy/blob/master/runipy/main.py
# See licenses/ directory for runipy license.
def main():
    log_format = '%(asctime)s %(message)s'
    log_datefmt = '%m/%d/%Y %I:%M:%S %p'
    ignore_dirs = ['.git', '.ipynb_checkpoints']

    logging.basicConfig(level=logging.DEBUG, format=log_format,
                        datefmt=log_datefmt)

    for root, dirs, files in os.walk('.'):
        for ignore_dir in ignore_dirs:
            if ignore_dir in dirs:
                dirs.remove(ignore_dir)

        for name in files:
            if name.endswith('.ipynb'):
                nbpath = os.path.normpath(os.path.join(root, name))

                logging.info('Reading notebook %s', nbpath)
                with open(nbpath) as nbfile:
                    notebook = read(nbfile, 'json')

                runner = NotebookRunner(notebook)

                try:
                    runner.run_notebook()
                except NotebookError as e:
                    logging.error('An error occurred while executing notebook '
                                  '%s. Exiting with nonzero exit status',
                                  nbpath)
                    sys.exit(1)


if __name__ == '__main__':
    main()
