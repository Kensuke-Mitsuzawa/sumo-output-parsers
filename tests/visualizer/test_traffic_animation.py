import pickle
from pathlib import Path
from sumo_output_parsers.visualizer.traffic_animation import TrafficAnimationVisualizer

from tempfile import mkdtemp
from sumo_output_parsers.logger_unit import logger


def test_traffic_animation(resource_path_root: Path):
    visualizer = TrafficAnimationVisualizer(
        path_sumo_net=resource_path_root.joinpath('grid.net.xml'),
        path_fcd_xml=resource_path_root.joinpath('output/fcd-output.xml'),
        fcd_skip_iteration=100
    )
    path_video = Path(mkdtemp()).joinpath('video.mp4')
    visualizer.generate_animation(intervals=-1, path_video_output=path_video)
    visualizer.generate_animation(intervals=None, path_video_output=path_video, n_samples=100)


if __name__ == '__main__':
    test_traffic_animation(Path('../resources/').absolute())

