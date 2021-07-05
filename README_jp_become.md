# Become Yukarin: 誰でも好きなキャラの声に
Become Yukarinは、機械学習（ディープラーニング）で声質変換を実現するリポジトリです。
元の声と好きな声の音声データを大量に用いて機械学習することで、
元の声を好きな声に変換することができるようになります。
* [yukarin](https://github.com/Hiroshiba/yukarin)の登場により、 [become-yukarin](https://github.com/Hiroshiba/become-yukarin)の学習第一段階を使う必要がなくなりました。これは本家のものより第一段階を取り除き、第二段階のパラメータの指定方法を [yukarin](https://github.com/Hiroshiba/yukarin)と統一したバージョンです。


[English README](./README.md)

## 推奨環境
* Linux OS
* Python 3.6

## 準備
### 必要なライブラリをインストール
```bash
pip install -r requirements.txt
```

### コードの実行方法（予備知識）
学習用のPythonスクリプトを実行するには、`become_yukarin`ライブラリをパス（PYTHONPATH）に通す必要があります。
例えば`scripts/extract_acoustic_feature.py`を以下のように書いて、パスを通しつつ実行します。

```bash
PYTHONPATH=`pwd` python scripts/extract_acoustic_feature.py ---
```
## データ作成
### 音声データを用意する
大量の目標音声データを用意し、ディレクトリ（例：`target_sr_wav`）に配置します。

### 音響特徴量を作成する

```bash
python scripts/extract_spectrogram_pair.py \
    -i './target_sr_wav/*' \
    -o './target_sr_feature/' \
    --sample_rate 24000
```

## 学習第二段階
### 学習用の設定ファイル`config2.json`を作る
`sample_config2.json`の`input_glob`、`target_glob`、`indexes_glob`を変更すればとりあえず動きます。
本家のconfig.jsonの`train_crop_size`の値は512ですが、うちの環境（GTX1060 メモリ6GB）では動かなかったので128に下げています。

### 学習する

```bashss
python train_2nd.py \
    sample_config2.json \
    ./model_stage2/
```

## License
[MIT License](./LICENSE)
