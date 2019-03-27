import nrekit
import numpy as np
import tensorflow as tf
import sys
import os

dataset_name = 'wiki18'
if len(sys.argv) > 1:
    dataset_name = sys.argv[1]
dataset_dir = os.path.join('./data', dataset_name)
if not os.path.isdir(dataset_dir):
    raise Exception("[ERROR] Dataset dir %s doesn't exist!" % (dataset_dir))

# The first 3 parameters are train / test data file name, word embedding file name and relation-id mapping file name respectively.
train_loader = nrekit.data_loader.json_file_data_loader(os.path.join(dataset_dir, 'train.json'), 
                                                        os.path.join(dataset_dir, 'word_vec.json'),
                                                        os.path.join(dataset_dir, 'rel2id.json'), 
                                                        mode=nrekit.data_loader.json_file_data_loader.MODE_RELFACT_BAG,
                                                        dataset_name=dataset_name,
                                                        shuffle=True)

val_loader = nrekit.data_loader.json_file_data_loader(os.path.join(dataset_dir, 'test.json'), 
                                                       os.path.join(dataset_dir, 'word_vec.json'),
                                                       os.path.join(dataset_dir, 'rel2id.json'), 
                                                       mode=nrekit.data_loader.json_file_data_loader.MODE_ENTPAIR_BAG,
                                                       dataset_name=dataset_name,
                                                       shuffle=False)

test_loader = nrekit.data_loader.json_file_data_loader(os.path.join(dataset_dir, 'test.json'), 
                                                       os.path.join(dataset_dir, 'word_vec.json'),
                                                       os.path.join(dataset_dir, 'rel2id.json'), 
                                                       mode=nrekit.data_loader.json_file_data_loader.MODE_ENTPAIR_BAG,
                                                       dataset_name=dataset_name,
                                                       shuffle=False)

framework = nrekit.framework.re_framework(train_loader, val_loader, test_loader)

