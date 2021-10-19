from sumo_output_parsers import LoopDetectorParser, LoopDetectorMatrixObject
from sumo_output_parsers import FCDFileParser, FcdMatrixObject
from sumo_output_parsers import SummaryFileParser, StatisticFileParser
from sumo_output_parsers import CollisionFileParser, CollisionMatrixObject
from sumo_output_parsers import TrafficAnimationVisualizer
from tempfile import mkdtemp
from pathlib import Path

path_fcd_output = Path('tests/resources/output/fcd-output.xml')
path_loop_output = Path('tests/resources/output/loop.out.xml')
path_collision_output = Path('tests/resources/output/collision-output.xml')
path_summary_output = Path('tests/resources/output/summary-output.xml')
path_statistic_output = Path('tests/resources/output/statistic-output.xml')
path_net = Path('tests/resources/grid.net.xml')

path_output = Path(mkdtemp())

# saving matrix from fcd-output.
fcd_parser = FCDFileParser(path_fcd_output)
for metric in fcd_parser.get_attributes():
    fcd_matrix_obj = fcd_parser.xml2matrix(metric)
    fcd_matrix_obj.to_pickle(path_output.joinpath(f'fcd-matrix-{metric}.pickle'))

# saving matrix from loop-output.
loop_parser = LoopDetectorParser(path_loop_output)
print(loop_parser.get_attributes())
for metric in loop_parser.get_attributes():
    loop_metric_matrix_obj = loop_parser.xml2matrix(metric)
    loop_metric_matrix_obj.to_pickle(path_output.joinpath(f'loop-detector-{metric}.pickle'))

# saving matrix from collision-output
collision_parser = CollisionFileParser(path_collision_output)
print(collision_parser.get_attributes())
for metric in collision_parser.get_attributes():
    collision_metric_matrix_obj = collision_parser.xml2matrix(metric)
    collision_metric_matrix_obj.to_pickle(path_output.joinpath(f'collision-{metric}.pickle'))

# saving csv of summary and statistics
df_summary = SummaryFileParser(path_summary_output).xml2csv()
df_statistic = StatisticFileParser(path_statistic_output).xml2csv()

# generating animation
path_video = path_output.joinpath('video.mp4')
traffic_animation = TrafficAnimationVisualizer(path_sumo_net=path_net, path_fcd_xml=path_fcd_output)
traffic_animation.generate_animation(path_video_output=path_video, n_parallel=4)
