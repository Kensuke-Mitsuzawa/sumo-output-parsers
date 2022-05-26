import pytest
from pathlib import Path
from tempfile import mkdtemp
from matplotlib import pyplot as plt
from uuid import uuid4


@pytest.mark.visualization
def test_detector_positions_visualize(resource_path_root: Path):
    from sumo_output_parsers.visualizer.detector_positions import DetectorPositionVisualizer
    assert resource_path_root.exists()
    visualizer = DetectorPositionVisualizer(
        path_sumo_net=resource_path_root.joinpath('grid.net.xml'),
        path_sumo_detector=resource_path_root.joinpath('grid_detectors.det.xml')
    )
    fig, ax = plt.subplots(figsize=(15, 15))
    path_tmp_dir = mkdtemp()
    # with specific detector-ids
    path_png = Path(path_tmp_dir).joinpath(f'{uuid4()}.png')
    visualizer.visualize(ax=ax,
                         fig_obj=fig,
                         path_save_png=path_png,
                         is_detector_name=True,
                         target_detector_ids={'left0A0_0': 'red', 'B0A0_1': 'blue'})
    # with specific detector-ids (without colors)
    fig, ax = plt.subplots(figsize=(15, 15))
    path_png = Path(path_tmp_dir).joinpath(f'{uuid4()}.png')
    visualizer.visualize(ax=ax,
                         fig_obj=fig,
                         path_save_png=path_png,
                         is_detector_name=True,
                         target_detector_ids={'left0A0_0': None, 'B0A0_1': None})
    # all
    fig, ax = plt.subplots(figsize=(15, 15))
    path_png = Path(path_tmp_dir).joinpath(f'{uuid4()}.png')
    visualizer.visualize(ax=ax,
                         fig_obj=fig,
                         path_save_png=path_png,
                         is_detector_name=False)


@pytest.mark.visualization
def test_detector_positions_visualize_interactive(resource_path_root: Path):
    from sumo_output_parsers.visualizer.detector_positions import DetectorPositionVisualizer
    assert resource_path_root.exists()
    visualizer = DetectorPositionVisualizer(
        path_sumo_net=resource_path_root.joinpath('grid.net.xml'),
        path_sumo_detector=resource_path_root.joinpath('grid_detectors.det.xml')
    )
    path_tmp_dir = mkdtemp()
    path_html = Path(path_tmp_dir).joinpath('tmp.html')
    visualizer.visualize_interactive(path_html)


if __name__ == '__main__':
    test_detector_positions_visualize(Path('../resources/').absolute())
    test_detector_positions_visualize_interactive(Path('../resources/').absolute())
