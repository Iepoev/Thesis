import keras

class FitzHughNagumo(keras.layers.Layer):
    def __init__(self, initializer="he_normal", **kwargs):
        super(FitzHughNagumo, self).__init__()
        v_init = tf.random_normal_initializer()
        self.v = tf.Variable(
            initial_value=v_init(shape=(input_dim, units), dtype="float32"),
            trainable=True,
        )

        p1_init = tf.zeros_initializer()
        self.p1 = tf.Variable(
            initial_value=p1_init(shape=(units,), dtype="float32"), trainable=True
        )

        p2_init = tf.zeros_initializer()
        self.p2 = tf.Variable(
            initial_value=p2_init(shape=(units,), dtype="float32"), trainable=True
        )
            
        p3_init = tf.zeros_initializer()
        self.p3 = tf.Variable(
            initial_value=p3_init(shape=(units,), dtype="float32"), trainable=True
        )        

        p4_init = tf.zeros_initializer()
        self.p4 = tf.Variable(
            initial_value=p4_init(shape=(units,), dtype="float32"), trainable=True
        )


    def call(self, inputs):
        return tf.matmul(inputs, self.w) + self.b


        v - v^3/3 - p1 * w * v + inputs

        w =  p2 * (v - p3 * w)