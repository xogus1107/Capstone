import tensorflow as tf
from FaceAging import FaceAging
from os import environ
import argparse

environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(description='CAAE')
parser.add_argument('--is_train', type=str2bool, default=False)
parser.add_argument('--dataset', type=str, default='faces', help='training dataset name that stored in ./data')
parser.add_argument('--savedir', type=str, default='save\\faces', help='dir of saving checkpoints and intermediate training results')
parser.add_argument('--testdir', type=str, default='test', help='dir of testing images')
parser.add_argument('--age', type=int, default='0', help='age of test image results')
parser.add_argument('--gender', type=int, default='0', help='gender(man is 0, woman is 1) of test image results')

FLAGS = parser.parse_args()


def main(_):

    # print settings
    import pprint
    pprint.pprint(FLAGS)

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    with tf.Session(config=config) as session:
        model = FaceAging(
            session,  # TensorFlow session
            is_training=FLAGS.is_train,  # flag for training or testing mode
            save_dir=FLAGS.savedir,  # path to save checkpoints, samples, and summary
            dataset_name=FLAGS.dataset  # name of the dataset in the folder ./data
        )
        print('\n\tTesting Mode')
        model.custom_test(
            testing_samples_dir=FLAGS.testdir + '/*jpg',
            age = FLAGS.age,
            gender = FLAGS.gender
        )


if __name__ == '__main__':
    # with tf.device('/cpu:0'):
    tf.app.run()
