import os
import torch
from abc import ABC, abstractmethod


class BaseFlow(ABC):

    def __init__(self, args):
        super(BaseFlow, self).__init__()
        self.evaluator = None
        self.evaluate_interval = 1
        self.load_from_checkpoint = True
        if hasattr(args, '_checkpoint'):
            self._checkpoint = os.path.join(args._checkpoint,
                                            f"{args.model}_{args.dataset}.pt")
        else:
            if self.load_from_checkpoint:
                self._checkpoint = os.path.join("./openhgnn/output/{}".format(args.model),
                                                f"{args.model}_{args.dataset}.pt")
            else:
                self._checkpoint = None

    @abstractmethod
    def train(self):
        pass

    def _full_train_step(self):
        # train with a full_batch graph
        raise NotImplementedError

    def _mini_train_step(self):
        # train with a mini_batch seed nodes graph
        raise NotImplementedError

    def _test_step(self):
        raise NotImplementedError

    def load_from_pretrained(self):
        if self.load_from_checkpoint:
            try:
                ck_pt = torch.load(self._checkpoint)
                self.model.load_state_dict(ck_pt)
            except FileNotFoundError:
                print(f"'{self._checkpoint}' doesn't exists")
        return self.model

    def save_checkpoint(self):
        if self._checkpoint and hasattr(self.model, "_parameters()"):
            torch.save(self.model.state_dict(), self._checkpoint)
