import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(ROOT_DIR)

import yaml
import logging
import argparse

from lib.helpers.dataloader_helper import build_dataloader
from lib.helpers.model_helper import build_model
from lib.helpers.optimizer_helper import build_optimizer
from lib.helpers.scheduler_helper import build_lr_scheduler
from lib.helpers.trainer_helper import Trainer
from lib.helpers.tester_helper import Tester
from datetime import datetime

parser = argparse.ArgumentParser(description='implementation of GUPNet')
parser.add_argument('-e', '--evaluate', dest='evaluate', action='store_true', help='evaluate model on validation set')
parser.add_argument('--config', type=str, default = 'experiments/config.yaml')
args = parser.parse_args()

def create_logger(log_file):
    log_format = '%(asctime)s  %(levelname)5s  %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format, filename=log_file)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(__name__).addHandler(console)
    return logging.getLogger(__name__)


def main():  
    # load cfg
    assert (os.path.exists(args.config))
    cfg = yaml.load(open(args.config, 'r'), Loader=yaml.Loader)
    logger = create_logger(os.path.join(cfg['trainer']['log_dir'],'train.log'))    
    
    #  build dataloader
    train_loader, val_loader, _ = build_dataloader(cfg['dataset'])

    # build model
    model = build_model(cfg['model'],train_loader.dataset.cls_mean_size)

    # evaluation mode
    if args.evaluate:
        tester = Tester(cfg['tester'], model, val_loader, logger)
        tester.test()
        return

    #  build optimizer
    optimizer = build_optimizer(cfg['optimizer'], model)

    # build lr & bnm scheduler
    lr_scheduler, warmup_lr_scheduler = build_lr_scheduler(cfg['lr_scheduler'], optimizer, last_epoch=-1)

    trainer = Trainer(cfg=cfg,
                      model=model,
                      optimizer=optimizer,
                      train_loader=train_loader,
                      test_loader=val_loader,
                      lr_scheduler=lr_scheduler,
                      warmup_lr_scheduler=warmup_lr_scheduler,
                      logger=logger)
    trainer.train()
    tester = Tester(cfg['tester'], model, val_loader, logger)
    tester.test()


if __name__ == '__main__':
    main()