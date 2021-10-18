import dataclasses
from typing import Tuple, List, Optional
from pathlib import Path
from collections import namedtuple

from sumo_output_parsers.logger_unit import logger
from sumo_output_parsers.models.parser import ParserClass

LanePosition = namedtuple('LanePosition', ('x', 'y'))


@dataclasses.dataclass
class DetectorPositions(object):
    """
    """
    detector_id: str
    lane_id: str
    detector_position: float
    lane_position_xy: Optional[Tuple[LanePosition, LanePosition, LanePosition, LanePosition]] = None


class DetectorDefinitionParser(ParserClass):
    def __init__(self,
                 path_detectors_det: Path):
        super().__init__(path_detectors_det)
        self.key_attribute_name = 'e1Detector'

    def xml2matrix(self, target_element: str):
        raise NotImplementedError()

    def xml2definitions(self) -> List[DetectorPositions]:
        detectors = []
        for elem in self.getelements(str(self.path_file), self.key_attribute_name):
            position_def = DetectorPositions(
                detector_id=elem.attrib['id'],
                lane_id=elem.attrib['lane'],
                detector_position=elem.attrib['pos'])
            detectors.append(position_def)
        # end for
        return detectors
