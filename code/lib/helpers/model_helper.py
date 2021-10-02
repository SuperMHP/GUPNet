from lib.models.gupnet import GUPNet


def build_model(cfg,mean_size):
    if cfg['type'] == 'gupnet':
        return GUPNet(backbone=cfg['backbone'], neck=cfg['neck'], mean_size=mean_size)
    else:
        raise NotImplementedError("%s model is not supported" % cfg['type'])
