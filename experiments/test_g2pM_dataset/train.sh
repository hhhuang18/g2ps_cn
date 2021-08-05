order="2"

mkdir model

cp ../../data/data_train/lexicon.txt ./model/
cp ../../data/data_train/aligned.corpus ./model/
cp ../../data/data_train/aligned_inv.corpus ./model/

echo "ngram order:"$order

estimate-ngram -o $order -t ./model/aligned.corpus -wl ./model/model.arpa
phonetisaurus-arpa2wfst --lm=./model/model.arpa --ofile=./model/model.fst

estimate-ngram -o $order -t ./model/aligned_inv.corpus -wl ./model/model_inv.arpa
phonetisaurus-arpa2wfst --lm=./model/model_inv.arpa --ofile=./model/model_inv.fst