import numpy as np
import dataclasses
from typing import List, Dict, Optional
from pathlib import Path
from tqdm import tqdm
from scipy.sparse import csr_matrix

from sumo_output_parsers.logger_unit import logger
from sumo_output_parsers.models.parser import ParserClass
from sumo_output_parsers.models.matrix import MatrixObject


@dataclasses.dataclass
class FcdMatrixObject(MatrixObject):
    """
    Attributes:
        matrix (2d-array): a 2d-array which contains {value_type}.
        interval_begins (1d-array): a 1d-array which contains a start of an interval-time.
        value_type: name of type that a matrix object has.
        time_interval: length of time-interval.
    """
    matrix: csr_matrix
    lane2id: Dict[str, int]
    car2id: Dict[str, int]
    interval_begins: np.ndarray
    interval_end: Optional[np.ndarray] = None
    value_type: str = 'lane-id'


class FCDFileParser(ParserClass):
    def __init__(self, path_file: Path):
        """A handler class that parse output-files of Sumo's output.
        Args:
            path_file: pathlib.Path object that leads into output file's path.
        """
        super().__init__(path_file)

    def xml2matrix(self,
                   target_element: str = 'timestamp') -> FcdMatrixObject:
        """generates matrix object with the specified key name.
        :param target_element: a name of key which corresponds to values of the matrix.
        :return: MatrixObject
        """
        route_stack = []
        car_ids = []
        lane_ids = []
        seq_begin = []
        time_interval = 0
        __time_interval: Optional[float] = None
        logger.info('Parsing FCD xml...')
        for elem in tqdm(self.getelements(str(self.path_file), tag=target_element)):
            seq_begin.append(elem.attrib['time'])
            time_interval += 1
            element_time_interval = []
            __car_ids = []
            __lane_ids = []
            for vehicle_tree in elem.findall('vehicle'):
                __lane_ids.append(vehicle_tree.attrib['lane'])
                __car_ids.append(vehicle_tree.attrib['id'])
                element_time_interval.append(
                    (time_interval, vehicle_tree.attrib['id'], vehicle_tree.attrib['lane']))
            # end for
            car_ids += list(set(__car_ids))
            lane_ids += list(set(__lane_ids))
            route_stack += element_time_interval
        # end for
        del __lane_ids
        del __car_ids

        car_ids = list(sorted(list(set(car_ids))))
        lane_ids = list(sorted(list(set(lane_ids))))
        logger.info(f'Parsing done. n-time-interval={time_interval} car-types={len(car_ids)} lane-types={len(lane_ids)}')
        # convert lane-id & car-id into integer
        car2id = {car_id: i for i, car_id in enumerate(car_ids)}
        lane2id = {lane_id: i for i, lane_id in enumerate(lane_ids)}

        # data
        __row = []
        __col = []
        __data = []
        for data_t in route_stack:
            __col.append(data_t[0])
            __row.append(car2id[data_t[1]])
            __data.append(lane2id[data_t[2]])
        # end for
        col = np.array(__col)
        row = np.array(__row)
        data = np.array(__data)
        del __row, __col, __data
        assert len(col) == len(data) == len(row)
        print(f'row-size={row.max()} column-size={col.max()}')
        # matrix-size
        matrix_size = (row.max() + 1, time_interval + 1)
        lane_matrix = csr_matrix((data, (row, col)), shape=matrix_size)

        begin_time_vector = np.array(seq_begin)
        assert len(lane_matrix.shape) == 2, f'The method expects 2nd array. But it detects {lane_matrix.shape} object. ' \
                                            f'Check your xml file at {self.path_file}'
        return FcdMatrixObject(
            matrix=lane_matrix,
            lane2id=lane2id,
            car2id=car2id,
            interval_begins=begin_time_vector)
