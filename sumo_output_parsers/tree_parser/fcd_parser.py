import numpy as np
import dataclasses
import pickle
from typing import List, Dict, Optional, Union
from pathlib import Path
from tqdm import tqdm
from scipy.sparse import csr_matrix

from sumo_output_parsers.logger_unit import logger
from sumo_output_parsers.models.parser import ParserClass
from sumo_output_parsers.models.matrix import MatrixObject


@dataclasses.dataclass
class FcdMatrixObject(MatrixObject):
    """
    """
    matrix: csr_matrix
    value2id: Dict[str, int]
    car2id: Dict[str, int]
    interval_begins: np.ndarray
    value_type: str
    interval_end: Optional[np.ndarray] = None


    @classmethod
    def from_pickle(self, path_pickle: Path) -> "FcdMatrixObject":
        with path_pickle.open('rb') as f:
            data = pickle.load(f)
        return FcdMatrixObject(**data)


class FCDFileParser(ParserClass):
    def __init__(self, path_file: Path):
        """A handler class that parse output-files of Sumo's output.
        Args:
            path_file: pathlib.Path object that leads into output file's path.
        """
        super().__init__(path_file)
        self.name_vehicle_node = 'vehicle'
        self.name_time_node = 'timestep'
        self.pre_defined_attribute = ['id']

    def get_attributes(self, is_traverse_all: bool = False) -> List[str]:
        max_search = 10
        metrics = []
        for search_i, elem in enumerate(self.getelements(str(self.path_file), self.name_vehicle_node)):
            if is_traverse_all is False and search_i == max_search:
                return list(set(metrics))
            # end if
            item_list = [e for e in elem.attrib.keys() if e not in self.pre_defined_attribute]
            metrics += item_list
        # end for
        return list(set(metrics))

    def xml2matrix(self, target_element: str) -> FcdMatrixObject:
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
        __car_ids = []
        __lane_ids = []
        for elem in tqdm(self.getelements(str(self.path_file), tag=self.name_time_node)):
            seq_begin.append(elem.attrib['time'])
            time_interval += 1
            element_time_interval = []
            __car_ids = []
            __lane_ids = []
            for vehicle_tree in elem.findall('vehicle'):
                __lane_ids.append(vehicle_tree.attrib[target_element])
                __car_ids.append(vehicle_tree.attrib['id'])
                element_time_interval.append(
                    (time_interval, vehicle_tree.attrib['id'], vehicle_tree.attrib[target_element]))
            # end for
            car_ids += list(set(__car_ids))
            lane_ids += list(set(__lane_ids))
            route_stack += element_time_interval
        # end for
        del __lane_ids
        del __car_ids

        assert len(car_ids) > 0 and len(lane_ids) > 0 and len(route_stack) > 0, 'Nothing extracted from the FCD output.'

        car_ids = list(sorted(list(set(car_ids))))
        lane_ids = list(sorted(list(set(lane_ids))))
        logger.info(f'Parsing done. n-time-interval={time_interval} car-types={len(car_ids)} value-types={len(lane_ids)}')
        # convert lane-id & car-id into integer
        car2id = {car_id: i for i, car_id in enumerate(car_ids)}
        lane2id = {lane_id: i for i, lane_id in enumerate(lane_ids)}
        time2id = None
        lane_matrix = self.generate_csr_matrix(
            data_stack=route_stack,
            row_index2id=car2id,
            data_index2id=lane2id,
            time_interval=time_interval,
            col_index2id=time2id
        )

        begin_time_vector = np.array(seq_begin)
        assert len(lane_matrix.shape) == 2, f'The method expects 2nd array. But it detects {lane_matrix.shape} object. ' \
                                            f'Check your xml file at {self.path_file}'
        return FcdMatrixObject(
            matrix=lane_matrix,
            value2id=lane2id,
            car2id=car2id,
            interval_begins=begin_time_vector,
            value_type=target_element)