'''
Blog:https://blog.csdn.net/qq_31622015/article/details/103364467
'''

import torch


def iou_loss(preds, bbox, eps=1e-6, reduction='mean'):
    '''
    https://github.com/open-mmlab/mmdetection/blob/master/mmdet/models/losses/iou_loss.py
    :param preds:[[x1,y1,x2,y2], [x1,y1,x2,y2],,,]
    :param bbox:[[x1,y1,x2,y2], [x1,y1,x2,y2],,,]
    :return: loss
    '''
    x1 = torch.max(preds[:, 0], bbox[:, 0])
    y1 = torch.max(preds[:, 1], bbox[:, 1])
    x2 = torch.min(preds[:, 2], bbox[:, 2])
    y2 = torch.min(preds[:, 3], bbox[:, 3])

    w = (x2 - x1 + 1.0).clamp(0.)
    h = (y2 - y1 + 1.0).clamp(0.)

    inters = w * h

    uni = (preds[:, 2] - preds[:, 0] + 1.0) * (preds[:, 3] - preds[:, 1] + 1.0) + (bbox[:, 2] - bbox[:, 0] + 1.0) * (
            bbox[:, 3] - bbox[:, 1] + 1.0) - inters

    ious = (inters / uni).clamp(min=eps)
    loss = -ious.log()

    if reduction == 'mean':
        loss = torch.mean(loss)
    elif reduction == 'sum':
        loss = torch.sum(loss)
    else:
        raise NotImplementedError
    return loss


if __name__ == '__main__':
    pred_bboxes = torch.tensor([[15, 18, 47, 60],
                                [50, 50, 90, 100],
                                [70, 80, 120, 145],
                                [130, 160, 250, 280],
                                [25.6, 66.1, 113.3, 147.8]], dtype=torch.float)
    gt_bbox = torch.tensor([[70, 80, 120, 150]], dtype=torch.float)
    print(iou_loss(pred_bboxes, gt_bbox))
