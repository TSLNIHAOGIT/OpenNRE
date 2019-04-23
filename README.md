# OpenNRE
###换数据时要删除_processed_data文件夹，让其重新生成


An open-source framework for neural relation extraction.

Contributed by [Tianyu Gao](https://github.com/gaotianyu1350), [Xu Han](https://github.com/THUCSTHanxu13), [Shulian Cao](https://github.com/ShulinCao), [Lumin Tang](https://github.com/Tsingularity), [Yankai Lin](https://github.com/Mrlyk423), [Zhiyuan Liu](http://nlp.csai.tsinghua.edu.cn/~lzy/)

If you want to learn more about neural relation extraction, visit another project of ours [NREPapers](https://github.com/thunlp/NREPapers).

**BIG UPDATE**: The project has been completely reconstructed and is faster, more extendable and the codes are easier to read and use now. If you need get to the old version, please refer to branch [old_version](https://github.com/thunlp/OpenNRE/tree/old_version).  

New features:

- JSON data support.
- Multi GPU training.
- Validating while training.

## Overview

It is a TensorFlow-based framwork for easily building relation extraction (RE) models. We divide the pipeline of relation extraction into four parts, which are embedding, encoder, selector (for distant supervision) and classifier. For each part we have implemented several methods.

* Embedding
  * Word embedding
  * Position embedding
* Encoder
  * PCNN
  * CNN
  * RNN
  * Bidirection RNN
* Selector
  * Attention
  * Maximum
  * Average
* Classifier
  * Softmax Loss Function
  * Output
  
All those methods could be combined freely. 

We also provide training and testing framework for sentence-level RE and bag-level RE. A plotting tool is also in the package.

This project is under MIT license.

## Requirements

- Python (>=2.7)
- Numpy (>=1.13.3)
- TensorFlow (>=1.4.1)
    - CUDA (>=8.0) if you are using gpu
- Matplotlib (>=2.0.0)
- scikit-learn (>=0.18)

## Data Format

For training and testing, you should provide four `JSON` files including training data, testing data, word embedding data and relation-ID mapping data. 

### Training Data & Testing Data

Training data file and testing data file, containing sentences and their corresponding entity pairs and relations, should be in the following format

```
[
    {
        'sentence': 'Bill Gates is the founder of Microsoft .',
        'head': {'word': 'Bill Gates', 'id': 'm.03_3d', ...(other information)},
        'tail': {'word': 'Microsoft', 'id': 'm.07dfk', ...(other information)},
        'relation': 'founder'
    },
    ...
]
```

**IMPORTANT**: In the sentence part, words and punctuations should be separated by blank spaces.

### Word Embedding Data

Word embedding data is used to initialize word embedding in the networks, and should be in the following format

```
[
    {'word': 'the', 'vec': [0.418, 0.24968, ...]},
    {'word': ',', 'vec': [0.013441, 0.23682, ...]},
    ...
]
```

### Relation-ID Mapping Data

This file indicates corresponding IDs for relations to make sure during each training and testing period, the same ID means the same relation. Its format is as follows

```
{
    'NA': 0,
    'relation_1': 1,
    'relation_2': 2,
    ...
}
```

**IMPORTANT**: Make sure the ID of `NA` is always 0.

## Provided Data

### NYT10 Dataset

NYT10 is a distantly supervised dataset originally released by the paper "Sebastian Riedel, Limin Yao, and Andrew McCallum. Modeling relations and their mentions without labeled text.". Here is the download [link](http://iesl.cs.umass.edu/riedel/ecml/) for the original data.

We've provided a toolkit to convert the original NYT10 data into JSON format that `OpenNRE` could use. You could download the original data + toolkit from [Google Drive](https://drive.google.com/file/d/1eSGYObt-SRLccvYCsWaHx1ldurp9eDN_/view?usp=sharing) or [Tsinghua Cloud](https://cloud.tsinghua.edu.cn/f/11391e48b72749d8b60a/?dl=1). Further instructions are included in the toolkit.

## Installation and Quick Start

1. **Install all the required package.**

2. **Clone the OpenNRE repository:**

```bash
git clone https://github.com/thunlp/OpenNRE.git
```

Since there are too many history commits of this project and the `.git` folder is too large, you could use the following command to download only the latest commit:

```bash
git clone https://github.com/thunlp/OpenNRE.git --depth 1
```

3. **Make data folder in the following structure**

```
OpenNRE
|-- ... 
|-- data
    |
    |-- {DATASET_NAME_1}
    |   |
    |   |-- train.json
    |   |-- test.json
    |   |-- word_vec.json
    |   |-- rel2id.json
    |
    |-- {DATASET_NAME_2}
    |   |
    |   |-- ...
    |
    |-- ...
```

You could use your own data or download datasets provided above.

4. **Run `train_demo.py {DATASET_NAME} {ENCODER_NAME} {SELECTOR_NAME}`. For example, if you want to train model with PCNN as the encoder and attention as the selector on the `nyt` dataset, run the following command**

```
python train_demo.py nyt pcnn att
```

Currently `{ENCODER_NAME}` includes `pcnn`, `cnn`, `rnn` and `birnn`, and `{SELECTOR_NAME}` includes `att` (for attention), `max` (for maximum) and `ave` (for average). The model will be named as `{DATASET_NAME}_{ENCODER_NAME}_{SELECTOR_NAME}` automatically.

The checkpoint of the best epoch (each epoch will be validated while training) will be saved in `./checkpoint` and results for plotting precision-recall curve will be saved in `./test_result` by default.

5. **Use `draw_plot.py` to check auc, average precision, F1 score and precision-recall curve by the following command**

```
python draw_plot.py {MODEL_NAME_1} {MODEL_NAME_2} ...
```

All the results of the models mentioned will be printed and precision-recall curves containing all the models will be saved in `./test_result/pr_curve.png`.

6. **If you have the checkpoint of the model and want to evaluate it, run `test_demo.py {DATASET_NAME} {ENCODER_NAME} {SELECTOR_NAME}`. For example:**

```
python test_demo.py nyt pcnn att
```

The prediction results will be stored in `test_result/nyt_pcnn_att_pred.json`.

## Additional Modules

### Reinforcement Learning (Feng et al. 2018)

We have implemented a reinforcement learning module following [(Feng et al. 2018)](https://tianjun.me/static/essay_resources/RelationExtraction/Paper/AAAI2018Denoising.pdf). There might be some slight differences in implementation details. The RL code is in `nrekit/rl.py`, and it can be added to any models by running:

```
python train_demo.py {DATASET_NAME} {ENCODER_NAME} {SELECTOR_NAME} rl
```

For example, by running `python train_demo.py nyt pcnn att rl`, you will get a `pcnn_att` model trained by RL.

For how the RL module helps alleviate false positive problem in DS data, please refer to the paper.

## Test Results

### NYT10 Dataset

AUC Results:

Model |  Attention | Maximum | Average
---- | ---- | ---- | ----
PCNN | 0.3408 | 0.3247 | 0.3190
CNN | 0.3277 | 0.3151 | 0.3044
RNN | 0.3418 | 0.3473 | 0.3405
BiRNN | 0.3352 | 0.3575 | 0.3244

## Reference

1. **Neural Relation Extraction with Selective Attention over Instances.** _Yankai Lin, Shiqi Shen, Zhiyuan Liu, Huanbo Luan, Maosong Sun._ ACL2016. [paper](http://www.aclweb.org/anthology/P16-1200)

2. **Adversarial Training for Relation Extraction.** _Yi Wu, David Bamman, Stuart Russell._ EMNLP2017. [paper](http://www.aclweb.org/anthology/D17-1187)

3. **A Soft-label Method for Noise-tolerant Distantly Supervised Relation Extraction.** _Tianyu Liu, Kexiang Wang, Baobao Chang, Zhifang Sui._ EMNLP2017. [paper](http://aclweb.org/anthology/D17-1189)

4. **Reinforcement Learning for Relation Classification from Noisy Data.** _Jun Feng, Minlie Huang, Li Zhao, Yang Yang, Xiaoyan Zhu._ AAAI2018. [paper](https://tianjun.me/static/essay_resources/RelationExtraction/Paper/AAAI2018Denoising.pdf)


'''
Instructions for updating:
Use standard file APIs to check for files with this prefix.
Pre-processed files exist. Loading them...
Finish loading
Total relation fact: 18409
Loading data file...
Finish loading
Loading word vector file...
Finish loading
Elimiating case sensitive problem...
Finish eliminating
Sort data...
Finish sorting
Got 114042 words of 50 dims
Building word vector matrix and mapping...
Finish building
Pre-processing data...
Finish pre-processing
Storing processed files...
Finish storing
Total relation fact: 1950
Testing...

#batchsize*class_kinds
iter_logit: (160, 53) [[9.0779334e-01 1.6628122e-03 1.2030023e-04 ... 2.0159893e-04
  1.6725782e-04 1.6264951e-04]
 [9.9153829e-01 3.7023046e-06 9.5945807e-06 ... 5.2198768e-03
  2.6372858e-05 2.1413434e-05]
 [9.9757618e-01 1.8322527e-04 3.9660349e-06 ... 1.2158742e-04
  8.0468108e-06 5.7619400e-06]
 ...
 [9.9917668e-01 1.0851457e-03 6.2309664e-05 ... 1.4919280e-04
  9.5790900e-05 1.2651835e-04]
 [9.9323612e-01 3.4092576e-05 2.1421401e-05 ... 1.0617092e-03
  4.2834243e-05 3.4047935e-05]
 [9.9806029e-01 3.3380649e-05 5.9000363e-06 ... 3.2917477e-04
  1.6308306e-05 1.3128209e-05]]
iter_logit: (160, 53) [[9.9774277e-01 1.2343051e-05 3.1490706e-06 ... 9.2573377e-04
  8.4147978e-06 6.3368957e-06]
 [8.9574289e-01 8.1437256e-04 1.5107193e-04 ... 3.8297111e-04
  3.9203881e-04 3.4698809e-04]
 [8.9923507e-01 3.5057162e-04 8.5299340e-05 ... 1.9872100e-03
  2.5783756e-04 1.7273077e-04]
 ...
 [8.5899496e-01 6.8872952e-04 2.1800832e-04 ... 5.2485424e-03
  4.8583225e-04 4.6430866e-04]
 [8.4655333e-01 5.6890049e-04 2.4550041e-04 ... 8.1427917e-03
  4.6162555e-04 3.6644642e-04]
 [9.8957574e-01 1.2618395e-04 6.2178005e-06 ... 4.9556911e-05
  1.7204202e-05 1.6398431e-05]]
iter_logit: (160, 53) [[9.8708576e-01 1.9620518e-05 4.6919167e-06 ... 2.2162161e-04
  1.2545245e-05 1.0078302e-05]
 [9.5025706e-01 2.1797947e-03 2.0507569e-04 ... 2.0510796e-03
  4.4260963e-04 3.8505159e-04]
 [4.9496129e-01 1.5855308e-03 6.7565103e-05 ... 1.0237494e-03
  1.0287181e-04 1.0115405e-04]
 ...
 [9.9981993e-01 2.6627047e-06 3.3836645e-07 ... 6.2830579e-05
  1.0753714e-06 7.0400000e-07]
 [9.9923122e-01 2.5917907e-06 8.8934070e-07 ... 3.5228793e-04
  3.1680238e-06 2.3502107e-06]
 [5.5149019e-01 1.4614163e-03 6.0377180e-05 ... 9.4606623e-04
  1.3816138e-04 1.1093271e-04]]


'''