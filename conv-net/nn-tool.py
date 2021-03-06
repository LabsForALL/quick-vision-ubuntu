import os
import tensorflow as tf
from model import ConvNet
from utils import pp

flags = tf.app.flags

flags.DEFINE_integer("epoch", 5, "Epoch to train [5]")
flags.DEFINE_float("learning_rate", 0.0002, "Learning rate of for adam [0.0002]")
flags.DEFINE_float("beta1", 0.5, "Momentum term of adam [0.5]")

flags.DEFINE_integer("input_size", 64, "The size of the input images [64]")
flags.DEFINE_integer("target_size", 256, "The size of image to use (will be center cropped) [256]")

flags.DEFINE_string("dataset", "outlook", "The name of the dataset [outlook]")
flags.DEFINE_string("checkpoint_dir", "checkpoint", "Directory name to save the checkpoints [checkpoint]")
flags.DEFINE_string("sample_dir", "samples", "Directory name to save the image samples [samples]")

flags.DEFINE_boolean("is_train", False, "True for training, False for testing [False]")
flags.DEFINE_boolean("is_crop", True, "[True]")
FLAGS = flags.FLAGS


def main(_):

    pp.pprint(flags.FLAGS.__flags)

    if not os.path.exists(FLAGS.checkpoint_dir):
        os.makedirs(FLAGS.checkpoint_dir)
    if not os.path.exists(FLAGS.sample_dir):
        os.makedirs(FLAGS.sample_dir)

    with tf.Session() as sess:

        conv_net = ConvNet(sess,
                           FLAGS.input_size,
                           FLAGS.target_size,
                           FLAGS.dataset,
                           FLAGS.checkpoint_dir)

        if FLAGS.is_train:
            conv_net.train(FLAGS.learning_rate,
                           FLAGS.beta1,
                           FLAGS.epoch,
                           FLAGS.dataset,
                           FLAGS.checkpoint_dir,
                           FLAGS.is_crop)
        else:
            conv_net.run_test(FLAGS.checkpoint_dir, FLAGS.dataset, FLAGS.is_crop)


if __name__ == '__main__':
    tf.app.run()
