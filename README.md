# GUPNet

This is the official implementation of "Geometry Uncertainty Projection Network for Monocular 3D Object Detection".

## Citation

If you find our work useful in your research, please consider citing:

    @article{lu2021geometry,title={Geometry Uncertainty Projection Network for Monocular 3D Object Detection},author={Lu, Yan and Ma, Xinzhu and Yang, Lei and Zhang, Tianzhu and Liu, Yating and Chu, Qi and Yan, Junjie and Ouyang, Wanli},journal={arXiv preprint arXiv:2107.13774},year={2021}}

## Training

Download the KITTI dataset from [KITTI website](http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d), includiing left color images, camera calibration matrices and training labels.

Clone this project and then go to the code directory:

    git clone https://github.com/SuperMHP/GUPNet.git
    cd code

Install the requirements:

    pip install -r requirements.yml

Train the model:

    CUDA_VISIBLE_DEVICES=0,1,2 python tools/train_val.py

## Evaluation

To test the model, you need to modify the "resume" of the "tester" in the code/experiments/config.yaml and then run:

    python tools/train_val.py -e

After that, please use the kitti evaluation devkit (deails can be refered to [FrustumPointNet](https://github.com/charlesq34/frustum-pointnets)) to evaluate:

    g++ evaluate_object_3d_offline_apXX.cpp -o evaluate_object_3d_offline_ap
    ../../tools/kitti_eval/evaluate_object_3d_offline_apXX KITTI_LABEL_DIR ./output

We also provide the trained checkpoint which achieved best multi-catagory performance on the validation set. It can be downloaded at [here](https://drive.google.com/file/d/1-iQEjNlWMGYC-wC4kN6We_TBbBmeKsmz/view?usp=sharing).
