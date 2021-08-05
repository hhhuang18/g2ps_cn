### G2P Tool for Chinese Sentences

**To run the demos, you would need**

- python3

**Run the demos**

```shell
# Have a look at the contents
ls
# README.md  data  experiments  models  phonetisaurus  setup.sh

# Initialize
source setup.sh

# Quick test with the pretrained model for English sentence
phonetisaurus-g2pfst --model=./models/model.fst --nbest=1 --word="中文句子转拼音"
# 中文句子转拼音  48.7726 zhong1 wen2 ju4 zi3 zhuan3 pin1 yin1

# Show G-P pairs
phonetisaurus-g2pfst --model=./models/model.fst --nbest=1 --word="中文句子转拼音" --print_pairs=true
# 中文句子转拼音  48.7726 {中:zhong1} {文:wen2} {句:ju4} {子:zi3} {转:zhuan3} {拼:pin1} {音:yin1}
```

1. **Evaluate the model based on g2pM dataset and statistical method** https://github.com/kakaobrain/g2pM

```shell
cd experiments/test_g2pM_dataset/

./train.sh
# please wait a while...
# default: 2-gram

./test.sh
# ------------------
# dataset: g2pM-test
# polyphone_accuracy %:
# forward      : 97.81548663936024
# backward     : 97.82523893114882
# bi_direction : 97.80573434757169

# ------------------
# dataset: g2pM-dev
# polyphone_accuracy %:
# forward      : 97.73577276862429
# backward     : 97.7054482967755
# bi_direction : 97.72566461134136
```

The detailed results are shown as below: 

|  Order  |  Direction   |   Dev.    |   Test    |
| :-----: | :----------: | :-------: | :-------: |
| order 2 |   forward    | **97.74** |   97.82   |
| order 2 |   backward   |   97.71   | **97.83** |
| order 2 | bi_direction |   97.73   |   97.81   |
| order 3 |   forward    |   97.67   |   97.75   |
| order 3 |   backward   |   97.63   |   97.74   |
| order 3 | bi_direction |   97.65   |   97.75   |
| order 6 |   forward    |   97.65   |   97.74   |
| order 6 |   backward   |   97.61   |   97.77   |
| order 6 | bi_direction |   97.69   |   97.75   |

Reference results:

| Model            | Dev            | Test         |
| :-------------:| :-------------: |:--------------:|
| g2pC                 | 84.84                | 84.45           |
| xpinyin(0.5.6)       | 78.74                | 78.56           |
| pypinyin(0.36.0)     | 85.44                | 86.13           |
| Majority Vote        | 92.15                | 92.08           |
| Chinese Bert         | **97.95**            | **97.85**       |
| g2pM             | 97.36                | 97.31           |

2. **Inference using our own word list**

```shell
cd experiments/test_our_data_example/
# the pretrained model is the 2-gram forward model trained with g2pM training set

./test.sh
# 我们在小米科技园			wo3 men5 zai4 xiao3 mi3 ke1 ji4 yuan2
# 有行政部门和银行			you3 xing2 zheng4 bu4 men2 he2 yin2 hang2
# 这是一首快乐的音乐		   zhe4 shi4 yi1 shou3 kuai4 le4 de5 yin1 yue4
# 他差不多要去出差了        ta1 cha4 bu4 duo1 yao4 qu4 chu1 chai1 le5
# 他穿着干净的衣服在干活     ta1 chuan1 zhe5 gan1 jing4 de5 yi1 fu2 zai4 gan4 huo2
# 大都市的人都很多          da4 du1 shi4 de5 ren2 dou1 hen3 duo1
```

3. **Train model using customized dataset**

The training dataset is based on the data from g2pM by data/make_trainset.py. (g2pM is required for this script)

Your can use your own data to train the model, just by making a corpus file:

- it is a pure text file

- each line is one sample
- each line is formatted as G-P pairs: 字}zi4 或}huo4 者}zhe3 句}ju:4 子}zi3
- there is an En blank space between two G-P pairs
- please view the data/data_train/aligned.corpus for more datails

Then train your own FST model similar to experiments/test_g2pM_dataset/train.sh



**If you would like to compile phonetisaurus, you would need** 

- openfst >= 1.6.0
- mitlm 

For more details about phonetisaurus, please refer to:

https://github.com/AdolfVonKleist/Phonetisaurus