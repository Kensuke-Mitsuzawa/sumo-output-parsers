import pickle
from pathlib import Path
from sumo_output_parsers.visualizer.detector_positions import DetectorPositionVisualizer

from tempfile import mkdtemp
from sumo_output_parsers.logger_unit import logger


def test_detector_positions(resource_path_root: Path):
    assert resource_path_root.exists()
    visualizer = DetectorPositionVisualizer(
        path_sumo_net=resource_path_root.joinpath('grid.net.xml'),
        path_sumo_detector=resource_path_root.joinpath('grid_detectors.det.xml')
    )
    path_tmp_dir = mkdtemp()
    path_png = Path(path_tmp_dir).joinpath('tmp.png')
    visualizer.visualize(path_png)
    path_html = Path(path_tmp_dir).joinpath('tmp.html')
    visualizer.visualize_interactive(path_html)


if __name__ == '__main__':
    test_detector_positions(Path('../resources/').absolute())