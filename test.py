"""
Copyright (c) 2018, National Institute of Informatics
All rights reserved.
Author: Huy H. Nguyen
-----------------------------------------------------
Script for testing Capsule-Forensics
"""

import sys
sys.setrecursionlimit(15000)
import os
import torch
import numpy as np
from torch.autograd import Variable
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
from tqdm import tqdm
import argparse
from sklearn import metrics
import model

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', default ='dataset', help='path to dataset')
parser.add_argument('--test_set', default ='test', help='test set')
parser.add_argument('--workers', type=int, help='number of data loading workers', default=1)
parser.add_argument('--batchSize', type=int, default=100, help='input batch size')
parser.add_argument('--imageSize', type=int, default=128, help='the height / width of the input image to network')
parser.add_argument('--gpu_id', type=int, default=0, help='GPU ID')
parser.add_argument('--outf', default='checkpoints', help='folder to output model checkpoints')
parser.add_argument('--random', action='store_true', default=False, help='enable randomness for routing matrix')
parser.add_argument('--id', type=int, help='checkpoint ID')

opt = parser.parse_args()
print(opt)

if __name__ == '__main__':

    text_writer = open(os.path.join(opt.outf, 'test.txt'), 'w')

    transform_fwd = transforms.Compose([
        transforms.Resize(opt.imageSize),
        transforms.CenterCrop(opt.imageSize),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ])


    dataset_test = dset.ImageFolder(root=os.path.join(opt.dataset, opt.test_set), transform=transform_fwd)
    assert dataset_test
    dataloader_test = torch.utils.data.DataLoader(dataset_test, batch_size=opt.batchSize, shuffle=False, num_workers=int(opt.workers))

    vgg_ext = model.VggExtractor()
    capnet = model.CapsuleNet(opt.gpu_id)
    capsule_loss = model.CapsuleLoss(opt.gpu_id)

    capnet.load_state_dict(torch.load(os.path.join(opt.outf,'capsule_' + str(opt.id) + '.pt')))
    capnet.eval()

    if opt.gpu_id >= 0:
        vgg_ext.cuda(opt.gpu_id)
        capsule_loss.cuda(opt.gpu_id)
        capnet.cuda(opt.gpu_id)


    ##################################################################################

    tol_label = np.array([], dtype=np.float)
    tol_pred = np.array([], dtype=np.float)

    count = 0
    loss_test = 0

    for img_data, labels_data in tqdm(dataloader_test):

        img_label = labels_data.numpy().astype(np.float)

        if opt.gpu_id >= 0:
            img_data = img_data.cuda(opt.gpu_id)
            labels_data = labels_data.cuda(opt.gpu_id)

        input_v = Variable(img_data)

        x = vgg_ext(input_v)
        classes, class_ = capnet(x, random=opt.random)

        loss_dis = capsule_loss(classes, Variable(labels_data, requires_grad=False))
        loss_dis_data = loss_dis.item()
        output_dis = class_.data.cpu().numpy()

        output_pred = np.zeros((output_dis.shape[0]), dtype=np.float)

        for i in range(output_dis.shape[0]):
            if output_dis[i,1] >= output_dis[i,0]:
                output_pred[i] = 1.0
            else:
                output_pred[i] = 0.0

        tol_label = np.concatenate((tol_label, img_label))
        tol_pred = np.concatenate((tol_pred, output_pred))

        loss_test += loss_dis_data
        count += 1

    acc_test = metrics.accuracy_score(tol_label, tol_pred)
    loss_test /= count

    fpr, tpr, threshold = metrics.roc_curve(tol_label, tol_pred)
    fnr = 1 - tpr
    # hter = (fpr + fnr)/2

    print('Test loss: %.4f | Test accuracy: %.2f' % (loss_test, acc_test*100))
    text_writer.write('%.4f,%.2f\n' % (loss_test, acc_test*100))

    text_writer.flush()
    text_writer.close()
