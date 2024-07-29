import numpy;
#import tf_agents;
#from tf_agents.networks import sequential
import tensorflow as tf
import keras
from keras import layers


def dense_layer(num_units):
  return tf.keras.layers.Dense(
      num_units,
      activation=tf.keras.activations.relu,
      kernel_initializer=tf.keras.initializers.VarianceScaling(
          scale=2.0, mode='fan_in', distribution='truncated_normal'))

#wrapper to handle constructing network
class QNetwork:
    q_net : keras.Sequential = None;
    def __init__(self,inputHeight : int, hiddenLayers : list[int], outputLayer:int):
        inputLayer = tf.keras.layers.Dense(hiddenLayers[0],activation=tf.keras.activations.relu,kernel_initializer=tf.keras.initializers.VarianceScaling(scale=2.0, mode='fan_in', distribution='truncated_normal')
        ,input_shape=(inputHeight,))
        dense_layers = [dense_layer(num_units) for num_units in  hiddenLayers[1:]]
        q_values_layer = tf.keras.layers.Dense(outputLayer,activation=None,kernel_initializer=tf.keras.initializers.RandomUniform(minval=-0.03, maxval=0.03),bias_initializer=tf.keras.initializers.Constant(-0.2))
        self.q_net = keras.Sequential([inputLayer] + dense_layers + [q_values_layer])


    def calc(self, inputs : list[int]) -> tf.Tensor:
        output = self.q_net(tf.reshape(tf.convert_to_tensor(inputs, dtype=tf.float32),shape=(1,len(inputs))));
        return output;