import os
import json
import argparse
import numpy as np
import subprocess
import time
import tensorflow as tf
import latticex.rosetta as rtt
from sklearn.metrics import roc_auc_score

np.set_printoptions(suppress=True)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class LogisticRegression:
    def __init__(self, protocol_config, in_dim, out_dim, learning_rate=0.1, random_seeds=1145141919810):
        self.in_dim = in_dim
        self.out_dim = out_dim

        # Activate rtt protocol
        rtt.activate("SecureNN", protocol_config_str=json.dumps(
            protocol_config, indent=4))

        # Build tensorflow graph
        self.inputX = tf.placeholder(tf.float64, [None, in_dim])
        self.inputY = tf.placeholder(tf.float64, [None, out_dim])

        # initialize W & b
        self.W = tf.Variable(tf.random_normal(
            [in_dim, out_dim], 0, 1 / (self.in_dim**0.5), dtype=tf.float64))
        self.b = tf.Variable(tf.zeros([out_dim], dtype=tf.float64))

        # Forward
        self.logits = tf.matmul(self.inputX, self.W) + self.b
        self.pred_y = tf.sigmoid(self.logits)
        self.loss = tf.nn.sigmoid_cross_entropy_with_logits(
            labels=self.inputY, logits=self.logits)

        self.train_step = tf.train.GradientDescentOptimizer(
            learning_rate).minimize(self.loss)

        self.dataX = None
        self.dataY = None

        self.prng = np.random.default_rng(random_seeds)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        self.session.run([self.W, self.b])

    def set_dataset(self, data_xs: dict, data_y: dict, split: int):
        party_id = rtt.py_protocol_handler.get_party_id()

        feature_owners = list(data_xs.keys())
        label_owner = list(data_y.keys())[0]

        self.dataX, self.dataY = rtt.PrivateDataset(data_owner=feature_owners, label_owner=label_owner).\
            load_data(data_xs.get(party_id), data_y.get(party_id))

        self.data_split = split

        assert self.dataX.shape[1] == self.in_dim and self.dataY.shape[1] == self.out_dim, \
            "Data/label dim must be the same as in/out dim"

    def train_one_batch(self, batch_size=32):
        batch_indices = self.prng.choice(self.data_split, batch_size)

        batch_x = self.dataX[batch_indices]
        batch_y = self.dataY[batch_indices]

        loss = self.session.run(self.train_step, feed_dict={
                                self.inputX: batch_x, self.inputY: batch_y})

        return loss

    def test_one_batch(self, batch_size=None):
        if not batch_size:
            batch_indices = np.arange(self.data_split, self.dataX.shape[0])
        else:
            batch_indices = self.prng.choice(
                np.arange(self.data_split, self.dataX.shape[0]), batch_size)

        batch_x = self.dataX[batch_indices]
        batch_y = self.dataY[batch_indices]

        predY = self.session.run(rtt.SecureReveal(self.pred_y, 0b001), feed_dict={
                                 self.inputX: batch_x}).astype(np.float)
        trueY = self.session.run(rtt.SecureReveal(
            batch_y, 0b001)).astype(np.float)

        return predY, trueY


def generate_config(rtt_args):
    party_id = rtt_args['party_id']
    exec_endpoints = rtt_args['exec_endpoints']

    host0, port0 = exec_endpoints['0'].split(":")
    host1, port1 = exec_endpoints['1'].split(":")
    host2, port2 = exec_endpoints['2'].split(":")

    cert_path = f"./certs_{party_id}"
    server_cert_path = f"{cert_path}/server-nopass.cert"
    server_prikey_path = f"{cert_path}/server-prikey"

    # P0, P1, P2 need generate their separate ssl server certificate and private key respectively:
    # Note: in production environment,lbe certain to use real trusted third-party certificates.
    subprocess.Popen(f"mkdir {cert_path}", stdout=subprocess.PIPE, shell=True)
    time.sleep(2)
    subprocess.Popen(f"openssl genrsa -out {server_prikey_path} 4096",
                     stdout=subprocess.PIPE, shell=True)
    time.sleep(2)
    subprocess.Popen("if [ ! -f '${HOME}/.rnd' ]; then openssl rand -writerand ${HOME}/.rnd; fi",
                     stdout=subprocess.PIPE, shell=True)
    time.sleep(2)
    subprocess.Popen(f"openssl req -new -subj '/C=BY/ST=Belarus/L=Minsk/O=Rosetta SSL IO server/OU=Rosetta server unit/CN=server' -key {server_prikey_path} -out {cert_path}/cert.req",
                     stdout=subprocess.PIPE, shell=True)
    time.sleep(2)
    subprocess.Popen(f"openssl x509 -req -days 365 -in {cert_path}/cert.req -signkey {server_prikey_path} -out {server_cert_path}",
                     stdout=subprocess.PIPE, shell=True)
    time.sleep(2)

    config_template = {
        "PARTY_ID": party_id,
        "MPC": {
            "FLOAT_PRECISION": 16,
            "P0": {
                "NAME": "PartyA(P0)",
                "HOST": host0,
                "PORT": int(port0)
            },
            "P1": {
                "NAME": "PartyB(P1)",
                "HOST": host1,
                "PORT": int(port1)
            },
            "P2": {
                "NAME": "PartyC(P2)",
                "HOST": host2,
                "PORT": int(port2)
            },
            "SAVER_MODE": 7,
            "SERVER_CERT": server_cert_path,
            "SERVER_PRIKEY": server_prikey_path,
            "SERVER_PRIKEY_PASSWORD": "123456"
        }
    }

    return config_template


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)

    args = parser.parse_args()
    rtt_args = json.load(open(args.config))
    protocol_config = generate_config(rtt_args)

    model_args = rtt_args['model_args']
    inputs = rtt_args['inputs']
    outputs = rtt_args['outputs']

    in_dim = model_args['in_dim']
    out_dim = model_args['out_dim']
    lr = model_args['lr']
    batch_size = model_args['batch_size']
    split = model_args['split']
    epoch = model_args['epoch']

    # party 0, 1 have the feature file, party 2 have the label file
    feature_files = {
        0: inputs['0'],
        1: inputs['1'],
    }
    label_files = {
        2: inputs['2']
    }

    output_party, output_path = None, None
    for k, v in outputs.items():
        output_party = int(k)
        output_path = v

    logistic = LogisticRegression(
        protocol_config, in_dim, out_dim, learning_rate=lr)

    logistic.set_dataset(feature_files, label_files, split=split)

    party = rtt.py_protocol_handler.get_party_id()

    for i in range(epoch):
        logistic.train_one_batch(batch_size=batch_size)

        if i % 100 == 0:
            if party == output_party:
                pred_y, true_y = logistic.test_one_batch()
                auc = roc_auc_score(true_y, pred_y)
                with open(output_path, 'a') as f:
                    f.write("AUC at round %d: %.4f\n" % (i, auc))
            else:
                logistic.test_one_batch()
