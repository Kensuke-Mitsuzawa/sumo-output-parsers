import pathlib
from typing import Optional, Tuple, List, Dict

import matplotlib.patches
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy

import SumoNetVis
import hvplot.pandas  # noqa
import geopandas
import holoviews
from bokeh.resources import INLINE
from shapely.geometry import Point

from sumo_output_parsers.definition_parser.detectors_det_parser import DetectorDefinitionParser, \
    DetectorPositions, LanePosition
from sumo_output_parsers.logger_unit import logger


class DetectorPositionVisualizer(object):
    def __init__(self,
                 path_sumo_net: pathlib.Path,
                 path_sumo_detector: pathlib.Path):
        self.path_sumo_net = path_sumo_net
        self.detector_parsers = DetectorDefinitionParser(path_sumo_detector)

    @staticmethod
    def clean_up_detector_id(detector_id: str) -> bool:
        if ':' in detector_id:
            return False
        else:
            return True

    @staticmethod
    def _collect_lane_info(sumo_net: SumoNetVis.Net) -> Dict[str, LanePosition]:
        """Collect lane information from net.xml file.

        Args:
            sumo_net:

        Returns: {lane-id: LanePosition}
        """
        lane_def = {}
        for e in sumo_net.edges.values():
            if e.function == 'internal':
                continue
            # end if
            for l_obj in e.lanes:
                lane_id = l_obj.id
                edge_id = e.id
                incoming_connection = [c_obj.from_lane.id for c_obj in l_obj.incoming_connections
                                       if c_obj.from_lane is not None and c_obj.from_edge.function != 'internal']
                outgoing_connection = [c_obj.to_lane.id for c_obj in l_obj.outgoing_connections
                                       if c_obj.to_lane is not None and c_obj.from_edge.function != 'internal']
                lane_def_obj = LanePosition(
                    lane_id=lane_id,
                    lane_number=l_obj.index,
                    edge_id=edge_id,
                    lane_from=incoming_connection,
                    lane_to=outgoing_connection,
                    lane_position_xy=l_obj.shape,
                    speed=l_obj.speed,
                    sumo_net_vis_lane_obj=l_obj
                )
                lane_def[lane_id] = lane_def_obj
            # end for
        # end for
        return lane_def

    @staticmethod
    def __decide_detector_position(detector_definition: DetectorPositions,
                                   lane2lane_def: Dict[str, LanePosition]) -> Tuple[Point, str]:
        """Decide a detector position 'left-hand' or 'right-hand' on a lane.
        The algorithm is that
        if all incoming-lanes have smaller x position, the detector position is 'right-hand'
        if all incoming-lanes have bigger x positions, then the detector position is 'left-hand'.
        else 'unknown', then returns center of the lane.
        """
        incoming_lanes = detector_definition.lane_object.lane_from
        positions_incoming = [lane2lane_def[l_id].lane_position_xy.bounds for l_id in incoming_lanes
                              if detector_definition.lane_object.sumo_net_vis_lane_obj.parentEdge.id != lane2lane_def[l_id].sumo_net_vis_lane_obj.parentEdge.id]
        x_right_most_incoming = [t[2] for t in positions_incoming]
        y_right_most_incoming = [t[3] for t in positions_incoming]

        positions_outgoing = [lane2lane_def[l_id].lane_position_xy.bounds for l_id in detector_definition.lane_object.lane_to
                              if detector_definition.lane_object.sumo_net_vis_lane_obj.parentEdge.id != lane2lane_def[l_id].sumo_net_vis_lane_obj.parentEdge.id]
        x_smallest_out = [t[0] for t in positions_outgoing]
        y_smallest_out = [t[2] for t in positions_outgoing]

        xy_current_lane_bound = detector_definition.lane_object.lane_position_xy.bounds
        xy_right_most_current = (xy_current_lane_bound[2], xy_current_lane_bound[3])
        is_x_current_lane_big = [True if x_in < xy_right_most_current[0] else False for x_in in x_right_most_incoming
                                 if x_in != xy_right_most_current[0]]
        is_y_current_lane_big = [True if y_in < xy_right_most_current[1] else False for y_in in y_right_most_incoming
                                 if y_in != xy_right_most_current[1]]
        lane_shape = 'left-right' \
            if abs(xy_current_lane_bound[2] - xy_current_lane_bound[0]) > abs(xy_current_lane_bound[3] - xy_current_lane_bound[1]) \
            else 'top-down'

        detector_top = numpy.mean([
            [xy_current_lane_bound[0], xy_current_lane_bound[3]],
            [xy_current_lane_bound[2], xy_current_lane_bound[3]]], axis=0)
        detector_down = numpy.mean([
            [xy_current_lane_bound[0], xy_current_lane_bound[1]],
            [xy_current_lane_bound[2], xy_current_lane_bound[1]]], axis=0)
        detector_left = numpy.mean([
            [xy_current_lane_bound[0], xy_current_lane_bound[1]],
            [xy_current_lane_bound[0], xy_current_lane_bound[3]]], axis=0)
        detector_right = numpy.mean([
            [xy_current_lane_bound[2], xy_current_lane_bound[1]],
            [xy_current_lane_bound[2], xy_current_lane_bound[3]]], axis=0)

        if lane_shape == 'left-right':
            if len(x_right_most_incoming) == 0:
                # then, starting lane. Check out-going lane.
                if all([True if x > xy_right_most_current[0] else False for x in x_smallest_out]):
                    return Point(*detector_right), 'right'
                else:
                    return Point(*detector_left), 'left'
                # end if
            elif all(is_x_current_lane_big):
                return Point(*detector_right), 'right'
            elif all(not x for x in is_x_current_lane_big):
                return Point(*detector_left), 'left'
            else:
                logger.warning(f'{detector_definition.detector_id} is out-of rules. Set centroid instead.')
                return detector_definition.lane_object.lane_position_xy.centroid, 'centroid'
        else:
            if len(y_right_most_incoming) == 0:
                # then, starting lane. Check out-going lane.
                if all([True if y > xy_right_most_current[1] else False for y in y_smallest_out]):
                    return Point(*detector_top), 'top'
                else:
                    return Point(*detector_down), 'down'
                # end if
            elif all(is_y_current_lane_big):
                return Point(*detector_top), 'top'
            elif all(not y for y in is_y_current_lane_big):
                return Point(*detector_down), 'down'
            else:
                logger.warning(f'{detector_definition.detector_id} is out-of rules. Set centroid instead.')
                return detector_definition.lane_object.lane_position_xy.centroid, 'centroid'

    def _collect_detector_info(self) -> Tuple[List[DetectorPositions], SumoNetVis.Net]:
        # get definition of detectors
        detector_definitions = self.detector_parsers.xml2definitions()
        # self.net.plot(ax=ax)
        net = SumoNetVis.Net(self.path_sumo_net.__str__())
        # mapping of lane-id into lane position
        lane2lane_def = self._collect_lane_info(net)
        # update detector object with lane positions
        for detector_def in detector_definitions:
            assert detector_def.lane_id in lane2lane_def, \
                f"key {detector_def.lane_id} does not exist in net.xml definition."
            detector_def.lane_object = lane2lane_def[detector_def.lane_id]
            # decide detector position based on incoming lane information
            det_position, det_position_type = self.__decide_detector_position(detector_def, lane2lane_def)
            detector_def.detector_position_xy = det_position
            detector_def.detector_position_type = det_position_type
        # end for
        return detector_definitions, net

    def get_detector_df(self,
                        detector_definitions: Optional[List[DetectorPositions]] = None,
                        position_visualization: str = 'left') -> geopandas.GeoDataFrame:
        """Generate a `GeoDataFrame` of detectors.
        """
        assert position_visualization in ('left', 'right', 'center')
        if detector_definitions is None:
            detector_definitions, sumo_net = self._collect_detector_info()
        # end if
        d = {
            'detector-id': [d.detector_id for d in detector_definitions],
            'geometry': [detector_def.detector_position_xy for detector_def in detector_definitions],
            'lane-id': [d.lane_id for d in detector_definitions],
            'detector-position-type': [d.detector_position_type for d in detector_definitions]
        }
        df = geopandas.GeoDataFrame(d)
        return df

    @staticmethod
    def _get_lanes_positions(sumo_net: SumoNetVis.Net) -> geopandas.GeoDataFrame:
        """Generate a `GeoDataFrame` of lanes.

        Returns: GeoPandas object
        """
        # records of [lane-id, detector-poly]
        d = {
            'lane-id': [l.id for e in sumo_net.edges.values() for l in e.lanes if l.shape.is_empty is False],
            'geometry': [l.shape for e in sumo_net.edges.values() for l in e.lanes if l.shape.is_empty is False]
        }

        gdf = geopandas.GeoDataFrame(d)
        return gdf

    def visualize_interactive(self,
                              path_save_html: pathlib.Path,
                              width: int = 600,
                              height: int = 500) -> holoviews.core.overlay.Overlay:
        """Visualization with interactive functions thank to hvplot.

        Args:
            path_save_html: path to save the generated html.
            width: size of plot.
            height: size of plot.

        Returns:
            holoviews.core.overlay.Overlay
        """
        assert path_save_html.parent.exists()
        detector_definitions, sumo_net = self._collect_detector_info()
        sumo_net_df = self._get_lanes_positions(sumo_net)
        detector_df = self.get_detector_df(detector_definitions)

        plot = sumo_net_df.hvplot(width=width, height=height, hover_cols='lane-id', legend=False) * \
               detector_df.hvplot(color='orange', hover_cols=['detector-id', 'lane-id', 'detector-position-type'])
        hvplot.save(plot, path_save_html, resources=INLINE)
        logger.info(f'saved at {path_save_html}')
        return plot

    def visualize(self,
                  path_save_png: pathlib.Path,
                  position_visualization: str = 'left',
                  is_detector_name: bool = False) -> Axes:
        """Visualization of detector positions.
        Currently, the detector position is not exact but approximation.
        The visualization shows only lane where a detector stands.

        Args:
            path_save_png: path to save png file.
            position_visualization: 'left', 'right', 'center'. The option on a lane to render a detector.
            is_detector_name: render detector name if True else nothing.
        Returns:
            ax: matplotlib layer object
        """
        assert position_visualization in ('left', 'right', 'center')
        detector_definitions, sumo_net = self._collect_detector_info()
        # visualizations
        fig, ax = plt.subplots()
        # self.net.plot(ax=ax)
        sumo_net.plot(ax=ax)
        # update detector object with lane positions
        for detector_def in detector_definitions:
            point_position: Point = detector_def.detector_position_xy
            ax.scatter(point_position.x, point_position.y)
            if is_detector_name:
                ax.annotate(detector_def.detector_id, (point_position.x, point_position.y))
            # end if
        # end for
        fig.savefig(path_save_png.__str__(), bbox_inches='tight')
        logger.info(f'saved at {path_save_png}')
        return ax
