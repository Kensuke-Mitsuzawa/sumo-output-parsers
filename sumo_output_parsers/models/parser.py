from pathlib import Path
from typing import Optional, List, Union, Dict, Tuple
from scipy.sparse import csr_matrix
from lxml import etree
import more_itertools

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
        assert path_file.exists()
        self.path_file = path_file

    @staticmethod
    def generate_time2id(time_intervals_begin: List[str]) -> Dict[str, int]:
        __ = {t: i for i, t in enumerate(more_itertools.unique_everseen(time_intervals_begin))}
        return __

    @staticmethod
    def detect_data_type_time(time_interval_begin: List[Union[str, int]],
                              is_traverse_all: bool = False) -> object:
        max_search = 10
        time_dtype = None
        for i, t in enumerate(time_interval_begin):
            try:
                t_int = int(t)
                time_dtype = float
            except ValueError:
                time_dtype = str

            if is_traverse_all is False and i == max_search:
                return time_dtype
            # end if
        # end for
        return time_dtype

    @staticmethod
    def generate_csr_matrix(data_stack: List[Tuple[str, str, Union[str, int, float]]],
                            row_index2id: Dict[str, int],
                            time_interval: int,
                            data_index2id: Dict[str, int] = None,
                            col_index2id: Dict[str, int] = None) -> csr_matrix:
        # data
        __row = []
        __col = []
        __data = []
        for data_t in data_stack:
            __col.append(data_t[0])
            assert isinstance(data_t[1], str), 'The 1st index must be `str` type.'
            __row.append(row_index2id[data_t[1]])
            if data_index2id is not None:
                __data.append(data_index2id[data_t[2]])
            else:
                __data.append(data_t[2])
        # end for
        if col_index2id is not None:
            col = np.array([col_index2id[c] for c in __col])
        else:
            col = np.array(__col, dtype=np.int)
        # end if
        row = np.array(__row)
        data = np.array(__data)
        del __row, __col, __data
        assert len(col) == len(data) == len(row)
        logger.info(f'row-size={row.max()} column-size={col.max()}')
        # matrix-size
        matrix_size = (row.max() + 1, time_interval + 1)
        target_matrix = csr_matrix((data, (row, col)), shape=matrix_size)
        return target_matrix

    @staticmethod
    def getelements(filename_or_file, tag):
        context = iter(etree.iterparse(filename_or_file, events=('start', 'end')))
        _, root = next(context)  # get root element
        for event, elem in context:
            if event == 'end' and elem.tag == tag:
                yield elem
                root.clear()  # preserve memory

    @staticmethod
    def get_attributes(self) -> List[str]:
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