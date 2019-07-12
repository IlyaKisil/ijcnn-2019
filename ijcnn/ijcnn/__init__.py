from hottbox.core import Tensor, TensorTKD
from hottbox.utils.generation import residual_tensor


def compression_rate(tensor, tensor_rep):
    """

    Parameters
    ----------
    tensor : Tensor
    tensor_rep : TensorTKD

    Returns
    -------
    float
    """
    s1 = tensor.size
    s2 = tensor_rep.core.size
    for fmat in tensor_rep.fmat:
        s2 += fmat.size
    return s1 / s2


def print_basic_metrics(tensor, tensor_rep):
    """

    Parameters
    ----------
    tensor : Tensor
    tensor_rep : TensorTKD
    """

    rel_error = (residual_tensor(tensor, tensor_rep).frob_norm / tensor.frob_norm) * 100
    comp_rate = compression_rate(tensor, tensor_rep)
    print("{}\n".format(tensor_rep))
    print("Basic metrics:")
    print("--------------")
    print("Compression rate = {:.2f}\n".format(comp_rate))
    print("Relative error of approximation = {:.2f}%\n".format(rel_error))
