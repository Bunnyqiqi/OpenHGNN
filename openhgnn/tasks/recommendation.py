import argparse
import copy
import dgl
import numpy as np
import torch
from tqdm import tqdm
import torch.nn.functional as F
from openhgnn.models import build_model

from . import BaseTask, register_task
from ..dataset import build_dataset
from ..utils import Evaluator


@register_task("recommendation")
class Recommendation(BaseTask):
    """Recommendation tasks."""
    def __init__(self, args):
        super(Recommendation, self).__init__()
        self.n_dataset = args.dataset
        self.dataset = build_dataset(args.dataset, 'recommendation')
        # self.evaluator = Evaluator()
        self.evaluator = Evaluator(args.seed)

    def get_graph(self):
        return self.dataset.g

    def get_loss_fn(self):
        return F.binary_cross_entropy_with_logits

    def get_evaluator(self, name):
        if name == 'acc':
            return self.evaluator.author_link_prediction
        elif name == 'mrr':
            return self.evaluator.mrr_
        elif name == 'academic_lp':
            return self.evaluator.author_link_prediction

    def evaluate(self, y_true, y_score, name):
        if name == 'ndcg':
            return self.evaluator.ndcg(y_true, y_score)

    def get_batch(self):
        return self.dataset.train_batch, self.dataset.test_batch

    def get_idx(self):
        return self.train_idx, self.val_idx, self.test_idx

    def get_labels(self):
        return self.dataset.get_labels()

