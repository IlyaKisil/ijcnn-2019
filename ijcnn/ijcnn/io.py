import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from hottbox.core import Tensor


# Ideally we would want to have an environment variable
_IJCNN_2019_HOME = Path(__file__).resolve().parents[2]
_DATA_HOME = os.path.join(_IJCNN_2019_HOME, "data")
_ETH80_HOME = os.path.join(_DATA_HOME, 'ETH80')


class ETH80(object):
    """ Class for interacting with images from the ETH-80 dataset.

    Attributes
    ----------
    _META : pd.DataFrame
        Contains meta data of all images from the ETH-80 dataset in the columns: Label, Object, Angle_1, Angle_2, Path.
        Label - for classification, ranges between 1 and 8 including
        Object - there are 10 different objects that with the same Label
        Angle_1, Angle_2 - there are 41 combinations of these two variables for each object
        Path - location of the image which name follows patters: Object-Angle_1-Angle_2.png

    Notes
    -----
    1.  More info about this dataset (eth80-cropped-close128.tgz) can be found on:
        https://www.mpi-inf.mpg.de/departments/computer-vision-and-multimodal-computing/research/object-recognition
        -and-scene-understanding/analyzing-appearance-and-contour-based-methods-for-object-categorization/

    2.  Car objects are ordered in different way
    """

    _objects_to_labels = {"apple": 1,
                          "car": 2,
                          "cow": 3,
                          "cup": 4,
                          "dog": 5,
                          "horse": 6,
                          "pear": 7,
                          "tomato": 8,
                          }

    def __init__(self) -> None:
        self._META = self._get_eth_meta()

    @staticmethod
    def _get_eth_meta():
        """ Read file with eth-80 meta data into pandas dataframe

        Returns
        -------
        df : pd.DataFrame
        """
        meta_data_path = os.path.join(_ETH80_HOME, 'meta_data.csv')
        df = pd.read_csv(meta_data_path, dtype={'Angle_1': str, 'Angle_2': str, 'Label': 'int8'})
        df['id'] = df.apply(lambda x: '-'.join([x['Object'], x['Angle_1'], x['Angle_2']]), axis=1)
        return df

    @property
    def meta_data(self):
        """ Dataframe with meta data of all samples for the ETH-80 dataset.

        It is stored in the columns: Angle_1, Angle_2, Label, Object, id.
            Angle_1 (str), Angle_2 (str) - there are 41 combinations of these two variables for each object \n
            Label (np.int8) - for classification, ranges between 1 and 8 including \n
            Object (str) - there are 10 different objects that with the same Label \n
            id (str) - Unique name of the sample that follows pattern: Object-Angle_1-Angle_2

        Returns
        -------
        df : pd.DataFrame
        """
        return self._META

    @property
    def available_objects(self):
        return list(self._objects_to_labels.keys())

    @property
    def available_angle_pairs(self):
        return self.meta_data.groupby(["Angle_1", "Angle_2"]).size()

    def get_samples(self, objects=(), angle_1=(), angle_2=(), as_tensor=True):
        """ Get representations of images from the ETH-80 dataset.

        Parameters
        ----------
        objects : list[str]
            List of objects of interest.
        angle_1 : list[str]
            List of angles of interest along longitude (from north to south).
        angle_2 : list[str]
            List of angles of interest along latitude (from west to east).
        as_tensor : bool
            If True, return samples as ``Tensor`` objects, numpy arrays otherwise.

        Returns
        -------
        samples : list[Tensor]
            List of tensors with dimensions representing height, width and color respectively.
        labels : np.ndarray
            Array of corresponding labels.
        """
        df = self.meta_data
        if len(angle_1) > 0:
            df = df[df.Angle_1.isin(angle_1)]

        if len(angle_2) > 0:
            df = df[df.Angle_2.isin(angle_2)]

        if len(objects) > 0:
            labels = [self._objects_to_labels[obj] for obj in objects]
            df = df[df.Label.isin(labels)]

        if df.empty:
            raise ValueError("Selected criteria are not present in this dataset. "
                             "Most likely, the specified pair(s) of `angle_1` and `angle_2` does not exist. \n"
                             "HINT: Use 'available_angle_pairs' and 'available_objects' to see correct options.")

        path = df.apply(lambda x: os.path.join(_ETH80_HOME, "original", "{}.npz".format(x['id'])),
                        axis=1
                        )
        data_as_series = path.apply(lambda x: np.load(x)['image'].astype(np.float))

        labels = df.Label.values

        if as_tensor:
            samples = [Tensor(sample, mode_names=["pixel_X", "pixel_Y", "color"]) for sample in data_as_series.tolist()]
        else:
            samples = data_as_series.tolist()

        return samples, labels


def rgb_to_gray(image):
    """ Convert to gray-scale

    Parameters
    ----------
    image : np.ndarray

    Returns
    -------
    np.ndarray
    """
    return np.dot(image[..., :3], [0.299, 0.587, 0.114])


def plot_tensors(tensors):
    """ Utility to plot tensors

    Parameters
    ----------
    tensors : {list[Tensor], list[np.ndarray]}
    """
    if len(tensors) > 4:
        n_plots_total = 4
    else:
        n_plots_total = len(tensors)

    fig = plt.figure(figsize=(12, 4))

    for i in range(n_plots_total):
        image = tensor_to_image(tensors[i])
        ax = fig.add_subplot(1, n_plots_total, i+1)
        ax.imshow(image)
        ax.set_axis_off()
        plt.title('Tensor {}'.format(i+1))


def tensor_to_image(tensor):
    """ Prepare a ``tensor`` for plotting

    Parameters
    ----------
    tensor : {Tensor, np.ndarray}

    Returns
    -------
    image : np.ndarray
    """
    if isinstance(tensor, Tensor):
        image = tensor.data.copy()
    else:
        image = tensor.copy()
    image -= image.min()
    image /= image.max()
    image *= 255
    return image.astype(np.uint8)
