# Become Yukarin: Convert your voice to favorite voice
Become Yukarin is a repository for voice conversion with a Deep Learning model.
By traingin with a large amount of the original and favorite voice,
The Deep Learning model can convert the original voice to the favorite voice.

* xxxxxxxxx

[Japanese README](./README_jp.md)

## Supported environment
* Linux OS
* Python 3.6

## Preparation
```bash
# install required libraries
pip install -r requirements.txt
```

## Training
To run a Python script for training,
you should set the environment variable `PYTHONPATH` to find the `become_yukarin` library.
For example, you can execute `scripts/extract_acoustic_feature.py` with the following command:

```bash
PYTHONPATH=`pwd` python scripts/extract_acoustic_feature.py ---
```

## Second Stage Model
### Create acoustic feature

```bash
python scripts/extract_spectrogram_pair.py \
    -i './target_sr_wav/*' \
    -o './target_sr_feature/' \
    --sample_rate 24000
```

### Second Stage Train

```bashss
python train_2nd.py \
    sample_config2.json \
    ./model_stage2/
```

## License
[MIT License](./LICENSE)
