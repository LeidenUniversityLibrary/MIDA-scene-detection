"""Add scene numbers to frames and aggregate frame data per scene.

Usage::

    $ python mark_scenes.py --output-frames frames-with-scenes.csv --output-scenes scenes.csv frames-wide.csv

"""
import pandas as pd
import click
import os.path


@click.command()
@click.option('--output-scenes', type=click.Path(file_okay=True))
@click.option('--output-frames', type=click.Path(file_okay=True))
@click.argument('input-frames', type=click.Path(file_okay=True), required=True)
def main(input_frames, output_scenes, output_frames):
    """
    Aggregate data from frames into scene data

    Saves results in two files: scene data and a copy of the input frames with
    scene numbers.
    """

    csv_dtypes = {
        "frame": "int64",
        "pkt_pts_time": "float64",
        "lavfi_scd_mafd": "float64",
        "lavfi_scd_score": "float64",
        "lavfi_scd_time": "float64",
        "lavfi_blackframe_pblack": "float64"
    }
    use_cols = ["frame","pkt_pts_time","lavfi_scd_mafd","lavfi_scd_score","lavfi_scd_time","lavfi_blackframe_pblack",
        "lavfi_signalstats_HUEAVG",
        "lavfi_signalstats_HUEMED",
        "lavfi_signalstats_SATAVG",
        "lavfi_signalstats_SATHIGH",
        "lavfi_signalstats_SATLOW",
        "lavfi_signalstats_SATMAX",
        "lavfi_signalstats_SATMIN",
        "lavfi_signalstats_UAVG",
        "lavfi_signalstats_UDIF",
        "lavfi_signalstats_UHIGH",
        "lavfi_signalstats_ULOW",
        "lavfi_signalstats_UMAX",
        "lavfi_signalstats_UMIN",
        "lavfi_signalstats_VAVG",
        "lavfi_signalstats_VDIF",
        "lavfi_signalstats_VHIGH",
        "lavfi_signalstats_VLOW",
        "lavfi_signalstats_VMAX",
        "lavfi_signalstats_VMIN",
        "lavfi_signalstats_YAVG",
        "lavfi_signalstats_YDIF",
        "lavfi_signalstats_YHIGH",
        "lavfi_signalstats_YLOW",
        "lavfi_signalstats_YMAX",
        "lavfi_signalstats_YMIN"]
    frames_data = pd.read_csv(input_frames, dtype = csv_dtypes, index_col="frame", usecols=use_cols)

    # Make sure the first frame starts a scene by setting the `scd_time`
    frames_data.loc[0, "lavfi_scd_time"] = 0.0

    # Black frames should start new scenes too
    frames_data.loc[:, "black_frames"] = frames_data["lavfi_blackframe_pblack"].rolling(2, min_periods=1, center=True).count()
    frames_data.loc[frames_data.black_frames == 1.0, "lavfi_scd_time"] = frames_data.pkt_pts_time

    # Fill down the scene detection time to allow grouping frames by scene
    frames_data["lavfi_scd_time"].fillna(method="pad", inplace=True)

    scene_numbers = frames_data.groupby("lavfi_scd_time").ngroup()
    print(scene_numbers.head())

    # Join the scene indices with the original frame list
    frames_with_scenes = frames_data.assign(scene=scene_numbers)
    print(frames_with_scenes.head())
    if output_frames is None:
        output_frames = os.path.splitext(input_frames)[0] + "-frames-with-scenes.csv"

    frames_with_scenes.to_csv(output_frames)

    # Determine length of scenes
    frames_by_scene = frames_data.reset_index().groupby("lavfi_scd_time")
    scene_sizes = frames_by_scene.size()
    print(scene_sizes.head())

    frame_duration = frames_data.loc[1, "pkt_pts_time"]

    scenes = frames_by_scene.agg(
        last_pts=("pkt_pts_time", "max"),
        duration=("pkt_pts_time", lambda x: round(x.max() - x.min() + frame_duration, 5)),
        first_frame=("frame", "min"),
        last_frame=("frame", "max")
        )\
        .assign(number_of_frames=scene_sizes,
        low_mafd=frames_by_scene["lavfi_scd_mafd"].quantile(0.2).round(5),
        median_mafd=frames_by_scene["lavfi_scd_mafd"].quantile(0.5).round(5),
        high_mafd=frames_by_scene["lavfi_scd_mafd"].quantile(0.8).round(5),
        high95_mafd=frames_by_scene["lavfi_scd_mafd"].quantile(0.95).round(5),
        scd_score=frames_by_scene["lavfi_scd_score"].first())\
        .join(frames_by_scene[["lavfi_signalstats_YAVG",
        "lavfi_signalstats_YDIF",
        "lavfi_signalstats_YHIGH",
        "lavfi_signalstats_YLOW",
        "lavfi_signalstats_YMAX",
        "lavfi_signalstats_YMIN"]].mean().round(5))\
        .reset_index()
    scenes.index.name = "scene"
    print(scenes.head())

    # Save the scenes information to a new file based on the input file name
    if output_scenes is None:
        output_scenes = os.path.splitext(input_frames)[0] + "-scenes.csv"
    scenes.to_csv(output_scenes)


if __name__ == '__main__':
    main()