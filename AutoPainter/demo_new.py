from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import base64

import json
import tensorflow as tf
from PIL import Image, ImageEnhance
from pylab import *
from scipy.ndimage import filters

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
model1 = {}
model2 = {}
model2 = {}
def sketchify(files1, outpath):
    filepath, filename = os.path.split(files1)
    out_dir, outname = os.path.split(outpath)
    Gamma = 0.97
    Phi = 200
    Epsilon = 0.1
    k = 2.5
    Sigma = 1.5

    im = Image.open(files1).convert('L')
    im = array(ImageEnhance.Sharpness(im).enhance(3.0))
    im1 = filters.gaussian_filter(im, Sigma)
    im2 = filters.gaussian_filter(im, Sigma * k)
    differencedIm1 = im1 - (Gamma * im2)
    (x, y) = shape(im1)
    for i in range(x):
        for j in range(y):
            if differencedIm1[i, j] < Epsilon:
                differencedIm1[i, j] = 1
            else:
                differencedIm1[i, j] = 250 + tanh(Phi * (differencedIm1[i, j]))
    basemat = differencedIm1.astype(np.uint8)
    if basemat.ndim == 2:
        basemat = np.expand_dims(basemat, 2)
        basemat = np.tile(basemat, [1, 1, 3])
    final_img = Image.fromarray(basemat)
    final_img.save(os.path.join(out_dir, outname))
    

def load_model1(local_models_dir):
    for name in os.listdir(local_models_dir):
        if name.startswith("."):
            continue

        print("loading model", name)

        with tf.compat.v1.Graph().as_default() as graph:
            config = tf.compat.v1.ConfigProto()
            config.gpu_options.allow_growth = True
            sess = tf.compat.v1.Session(config=config,graph=graph)
            saver = tf.compat.v1.train.import_meta_graph(os.path.join(local_models_dir, "export.meta"))

            saver.restore(sess, os.path.join(local_models_dir, "export"))
            input_vars = json.loads(tf.compat.v1.get_collection("inputs")[0].decode("utf-8"))
            output_vars = json.loads(tf.compat.v1.get_collection("outputs")[0].decode("utf-8"))
            input = graph.get_tensor_by_name(input_vars["input"])
            output = graph.get_tensor_by_name(output_vars["output"])

            if name not in model1:
                model1[name] = {}

            model1[name]["local"] = dict(
                sess=sess,
                input=input,
                output=output,
            )


def input_pic1(input_dir, output_dir):
    f = open(input_dir, 'rb')
    filedata = f.read()
    f.close()
    filedata = bytearray(filedata)
    input_b64data = base64.urlsafe_b64encode(filedata)
    m1 = model1["checkpoint"]["local"]
    output_b64data = m1["sess"].run(m1["output"], feed_dict={m1["input"]: [input_b64data]})[0]
    output_b64data += b'=' * (-len(output_b64data) % 4)
    output_data = base64.urlsafe_b64decode(output_b64data)
    f1 = open(output_dir, 'wb')
    f1.write(output_data)
    f1.close()

def load_model2(local_models_dir):
    for name in os.listdir(local_models_dir):
        if name.startswith("."):
            continue

        print("loading model", name)

        with tf.compat.v1.Graph().as_default() as graph:
            config = tf.compat.v1.ConfigProto()
            config.gpu_options.allow_growth = True
            sess = tf.compat.v1.Session(config=config,graph=graph)
            saver = tf.compat.v1.train.import_meta_graph(os.path.join(local_models_dir, "export.meta"))

            saver.restore(sess, os.path.join(local_models_dir, "export"))
            input_vars = json.loads(tf.compat.v1.get_collection("inputs")[0].decode("utf-8"))
            output_vars = json.loads(tf.compat.v1.get_collection("outputs")[0].decode("utf-8"))
            input = graph.get_tensor_by_name(input_vars["input"])
            output = graph.get_tensor_by_name(output_vars["output"])

            if name not in model2:
                model2[name] = {}

            model2[name]["local"] = dict(
                sess=sess,
                input=input,
                output=output,
            )


def input_pic2(input_dir, output_dir):
    f = open(input_dir, 'rb')
    filedata = f.read()
    f.close()
    filedata = bytearray(filedata)
    input_b64data = base64.urlsafe_b64encode(filedata)
    m2 = model2["checkpoint"]["local"]
    output_b64data = m2["sess"].run(m2["output"], feed_dict={m2["input"]: [input_b64data]})[0]
    output_b64data += b'=' * (-len(output_b64data) % 4)
    output_data = base64.urlsafe_b64decode(output_b64data)
    f2 = open(output_dir, 'wb')
    f2.write(output_data)
    f2.close()
    
load_model1('./AutoPainter/media/autopaint_model/model1')
load_model2('./AutoPainter/media/autopaint_model/model2')