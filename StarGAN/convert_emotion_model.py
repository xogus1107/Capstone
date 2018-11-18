import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.autograd import Variable
from data_loader import get_loader
import os
from torchvision.utils import save_image
from data_loader import get_loader
import onnx
from PIL import Image

class ResidualBlock(nn.Module):
    """Residual Block with instance normalization."""
    def __init__(self, dim_in, dim_out):
        super(ResidualBlock, self).__init__()
        self.main = nn.Sequential(
            nn.Conv2d(dim_in, dim_out, kernel_size=3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(dim_out, affine=True, track_running_stats=True),
            nn.ReLU(inplace=True),
            nn.Conv2d(dim_out, dim_out, kernel_size=3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(dim_out, affine=True, track_running_stats=True))

    def forward(self, x):
        return x + self.main(x)


class Generator(nn.Module):
    """Generator network."""
    def __init__(self, conv_dim=64, c_dim=8, repeat_num=6):
        super(Generator, self).__init__()

        layers = []
        layers.append(nn.Conv2d(3+c_dim, conv_dim, kernel_size=7, stride=1, padding=3, bias=False))
        layers.append(nn.InstanceNorm2d(conv_dim, affine=True, track_running_stats=True))
        layers.append(nn.ReLU(inplace=True))

        # Down-sampling layers.
        curr_dim = conv_dim
        for i in range(2):
            layers.append(nn.Conv2d(curr_dim, curr_dim*2, kernel_size=4, stride=2, padding=1, bias=False))
            layers.append(nn.InstanceNorm2d(curr_dim*2, affine=True, track_running_stats=True))
            layers.append(nn.ReLU(inplace=True))
            curr_dim = curr_dim * 2

        # Bottleneck layers.
        for i in range(repeat_num):
            layers.append(ResidualBlock(dim_in=curr_dim, dim_out=curr_dim))

        # Up-sampling layers.
        for i in range(2):
            layers.append(nn.ConvTranspose2d(curr_dim, curr_dim//2, kernel_size=4, stride=2, padding=1, bias=False))
            layers.append(nn.InstanceNorm2d(curr_dim//2, affine=True, track_running_stats=True))
            layers.append(nn.ReLU(inplace=True))
            curr_dim = curr_dim // 2

        layers.append(nn.Conv2d(curr_dim, 3, kernel_size=7, stride=1, padding=3, bias=False))
        layers.append(nn.Tanh())
        self.main = nn.Sequential(*layers)

    def forward(self, x):
        # Replicate spatially and concatenate domain information.
        '''
        c = c.view(c.size(0), c.size(1), 1, 1)
        c = c.repeat(1, 1, x.size(2), x.size(3))
        x = torch.cat([x, c], dim=1)
        '''
        return self.main(x)

class Discriminator(nn.Module):
    """Discriminator network with PatchGAN."""
    def __init__(self, image_size=128, conv_dim=64, c_dim=5, repeat_num=6):
        super(Discriminator, self).__init__()
        layers = []
        layers.append(nn.Conv2d(3, conv_dim, kernel_size=4, stride=2, padding=1))
        layers.append(nn.LeakyReLU(0.01))

        curr_dim = conv_dim
        for i in range(1, repeat_num):
            layers.append(nn.Conv2d(curr_dim, curr_dim*2, kernel_size=4, stride=2, padding=1))
            layers.append(nn.LeakyReLU(0.01))
            curr_dim = curr_dim * 2

        kernel_size = int(image_size / np.power(2, repeat_num))
        self.main = nn.Sequential(*layers)
        self.conv1 = nn.Conv2d(curr_dim, 1, kernel_size=3, stride=1, padding=1, bias=False)
        self.conv2 = nn.Conv2d(curr_dim, c_dim, kernel_size=kernel_size, bias=False)

    def forward(self, x):
        h = self.main(x)
        out_src = self.conv1(h)
        out_cls = self.conv2(h)
        return out_src, out_cls.view(out_cls.size(0), out_cls.size(1))

def create_labels(c_org, c_dim=8):
    """Generate target domain labels for debugging and testing."""
    c_trg_list = []
    for i in range(c_dim):
        c_trg = label2onehot(torch.ones(c_org.size(0))*i, c_dim)
        c_trg_list.append(c_trg.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu')))
    return c_trg_list
def label2onehot(labels, dim):
    """Convert label indices to one-hot vectors."""
    batch_size = labels.size(0)
    out = torch.zeros(batch_size, dim)
    out[np.arange(batch_size), labels.long()] = 1
    return out
def denorm(x):
    """Convert the range from [-1, 1] to [0, 1]."""
    out = (x + 1) / 2
    return out.clamp_(0, 1)

from scipy import misc

def normalize(x) :
    return x/127.5 - 1


def load_test_data(image_path, size=128):
    img = misc.imread(image_path, mode='RGB')
    img = misc.imresize(img, [size, size])
    img = np.expand_dims(img, axis=0)
    img = normalize(img)

    return img
def convert_to_opencv(image):
    # RGB -> BGR conversion is performed as well.
    r,g,b = np.array(image).T
    opencv_image = np.array([b,g,r]).transpose()
    return opencv_image
def update_orientation(image):
    exif_orientation_tag = 0x0112
    if hasattr(image, '_getexif'):
        exif = image._getexif()
        if (exif != None and exif_orientation_tag in exif):
            orientation = exif.get(exif_orientation_tag, 1)
            # orientation is 1 based, shift to zero based and flip/transpose based on 0-based values
            orientation -= 1
            if orientation >= 4:
                image = image.transpose(Image.TRANSPOSE)
            if orientation == 2 or orientation == 3 or orientation == 6 or orientation == 7:
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
            if orientation == 1 or orientation == 2 or orientation == 5 or orientation == 6:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
    return image
def resize_to_128_square(image):
    h, w = image.shape[:2]
    return cv2.resize(image, (128, 128), interpolation = cv2.INTER_LINEAR)

if __name__ == '__main__':
    model = Generator().cuda()

    state_dict = torch.load('950000-G.ckpt')

    model.load_state_dict(state_dict, strict=False)

    data_loader = get_loader('age/test', 128, 128, 1,'test', 1)
    for i, (x_real, c_org) in enumerate(data_loader):
        image = x_real
        break;

    dummy_input = image.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

    x_fake_list = [dummy_input]
    label = 8
    c_list = torch.tensor([0])
    c_list = create_labels(c_list,label)
    for i in range(len(c_list)):
        if i is 0:
            c = c_list[i]
        else:
            c = c + c_list[i]
    x = dummy_input
    c = c.view(c.size(0), c.size(1), 1, 1)
    c = c.repeat(1, 1, x.size(2), x.size(3))
    x = torch.cat([x, c], dim=1)
    x_fake_list.append(model(x))

    # Save the translated images.
    x_concat = torch.cat(x_fake_list, dim=3)
    result_path = os.path.join('', '{}-images.jpg'.format(1))
    save_image(denorm(x_concat.data.cpu()), result_path, nrow=1, padding=0)
    print('Saved real and fake images into {}...'.format(result_path))



    torch_out = torch.onnx.export(model, x, 'emotion_model.onnx', verbose=False)

    '''
    import tensorflow as tf
    import os

    graph_def = tf.GraphDef()
    labels = []

    # Import the TF graph
    with tf.gfile.FastGFile('emotion.pb', 'rb') as f:
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    from PIL import Image
    import numpy as np
    import cv2

    data_loader = get_loader('age/test', 128, 128, 1,'test', 1)
    for i, (x_real, c_org) in enumerate(data_loader):
        image = x_real
        break;

    dummy_input = image.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

    x_fake_list = [dummy_input]
    label = 8
    c_list = torch.tensor([0])
    c_list = create_labels(c_list,label)
    #for i in range(len(c_list)):
    #    if i is 0:
    #        c = c_list[i]
    #    else:
    c = c_list[0]
    x = dummy_input
    c = c.view(c.size(0), c.size(1), 1, 1)
    c = c.repeat(1, 1, x.size(2), x.size(3))
    x = torch.cat([x, c], dim=1)

    # These names are part of the model and cannot be changed.
    output_layer = 'Tanh:0'
    input_node = '0:0'

    with tf.Session() as sess:
        prob_tensor = sess.graph.get_tensor_by_name(output_layer)
        predictions, = sess.run(prob_tensor, {input_node: x })
'''
    '''
    import onnx
    import warnings
    from onnx_tf.backend import prepare
    import tensorflow as tf

    data_loader = get_loader('age/test', 128, 128, 1,'test', 1)
    for i, (x_real, c_org) in enumerate(data_loader):
        image = x_real
        break;

    dummy_input = image.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

    x_fake_list = [dummy_input]
    label = 8
    c_list = torch.tensor([0])
    c_list = create_labels(c_list,label)
    #for i in range(len(c_list)):
    #    if i is 0:
    #        c = c_list[i]
    #    else:
    c = c_list[0]
    x = dummy_input
    c = c.view(c.size(0), c.size(1), 1, 1)
    c = c.repeat(1, 1, x.size(2), x.size(3))
    x = torch.cat([x, c], dim=1)
    onnx_model = onnx.load("emotion_model.onnx")  # load onnx model
    tf_rep = prepare(onnx_model)  # prepare tf representation

    x = tf_rep.run(x)._0
    result_img = Image.fromarray(np.uint8(result_img[0, 0, :, :].clip(0, 255)),mode='RGB')
    result_img.save('2.jpg')
    '''
'''
    warnings.filterwarnings('ignore') # Ignore all the warning messages in this tutorial
    onnx_model = onnx.load("emotion_model.onnx")  # load onnx model
    tf_rep = prepare(onnx_model)  # prepare tf representation
    x_init = np.asarray(load_test_data('1.jpg', size=128))
    c = tf.constant([[1,0,0,0,0,0,0,0]])
    print(c.shape)
    c = tf.cast(tf.reshape(c, shape=[-1, c.shape[-1], 1, 1]), tf.float32)
    print(c.shape)
    c = tf.tile(c, [1, 1, x_init.shape[1], x_init.shape[2]])
    print(c.shape)
    print(x_init.shape)
    x_init = tf.cast(tf.reshape(x_init, shape=[1,3,128,128]), tf.float32)
    print(x_init.shape)

    x = tf.concat([x_init, c], 1, name='0')
    print(x.shape)
    tf.identity(x, name="0")

    result_img = tf_rep.run(x)._0

    result_img.save('2.jpg')
'''

    #tf_rep.export_graph('emotion.pb')  # export the model

'''
    import onnx
    # Load the ONNX model
    model = onnx.load("emotion_model.onnx")

    # Check that the IR is well formed
    print (onnx.checker.check_model(model))

    # Print a human readable representation of the graph
    print(onnx.helper.printable_graph(model.graph))
    '''
'''
    model = Generator().cuda()

    state_dict = torch.load('950000-G.ckpt')

    model.load_state_dict(state_dict, strict=False)

    data_loader = get_loader('age/test', 128, 128, 1,'test', 1)
    for i, (x_real, c_org) in enumerate(data_loader):
        image = x_real
        break;

    dummy_input = image.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

    x_fake_list = [dummy_input]
    label = 8
    c_list = torch.tensor([0])
    c_list = create_labels(c_list,label)
    for i in range(len(c_list)):
        if i is 0:
            c = c_list[i]
        else:
            c = c + c_list[i]
    x = dummy_input
    c = c.view(c.size(0), c.size(1), 1, 1)
    c = c.repeat(1, 1, x.size(2), x.size(3))
    x = torch.cat([x, c], dim=1)
    x_fake_list.append(model(x))

    # Save the translated images.
    x_concat = torch.cat(x_fake_list, dim=3)
    result_path = os.path.join('', '{}-images.jpg'.format(1))
    save_image(denorm(x_concat.data.cpu()), result_path, nrow=1, padding=0)
    print('Saved real and fake images into {}...'.format(result_path))



    torch_out = torch.onnx.export(model, x, 'emotion_model.onnx', verbose=False)
'''
'''
    model = onnx.load("model.onnx")
    prepared_backend = onnx_caffe2.backend.prepare(model)
    W = {model.graph.input[0].name: x.data.numpy()}
    c2_out = prepared_backend.run(W)[0]
    np.testing.assert_almost_equal(torch_out.data.cpu().numpy(), c2_out, decimal=3)
'''





'''

x = torch.randn (3, 6, 1, 1)
y = x.data.numpy()
#y = np.random.rand(3,6,1,1)
#x = torch.from_numpy(y)

y_hat = np.tile(y, (1,1,5,10))
x_hat = torch.from_numpy(y_hat)
#x_hat = x.repeat (1,1,5,10)

print (x_hat)
#print (z)
print (y_hat)

print (x)
print (y)
'''
