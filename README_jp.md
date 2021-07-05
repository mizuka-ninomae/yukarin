# Yukarin: ディープラーニング声質変換の第１段階の学習コード＋第２段階の学習コード
このリポジトリは、[Become Yukarin: 誰でも好きなキャラの声になれるリポジトリ](https://github.com/Hiroshiba/become-yukarin)の、
第１段階の学習コードを拡張したものです。
（追記）さらに[Become Yukarin](https://github.com/Hiroshiba/become-yukarin)の第２段階の学習コードをマージしました。

[English README](./README.md)

## 推奨環境
* Linux OS
* Python 3.6
* Python 3.7（でも動いた3.8以上はおそらく不可）

## 準備
### 必要なライブラリのインストール
```bash
pip install -r requirements.txt
```

### コードの実行方法（予備知識）
このリポジトリのコードを実行するには、`yukarin`ライブラリをパス（PYTHONPATH）に通す必要があります。
例えばubuntuの場合は`.bashrc`に以下を追記します。

```bash
export PYTHONPATH=/home/[ユーザー名]/yukarin
```

## 第１段階
### 音声データを用意する
入力音声データと、目標音声データを大量に用意し、別々のディレクトリ（例：`input_wav`と`target_wav`）に配置します。
ファイル名は同じである必要があります。
（追記）できるだけ高いサンプリングレートで録音し、サンプリングレート24000に変換する事をおすすめします。
サンプリングレート24000以外の場合、もしくはおかしな変換方法をした場合、エラーを起こす可能性が高いです。

### 音響特徴量を切り出す
入力と目標の音声データそれぞれの音響特徴量ファイルを出力します。

```bash
python scripts/extract_acoustic_feature.py \
    -i './input_wav/*' \
    -o './input_feature/' \
    --sampling_rate 24000

python scripts/extract_acoustic_feature.py \
    -i './target_wav/*' \
    -o './target_feature/' \
    --sampling_rate 24000
```

### データを揃える（アライメントする）
入力と目標の音響特徴量を時間方向に揃えます。
次の例では、`input_feature`と`target_feature`のアライメントデータを`aligned_indexes`に出力します。

```bash
python scripts/extract_align_indexes.py \
    -i1 './input_feature/*.npy' \
    -i2 './target_feature/*.npy' \
    -o './aligned_indexes/'
```

### 周波数の統計量を求める
声の高さの変換に必要な周波数の統計量を、入力・目標データそれぞれに対して求めます。

```bash
python scripts/extract_f0_statistics.py \
    -i './input_feature/*.npy' \
    -o './input_statistics.npy'

python scripts/extract_f0_statistics.py \
    -i './target_feature/*.npy' \
    -o './target_statistics.npy'
```

## 第１段階 学習
### 学習用の設定ファイル`config.json`を作る
`sample_config1.json`の`input_glob`、`target_glob`、`indexes_glob`を変更すればとりあえず動きます。

### 学習する

```bash
python train_1st.py \
    sample_config1.json \
    ./model_stage1/
```

## 第１段階 テスト
テスト用の入力音声データをディレクトリ（例：`test_wav`）に配置し、`voice_change.py`を実行します。

```bash
python scripts/voice_change.py \
    --model_dir         './model_stage1' \
    --config_path       './model_stage1/config.json' \
    --input_statistics  'input_statistics.npy' \
    --target_statistics 'target_statistics.npy' \
    --output_sampling_rate 24000 \
    --test_wave_dir     './test_wav/' \
    --output_dir        './output1/'
    --gpu 0
```

## 第２段階
### 音声データを用意する
大量の目標音声データを用意し、ディレクトリ（例：`target_sr_wav`）に配置します。
（追記）できるだけ高いサンプリングレートで録音し、サンプリングレート24000に変換する事をおすすめします。
サンプリングレート24000以外の場合、もしくはおかしな変換方法をした場合、エラーを起こす可能性が高いです。

### 音響特徴量を作成する

```bash
python scripts/extract_spectrogram_pair.py \
    -i './target_sr_wav/*' \
    -o './target_sr_feature/' \
    --sample_rate 24000
```

## 第２段階 学習
### 学習用の設定ファイル`config.json`を作る
`sample_config2.json`の`input_glob`を変更すればとりあえず動きます。
（追記）本家のconfig.jsonの`train_crop_size`の値は512ですが、うちの環境（GTX1060 メモリ6GB）では動かなかったので128に下げています。

### 学習する

```bashss
python train_2nd.py \
    sample_config2.json \
    ./model_stage2/
```

## 第２段階 テスト
テスト用の入力音声データをディレクトリ（例：`test_wav`）に配置し、`voice_change_with_second_stage.py`を実行します。

```bash
python scripts/voice_change_with_second_stage.py \
    --voice_changer_model_dir    './model_stage1' \
    --voice_changer_config       './model_stage1/config.json' \
    --voice_changer_model_iteration 250000 \
    --super_resolution_model_dir './model_stage2' \
    --super_resolution_config    './model_stage2/config.json' \
    --super_resolution_model_iteration 250000 \
    --input_statistics           'input_statistics.npy' \
    --target_statistics          'target_statistics.npy' \
    --out_sampling_rate 24000 \
    --dataset_input_wave_dir     './input_wav' \
    --dataset_target_wave_dir    './target_wav' \
    --test_wave_dir              './test_wav' \
    --output_dir                 './output2' \
    --gpu 0
```

## License
[MIT License](./LICENSE)
