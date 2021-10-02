from pathlib import Path
from typing import Optional, List
from lxml import etree

import numpy as np

from sumo_output_parsers.models.matrix import MatrixObject
from sumo_output_parsers.logger_unit import logger


class ParserClass(object):
    def __init__(
            self,
            path_file: Path):
        """A handler class that parse output-files of Sumo's output.
        Args:
            path_file: pathlib.Path object that leads into output file path
        """
        self.path_file = path_file

    @staticmethod
    def getelements(filename_or_file, tag):
        context = iter(etree.iterparse(filename_or_file, events=('start', 'end')))
        _, root = next(context)  # get root element
        for event, elem in context:
            if event == 'end' and elem.tag == tag:
                yield elem
                root.clear()  # preserve memory

    @staticmethod
    def get_attributes() -> List[str]:
        raise NotImplementedError()

    @staticmethod
    def matrix_with_autofill(matrix_stack: List[List[float]]) -> np.ndarray:
        """auto-fill a matrix object with nan value if lengths of lists are different.
        :param matrix_stack: 2nd list. [[value]]
        :return: 2nd ndarray.
        """
        max_length = max([len(l) for l in matrix_stack])
        min_length = min([len(l) for l in matrix_stack])
        if max_length == min_length:
            matrix_value = np.array(matrix_stack)
            return matrix_value
        else:
            matrix_value = np.zeros([len(matrix_stack), max_length])
            logger.warning('The output file different length of elements. I replaced insufficient values with Nan. '
                           'Be careful the existence of Nan values.')
            matrix_value[:] = np.NAN
            for i, j in enumerate(matrix_stack):
                matrix_value[i][0:len(j)] = j
            # end for
            return matrix_value

    def to_array_objects(self, aggregation_on: str) -> MatrixObject:
        raise NotImplementedError()

    def xml2matrix(self, target_element: str):
        raise NotImplementedError()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'ResultFile class for {self.path_file}'