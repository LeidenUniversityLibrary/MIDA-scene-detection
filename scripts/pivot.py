"""
Tidy a CSV file by pivoting
"""
import pandas as pd
import click
import os.path


@click.command()
@click.option('-o', '--output-file', type=click.Path(file_okay=True), required=False)
@click.option('-m', '--header-missing', is_flag=True, help='Set to indicate '
                'that the input file has no header line', required=False)
@click.argument('input_file', type=click.Path(file_okay=True), required=True)
def main(input_file, output_file, header_missing: bool):
    """
    Pivot a CSV file from 'frame,variable,value' format to tidy long format
    """
    if header_missing:
        stacked_data = pd.read_csv(input_file, header=None, names=['frame','variable','value']).fillna("")
    else:
        stacked_data = pd.read_csv(input_file).fillna("")
    print(stacked_data.head())

    pivoted_data = stacked_data.pivot(index="frame", columns="variable", values="value")

    if output_file is None:
        output_file = os.path.basename(input_file) + "-p.csv"

    pivoted_data.to_csv(output_file)


if __name__ == '__main__':
    main()