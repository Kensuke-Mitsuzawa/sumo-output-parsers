import pickle
from pathlib import Path
from sumo_output_parsers.visualizer.traffic_animation import TrafficAnimationVisualizer

from tempfile import mkdtemp
from sumo_output_parsers.logger_unit import logger


def test_traffic_animation(resource_path_root: Path):
    visualizer = TrafficAnimationVisualizer(
        # path_sumo_net=resource_path_root.joinpath('grid.net.xml'),
        path_sumo_net=resource_path_root.joinpath('shenzhen_bantian.net.xml'),
        path_fcd_xml=resource_path_root.joinpath('output/fcd-output.xml')
    )
    path_video = Path(mkdtemp()).joinpath('video.mp4')
    visualizer.generate_animation(intervals=-1, path_video_output=path_video, frames_auto_adjustment=20)


if __name__ == '__main__':
    # test_traffic_animation(Path('../resources/').absolute())
    test_traffic_animation(Path('/home/kensuke-mi/Desktop/2020-12-22-modification-teleport').absolute())
