import logging
from typing import List

import torch
from torch import Tensor

from attnganw import config


def get_single_normal_vector(shape, gpu_id: int) -> List[Tensor]:
    noise_vector = torch.FloatTensor(*shape)
    if gpu_id >= 0:
        noise_vector = noise_vector.cuda()
    noise_vector.data.normal_(mean=0, std=1)

    return [noise_vector]


def get_zeroes(shape, gpu_id: int) -> Tensor:
    zero: Tensor = torch.zeros(*shape)
    if gpu_id >= 0:
        zero = zero.cuda()

    return zero

def get_vector_interpolation(batch_size: int, noise_vector_size: int, gpu_id: int,
                             noise_vector_start: Tensor = None,
                             noise_vector_end: Tensor = None) -> List[Tensor]:
    if noise_vector_start is None:
        noise_vector_start: Tensor = torch.randn(batch_size, noise_vector_size, dtype=torch.float)

    if noise_vector_end is None:
        noise_vector_end: Tensor = torch.randn(batch_size, noise_vector_size, dtype=torch.float)

    noise_vectors: List[Tensor] = []
    number_of_steps: int = config.generation['noise_interpolation_steps']
    for vector_index in range(number_of_steps + 1):
        ratio: float = vector_index / float(number_of_steps)
        # ratio = 0

        logging.debug("ratio " + str(ratio))
        new_noise_vector: Tensor = noise_vector_start * (1 - ratio) + noise_vector_end * ratio
        if gpu_id >= 0:
            new_noise_vector = new_noise_vector.cuda()
        noise_vectors.append(new_noise_vector)

    return noise_vectors