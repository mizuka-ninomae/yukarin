"""
extract low and high quality spectrogram data.
"""

import argparse
import glob
import multiprocessing
from pathlib import Path
from pprint import pprint

import numpy
import pysptk
import pyworld
from tqdm import tqdm

from become_yukarin.dataset.dataset import AcousticFeatureProcess
from become_yukarin.dataset.dataset import WaveFileLoadProcess
from become_yukarin.param import AcousticFeatureParam
from become_yukarin.param import VoiceParam

base_voice_param = VoiceParam()
base_acoustic_feature_param = AcousticFeatureParam()

parser = argparse.ArgumentParser()
parser.add_argument('--input_glob', '-i')
parser.add_argument('--output', '-o', type=Path)
parser.add_argument('--sample_rate', type=int, default=base_voice_param.sample_rate)
parser.add_argument('--top_db', type=float, default=base_voice_param.top_db)
parser.add_argument('--pad_second', type=float, default=base_voice_param.pad_second)
parser.add_argument('--frame_period', type=int, default=base_acoustic_feature_param.frame_period)
parser.add_argument('--order', type=int, default=base_acoustic_feature_param.order)
parser.add_argument('--alpha', type=float, default=base_acoustic_feature_param.alpha)
parser.add_argument('--f0_estimating_method', default=base_acoustic_feature_param.f0_estimating_method)
parser.add_argument('--enable_overwrite', action='store_true')
arguments = parser.parse_args()


def generate_file(path):
    out = Path(arguments.output, path.stem + '.npy')
    if out.exists() and not arguments.enable_overwrite:
        return

    # load wave and padding
    wave_file_load_process = WaveFileLoadProcess(
        sample_rate=arguments.sample_rate,
        top_db=arguments.top_db,
        pad_second=arguments.pad_second,
    )
    wave = wave_file_load_process(path, test=True)

    # make acoustic feature
    acoustic_feature_process = AcousticFeatureProcess(
        frame_period=arguments.frame_period,
        order=arguments.order,
        alpha=arguments.alpha,
        f0_estimating_method=arguments.f0_estimating_method,
    )
    feature = acoustic_feature_process(wave, test=True).astype_only_float(numpy.float32)
    high_spectrogram = feature.spectrogram

    fftlen = pyworld.get_cheaptrick_fft_size(arguments.sample_rate)
    low_spectrogram = pysptk.mc2sp(
        feature.mfcc,
        alpha=arguments.alpha,
        fftlen=fftlen,
    )

    # save
    numpy.save(out.absolute(), {
        'low': low_spectrogram,
        'high': high_spectrogram,
    })


def main():
    pprint(vars(arguments))

    arguments.output.mkdir(exist_ok=True)
#    save_arguments(arguments, arguments.output / 'arguments.json')

    paths = [Path(p) for p in glob.glob(arguments.input_glob)]

    pool = multiprocessing.Pool()
    list(tqdm(pool.imap(generate_file, paths), total=len(paths)))


if __name__ == '__main__':
    main()
