import argparse
import json
import os
import logging
import traceback as tb

import coco_exporter
import coco_downloader

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def export(file_input, file_output, to_download):
    "Uses COCO exporter function from_json to convert labelbox JSON into MS COCO format."
    try:
        artifact = '{}/coco.json'.format(file_output)
        os.makedirs(file_output, exist_ok=True)

        print(to_download)
        # ========== my changes ==========
        if to_download:
            LOGGER.info('Downloading images')

            coco_downloader.download_images(file_output)

            LOGGER.info('Finished downlaoding images')
        else:
            LOGGER.info('Not downlaoding images')
        # ========== my changes ==========

        LOGGER.info('Creating coco export')

        coco_exporter.from_json(file_input, artifact)

        LOGGER.info('Done saving coco export')

    except Exception as e:
        tb.print_exc()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_input', help  ='File path to Labelbox JSON to parse export')
    parser.add_argument('file_output', help ='File path to desired output directory for export asset')
    parser.add_argument('to_download', help ='Boolean: whether to download to file output path')

    args = parser.parse_args()

    file_input = args.file_input
    assert file_input

    file_output = args.file_output
    assert file_output

    to_download = args.file_output
    assert to_download

    export(file_input, file_output, to_download)
