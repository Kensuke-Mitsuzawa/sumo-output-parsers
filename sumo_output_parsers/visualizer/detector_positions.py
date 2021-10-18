import pathlib
from typing import Optional, Tuple, List

import matplotlib.patches
import matplotlib.pyplot as plt

import numpy as np
import SumoNetVis
import hvplot.pandas  # noqa
import geopandas
from bokeh.resources import INLINE
from shapely.geometry import Point

from sumo_output_parsers.definition_parser.detectors_det_parser import DetectorDefinitionParser, DetectorPositions
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

    def _collect_detector_info(self) -> Tuple[List[DetectorPositions], SumoNetVis.Net]:
        # get definition of detectors
        detector_definitions = self.detector_parsers.xml2definitions()
        # self.net.plot(ax=ax)
        net = SumoNetVis.Net(self.path_sumo_net.__str__())
        # mapping of lane-id into lane position
        lane2shape = {l.id: l for e in net.edges.values() for l in e.lanes
                      if e.function != 'internal' and self.clean_up_detector_id(l.id) is True}
        # update detector object with lane positions
        for detector_def in detector_definitions:
            lane_obj = lane2shape[detector_def.lane_id]
            # poly = matplotlib.patches.Polygon(lane_obj.shape.boundary.coords, True, **kwargs)
            poly = matplotlib.patches.Polygon(lane_obj.shape.boundary.coords, True)
            detector_def.lane_position_xy = poly.xy
            # the detector position depends on lane direction. The detector stands at the end of the lane normally.
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

        seq_geometry = []
        for detector_def in detector_definitions:
            if position_visualization == 'left':
                x, y = detector_def.lane_position_xy[4]
            elif position_visualization == 'right':
                x, y = detector_def.lane_position_xy[1]
            elif position_visualization == 'center':
                x = np.mean([t[0] for t in detector_def.lane_position_xy])
                y = np.mean([t[1] for t in detector_def.lane_position_xy])
            else:
                raise NotImplementedError()
            # end if
            seq_geometry.append(Point(x, y))
        # end for

        d = {
            'detector-id': [d.detector_id for d in detector_definitions],
            'geometry': seq_geometry,
            'lane-id': [d.lane_id for d in detector_definitions]
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
            'lane-id': [l.id for e in sumo_net.edges.values() for l in e.lanes],
            'geometry': [l.shape for e in sumo_net.edges.values() for l in e.lanes]
        }
        gdf = geopandas.GeoDataFrame(d)
        return gdf

    def visualize_interactive(self,
                              path_save_html: pathlib.Path,
                              width: int = 600,
                              height: int = 500):
        """Visualization with interactive functions thank to hvplot.

        Args:
            path_save_html: path to save the generated html.
            width: size of plot.
            height: size of plot.
        """
        assert path_save_html.parent.exists()
        detector_definitions, sumo_net = self._collect_detector_info()
        sumo_net_df = self._get_lanes_positions(sumo_net)
        detector_df = self.get_detector_df(detector_definitions)

        plot = sumo_net_df.hvplot(width=width, height=height, hover_cols='lane-id', legend=False) * \
               detector_df.hvplot(color='orange', hover_cols=['detector-id', 'lane-id'])
        hvplot.save(plot, path_save_html, resources=INLINE)
        logger.info(f'saved at {path_save_html}')

    def visualize(self,
                  path_save_png: pathlib.Path,
                  position_visualization: str = 'left',
                  is_detector_name: bool = True):
        """Visualization of detector positions.
        Currently, the detector position is not exact but approximation.
        The visualization shows only lane where a detector stands.

        Args:
            path_save_png: path to save png file.
            position_visualization: 'left', 'right', 'center'. The option on a lane to render a detector.
            is_detector_name: render detector name if True else nothing.
        """
        assert position_visualization in ('left', 'right', 'center')
        detector_definitions, sumo_net = self._collect_detector_info()
        # visualizations
        fig, ax = plt.subplots()
        # self.net.plot(ax=ax)
        sumo_net.plot(ax=ax)
        # update detector object with lane positions
        for detector_def in detector_definitions:
            if position_visualization == 'left':
                x, y = detector_def.lane_position_xy[4]
            elif position_visualization == 'right':
                x, y = detector_def.lane_position_xy[1]
            elif position_visualization == 'center':
                x = np.mean([t[0] for t in detector_def.lane_position_xy])
                y = np.mean([t[1] for t in detector_def.lane_position_xy])
            else:
                raise NotImplementedError()
            # end if
            ax.scatter(x, y)
            if is_detector_name:
                ax.annotate(detector_def.detector_id, (x, y))
            # end if
        # end for
        fig.savefig(path_save_png.__str__(), bbox_inches='tight')
        logger.info(f'saved at {path_save_png}')
