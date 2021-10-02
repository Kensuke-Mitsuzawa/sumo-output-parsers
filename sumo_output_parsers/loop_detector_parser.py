import dataclasses
from pathlib import Path
from typing import Optional, List
from itertools import groupby

import numpy

from sumo_output_parsers.logger_unit import logger
from sumo_output_parsers.models.parser import ParserClass
from sumo_output_parsers.models.matrix import MatrixObject


@dataclasses.dataclass
class LoopDetectorMatrixObject(MatrixObject):
    matrix: numpy.ndarray
    detectors: numpy.ndarray
    interval_begins: numpy.ndarray
    interval_end: numpy.ndarray
    value_type: str


class LoopDetectorParser(ParserClass):
    """A handler class that parse output-files of Sumo's output.
    Args:
        path_file: pathlib.Path object that leads into output file's path.
    """
    def __init__(self, path_file: Path):
        super(LoopDetectorParser, self).__init__(path_file)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'ResultFile class for {self.path_file}'

    def xml2matrix(self, target_element: str) -> LoopDetectorMatrixObject:
        """generates matrix object with the specified key name.
        :param target_element: a name of key which corresponds to values of the matrix.
        :return: MatrixObject
        """
        stacks = []
        __time_interval: Optional[float] = None
        for elem in root_soup.find_all('interval'):
            detector_id = elem.get('id')
            time_begin = float(elem.get('begin'))
            time_end = float(elem.get('end'))

            obj_value = elem.get(target_element)
            try:
                if obj_value == '':
                    target_value = 0.0
                elif obj_value is None:
                    target_value = 0.0
                else:
                    target_value = float(elem.get(target_element))
            except ValueError:
                raise SystemError(f'unexpected error during parsing values because of {obj_value}')
            except KeyError:
                keys = elem.attrs.keys()
                raise KeyError(f'Invalid key name. Available keys are {keys}')
            # end try
            stacks.append([detector_id, time_begin, time_end, target_value])
        # end for
        seq_detector_id = []
        matrix_stack = []
        seq_begin = []
        seq_end = []
        for detector_id, g_obj in groupby(sorted(stacks, key=lambda t: t[0]), key=lambda t: t[0]):
            __ = list(sorted([t for t in g_obj], key=lambda t: t[1]))
            seq_begin = [t[1] for t in __]
            seq_end = [t[2] for t in __]
            seq_value = [t[3] for t in __]
            seq_detector_id.append(detector_id)
            matrix_stack.append(seq_value)
        # end for
        detectors = numpy.array(seq_detector_id)

        begin_time_vector = numpy.array(seq_begin)
        end_time_vector = numpy.array(seq_end)
        matrix_value = self.matrix_with_autofill(matrix_stack)
        assert len(matrix_value.shape) == 2, f'The method expects 2nd array. But it detects {matrix_value.shape} object. ' \
                                             f'Check your xml file at {self.path_file}'
        return LoopDetectorMatrixObject(
            matrix=matrix_value,
            detectors=detectors,
            interval_begins=begin_time_vector,
            interval_end=end_time_vector,
            value_type=target_element)

    def to_array_objects(self, aggregation_on: str) -> MatrixObject:
        matrix_obj = self.xml2matrix(root_soup=self.tree_object, target_element=aggregation_on)
        return matrix_obj
