import tensorflow as tf
print(tf.__version__)

# 设置设备类型
device = 'cpu' # 在Mac设备中，tensorflow暂时不支持mps加速


# 张量测试
def test_tensor():
    # 张量
    x = tf.constant([[1, 2], [3, 4]], dtype=tf.float32)
    y = tf.constant([[5, 6], [7, 8]], dtype=tf.float32)
    z = tf.matmul(x, y) # 矩阵乘法
    print(z.shape)

    # 自动微分（auto-grade)
    x = tf.Variable(3.0)
    with tf.GradientTape() as tape:
        y = x ** 2
    dy_dx = tape.gradient(y, x)

    # keras-api
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(3, activation=tf.nn.relu, input_shape=(784,)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation=tf.nn.softmax),
    ])
    print(model.summary())


# 模型测试
def test_minist():
    # 加载数据
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train = x_train.reshape(-1, 28*28).astype('float32')/255.0
    x_test = x_test.reshape(-1, 28*28).astype('float32')/255.0

    # 构建模型
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation = tf.nn.relu),
        tf.keras.layers.Dense(10, activation = tf.nn.softmax)
    ])

    # 编译模型
    model.compile(optimizer = 'adam',
                  loss = 'sparse_categorical_crossentropy',
                  metrics = ['accuracy'])

    # 训练
    model.fit(x_train, y_train, epochs = 5, batch_size = 32)

    # 评估
    acc = model.evaluate(x_test, y_test)
    print(acc)


# 调度主函数
if __name__ == '__main__':
    print(tf.__version__)

    test_tensor() # 测试张量操作

    test_minist() # 测试minist模型