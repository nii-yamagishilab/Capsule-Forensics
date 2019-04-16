# Capsule-Forensics

Implementation of the paper:  <a href="https://arxiv.org/abs/1810.11215">Capsule-Forensics: Using Capsule Networks to Detect Forged Images and Videos</a> (ICASSP 2019).

You can clone this repository into your favorite directory:

    $ git clone https://github.com/nii-yamagishilab/Capsule-Forensics

## Requirement
- PyTorch 0.3
- TorchVision
- scikit-learn
- Numpy
- pickle

## Project organization
- Datasets folder, where you can place your training, evaluation, and test set:

      ./dataset/<train; validation; test>
- Checkpoint folder, where the training outputs will be stored:

      ./checkpoints
      
## Dataset
Each dataset has two parts:
- Real images: ./dataset/\<train;test;validation\>/Real
- Fake images: ./dataset/\<train;test;validation\>/Fake


## Training
**Note**: Parameters with detail explanation could be found in the corresponding source code.

    $ python train.py

## Evaluating
**Note**: Parameters with detail explanation could be found in the corresponding source code.

    $ python test.py

## Authors
- Huy H. Nguyen (https://researchmap.jp/nhhuy/?lang=english)
- Junichi Yamagishi (https://researchmap.jp/read0205283/?lang=english)
- Isao Echizen (https://researchmap.jp/echizenisao/?lang=english)

## Reference
H. H. Nguyen, J. Yamagishi, and I. Echizen, “Capsule-Forensics: Using Capsule Networks to Detect Forged Images and Videos,” Proc. of the 2019 International Conference on Acoustics, Speech, and Signal Processing (ICASSP 2019), 5 pages, (May 2019)
