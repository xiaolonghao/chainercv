import numpy as np

import chainer


class StubLink(chainer.Link):
    """A chainer.Link that returns dummy value(s).

    This is a :obj:`chainer.Link` that returns dummy
    :obj:`chainer.Variable`(s) when :meth:`__call__` method is called.

    Args:
        shapes (iterable of int or tuple of int): The shapes of returned
            variables. If :obj:`len(shapes) == 1`, :meth:`__call__` returns
            a :obj:`chainer.Variable`. Otherwise, it returns a tuple of
            :obj:`chainer.Variable`.
        value (:obj:`'uniform'`, int or float): The value of returned
            variable. If this is :obj:`'uniform'`, the values of the variable
            are drawn from an uniformed distribution. Otherwise, They are
            initalized with the specified value.
            The default value is :obj:`'uniform'`.
        dtype: The type of returned variable. The default value is
            :obj:`~numpy.float32`.
    """

    def __init__(self, shapes, value='uniform', dtype=np.float32):
        super(StubLink, self).__init__()

        self.shapes = shapes

        if value == 'uniform':
            def _get_array(shape):
                return np.random.uniform(size=shape).astype(dtype)
        elif isinstance(value, (int, float)):
            def _get_array(shape):
                array = np.empty(shape, dtype=dtype)
                array[:] = value
                return array
        else:
            raise ValueError('value must be \'uniform\', int or float')

        self._get_array = _get_array

    def __call__(self, *_):
        """Returns dummy value(s).

        Args:
            This method can take any values as its arguments.
            This function returns values independent of the arguments.

        Returns:
            chainer.Variable or tuple of chainer.Variable:
            If :obj:`len(shapes) == 1`, this method returns
            a :obj:`chainer.Variable`. Otherwise, this returns a
            tuple of :obj:`chainer.Variable`.
        """

        outputs = tuple(
            chainer.Variable(self.xp.asarray(self._get_array(shape)))
            for shape in self.shapes)

        if len(outputs) == 1:
            return outputs[0]
        else:
            return outputs
