import sys,os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'../..')))

import nrekit
import numpy as np
import tensorflow as tf
import sys
import os
import json

dataset_name = 'nyt'
# if len(sys.argv) > 1:
#     dataset_name = sys.argv[1]
# dataset_dir = os.path.join('./data', dataset_name)

dataset_dir='./data'
# if not os.path.isdir(dataset_dir):
#     raise Exception("[ERROR] Dataset dir %s doesn't exist!" % (dataset_dir))

# The first 3 parameters are train / test data file name, word embedding file name and relation-id mapping file name respectively.
train_loader = nrekit.data_loader.json_file_data_loader(os.path.join(dataset_dir, 'train_people.json'),
                                                        os.path.join(dataset_dir, 'word_vec_people.json'),
                                                        os.path.join(dataset_dir, 'rel2id_people.json'),
                                                        mode=nrekit.data_loader.json_file_data_loader.MODE_RELFACT_BAG,
                                                        shuffle=False)
test_loader = nrekit.data_loader.json_file_data_loader(os.path.join(dataset_dir,
                                                                    # 'label_test_relation_new.json',
                                                                    # 'test-reading-friendly.json',
                                                                    # 'dev_people.json',
                                                                    'label_test_relation_split.json',
                                                                    # 'train_people.json'

                                                                    ),
                                                       os.path.join(dataset_dir, 'word_vec_people.json'),
                                                       os.path.join(dataset_dir, 'rel2id_people.json'),
                                                       mode=nrekit.data_loader.json_file_data_loader.MODE_ENTPAIR_BAG,
                                                       shuffle=False)

print('test_loader',type(test_loader),test_loader)
for i, batch_data in enumerate(test_loader):
    print(i,batch_data)
    if i>3:
        break
framework = nrekit.framework.re_framework(train_loader, test_loader)


# class MyEncoder(json.JSONEncoder):
#
#     def default(self, obj):
#         """
#         只要检查到了是bytes类型的数据就把它转为str类型
#         :param obj:
#         :return:
#         """
#         if isinstance(obj, bytes):
#             return str(obj, encoding='utf-8')
#         return json.JSONEncoder.default(self, obj)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        else:
            return json.JSONEncoder.default(self, obj)
            # return super(MyEncoder, self).default(obj)

class model(nrekit.framework.re_model):
    encoder = "pcnn"
    selector = "att"

    def __init__(self, train_data_loader, batch_size, max_length=120):
        nrekit.framework.re_model.__init__(self, train_data_loader, batch_size, max_length=max_length)
        self.mask = tf.placeholder(dtype=tf.int32, shape=[None, max_length], name="mask")
        
        # Embedding
        x = nrekit.network.embedding.word_position_embedding(self.word, self.word_vec_mat, self.pos1, self.pos2)

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
        elif model.selector == "max":
            self._train_logit, train_repre = nrekit.network.selector.bag_maximum(x_train, self.scope, self.ins_label, self.rel_tot, True, keep_prob=0.5)
            self._test_logit, test_repre = nrekit.network.selector.bag_maximum(x_test, self.scope, self.ins_label, self.rel_tot, False, keep_prob=1.0)
            self._test_logit = tf.nn.softmax(self._test_logit)
        else:
            raise NotImplementedError
        
        # Classifier
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

# if len(sys.argv) > 2:
#     model.encoder = sys.argv[2]
# if len(sys.argv) > 3:
#     model.selector = sys.argv[3]

model.encoder='pcnn'
model.selector='att'
'''is not a valid checkpoint: ./checkpoint/nyt_pcnn_att'''
checkpoint_path=  tf.train.latest_checkpoint('./checkpoint/')

if __name__=='__main__':
    #注意要把_processed_data文件删除，让其重新生成
    #因为里面既包含tran的文件也包含test的文件

    # auc, pred_result = framework.test(model, ckpt="./checkpoint/" + dataset_name + "_" + model.encoder + "_" + model.selector, return_result=True)
    # auc, pred_result = framework.test(model, ckpt=checkpoint_path
    #                               , return_result=True)
    # print('auc',auc)

    pred_result=framework.predict(model, ckpt=checkpoint_path
                                  , return_result=True)
    # print('pred_result:')
    # for i in range(100):
    #     print(pred_result[i])


    #先不保存结果看一下
    print("start save predict results")
    #open要加上encoding=utf8，否则后面的dump会报错
    with open('./test_result/' + dataset_name + "_" + model.encoder + "_" + model.selector + "_pred.json", 'w',encoding='utf8') as outfile:
        json.dump(pred_result, outfile,cls=MyEncoder,ensure_ascii=False,indent=4)