class model(nrekit.framework.re_model):
    encoder = "pcnn"
    selector = "att"
    adv = False

    def get_model(self, x):
        with tf.variable_scope(encoder + '_' + selector, reuse=tf.AUTO_REUSE):
            # Encoder
            if model.encoder == "pcnn":
                x_train = nrekit.network.encoder.pcnn(x, self.mask, keep_prob=0.5)
                x_test = nrekit.network.encoder.pcnn(x, self.mask, keep_prob=1.0)
            elif model.encoder == "cnn":
                x_train = nrekit.network.encoder.cnn(x, keep_prob=0.5)
                x_test = nrekit.network.encoder.cnn(x, keep_prob=1.0)
            elif model.encoder == "rnn":
                x_train = nrekit.network.encoder.rnn(x, self.length, keep_prob=0.5)
                x_test = nrekit.network.encoder.rnn(x, self.length, keep_prob=1.0)
            elif model.encoder == "birnn":
                x_train = nrekit.network.encoder.birnn(x, self.length, keep_prob=0.5)
                x_test = nrekit.network.encoder.birnn(x, self.length, keep_prob=1.0)
            else:
                raise NotImplementedError

            # Selector
            if model.selector == "att":
                self._train_logit, train_repre = nrekit.network.selector.bag_attention(x_train, self.scope, self.ins_label, self.rel_tot, True, keep_prob=0.5)
                self._test_logit, test_repre = nrekit.network.selector.bag_attention(x_test, self.scope, self.ins_label, self.rel_tot, False, keep_prob=1.0)
            elif model.selector == "ave":
                self._train_logit, train_repre = nrekit.network.selector.bag_average(x_train, self.scope, self.rel_tot, keep_prob=0.5)
                self._test_logit, test_repre = nrekit.network.selector.bag_average(x_test, self.scope, self.rel_tot, keep_prob=1.0)
                self._test_logit = tf.nn.softmax(self._test_logit)
            elif model.selector == "one":
                self._train_logit, train_repre = nrekit.network.selector.bag_one(x_train, self.scope, self.label, self.rel_tot, True, keep_prob=0.5)
                self._test_logit, test_repre = nrekit.network.selector.bag_one(x_test, self.scope, self.label, self.rel_tot, False, keep_prob=1.0)
                self._test_logit = tf.nn.softmax(self._test_logit)
            elif model.selector == "cross_max":
                self._train_logit, train_repre = nrekit.network.selector.bag_cross_max(x_train, self.scope, self.rel_tot, keep_prob=0.5)
                self._test_logit, test_repre = nrekit.network.selector.bag_cross_max(x_test, self.scope, self.rel_tot, keep_prob=1.0)
                self._test_logit = tf.nn.softmax(self._test_logit)
            else:
                raise NotImplementedError
 
    def __init__(self, train_data_loader, batch_size, max_length=120):
        nrekit.framework.re_model.__init__(self, train_data_loader, batch_size, max_length=max_length)
        self.mask = tf.placeholder(dtype=tf.int32, shape=[None, max_length], name="mask")
        
        # Embedding
        w_embedding = nrekit.embedding.word_embedding(self.word, self.word_vec_mat)
        p_embedding = nrekit.embedding.pos_embedding(self.pos1, self.pos2)
        x = tf.concat([w_embedding, p_embedding], -1)
        # x = nrekit.network.embedding.word_position_embedding(self.word, self.word_vec_mat, self.pos1, self.pos2)

        self.get_model(x)   

        # Classifier
        self._loss = nrekit.network.classifier.softmax_cross_entropy(self._train_logit, self.label, self.rel_tot, weights_table=self.get_weights())

        if model.adv:
            new_w_embedding = nrekit.network.adversarial(self._loss, w_embedding)
            new_x = tf.concat([new_w_embedding, p_embedding], -1)
            self.get_model(new_x)
            self._loss = nrekit.network.classifier.softmax_cross_entropy(self._train_logit, self.label, self.rel_tot, weights_table=self.get_weights())
 
    def loss(self):
        return self._loss

    def train_logit(self):
        return self._train_logit

    def test_logit(self):
        return self._test_logit

    def get_weights(self):
        with tf.variable_scope("weights_table", reuse=tf.AUTO_REUSE):
            print("Calculating weights_table...")
            _weights_table = np.zeros((self.rel_tot), dtype=np.float32)
            for i in range(len(self.train_data_loader.data_rel)):
                _weights_table[self.train_data_loader.data_rel[i]] += 1.0 
            _weights_table = 1 / (_weights_table ** 0.05)
            weights_table = tf.get_variable(name='weights_table', dtype=tf.float32, trainable=False, initializer=_weights_table)
            print("Finish calculating")
        return weights_table

use_rl = False
if len(sys.argv) > 2:
    model.encoder = sys.argv[2]
if len(sys.argv) > 3:
    model.selector = sys.argv[3]
if len(sys.argv) > 4:
    if sys.argv[4] == 'rl':
        use_rl = True
    if sys.argv[4] == 'adv':
        model.adv = True

if use_rl:
    model_name=dataset_name + "_" + model.encoder + "_" + model.selector + "_rl"
    rl_framework = nrekit.rl.rl_re_framework(train_loader, val_loader, test_loader)
    rl_framework.train(model, nrekit.rl.policy_agent, model_name=model_name, max_epoch=60, ckpt_dir="checkpoint")
    print("\n-------- TEST --------\n")
    test_result_dir = './test_result'
    rl_framework.test(model, ckpt="checkpoint/" + model_name)
    if not os.path.isdir(test_result_dir):
        os.mkdir(test_result_dir)
    np.save(os.path.join(test_result_dir, model_name + "_x.npy"), best_recall)
    np.save(os.path.join(test_result_dir, model_name + "_y.npy"), best_prec)

else:
    model_name = dataset_name + "_" + model.encoder + "_" + model.selector
    framework.train(model, model_name=model_name, max_epoch=60, ckpt_dir="checkpoint", gpu_nums=1)
    print("\n-------- TEST --------\n")
    test_result_dir = './test_result'
    framework.test(model, ckpt="checkpoint/" + model_name)
    if not os.path.isdir(test_result_dir):
        os.mkdir(test_result_dir)
    np.save(os.path.join(test_result_dir, model_name + "_x.npy"), framework.cur_recall)
    np.save(os.path.join(test_result_dir, model_name + "_y.npy"), framework.cur_prec)
