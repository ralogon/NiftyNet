from __future__ import absolute_import, print_function, division

import tensorflow as tf
import numpy as np

from niftynet.layer.resampler import ResamplerLayer


class ResamplerTest(tf.test.TestCase):
    def get_2d_input(self):
        test_case = tf.constant(
            [[[[1, 2, -1], [3, 4, -2]], [[5, 6, -3], [7, 8, -4]]],
             [[[9, 10, -5], [11, 12, -6]], [[13, 14, -7], [15, 16, -8]]]],
            dtype=tf.float32)
        return test_case

    def get_3d_input1(self):
        test_case = tf.constant(
            [[[[1, 2, -1], [3, 4, -2]], [[5, 6, -3], [7, 8, -4]]],
             [[[9, 10, -5], [11, 12, -6]], [[13, 14, -7], [15, 16, -8]]]],
            dtype=tf.float32)
        return tf.expand_dims(test_case, 4)

    def get_3d_input2(self):
        return tf.concat([self.get_3d_input1(), 100 + self.get_3d_input1()], 4)

    def _test_correctness(
            self, input, grid, interpolation, boundary, expected_value):
        resampler = ResamplerLayer(interpolation=interpolation,
                                   boundary=boundary)
        out = resampler(input, grid)
        with self.test_session() as sess:
            out_value = sess.run(out)
            #print(expected_value)
            #print(out_value)
            self.assertAllClose(expected_value, out_value)

    #def test_resampler_2d_replicate_linear_correctness(self):
    #    test_grid = tf.constant([[[.25, .25], [.25, .78]],
    #                             [[.62, .25], [.25, .28]]],
    #                            dtype=tf.float32)
    #    expected = [[[2.5, 3.5, -1.75],
    #                 [3.56, 4.56, -2.28]],
    #                [[11.98, 12.98, -6.49],
    #                 [10.56, 11.56, -5.78]]]
    #    self._test_correctness(input=self.get_2d_input(),
    #                           grid=test_grid,
    #                           interpolation='LINEAR',
    #                           boundary='ZERO',
    #                           expected_value=expected)

    #def test_resampler_3d_multivariate_replicate_linear_correctness(self):
    #    test_grid = tf.constant([[[.25, .25, .25], [.25, .75, .25]],
    #                             [[.75, .25, .25], [.25, .25, .75]]],
    #                            dtype=tf.float32)
    #    expected = [[[2.75, 102.75], [3.75, 103.75]],
    #                [[12.75, 112.75], [11.25, 111.25]]]
    #    self._test_correctness(input=self.get_3d_input2(),
    #                           grid=test_grid,
    #                           interpolation='LINEAR',
    #                           boundary='REPLICATE',
    #                           expected_value=expected)

    #def test_resampler_3d_replicate_nearest_correctness(self):
    #    test_grid = tf.constant([[[.25, .25, .25], [.25, .75, .25]],
    #                              [[.75, .25, .25], [.25, .25, .75]]],
    #                             dtype=tf.float32)
    #    expected = [[[1, 101], [3, 103]],
    #                [[13, 113], [10, 110]]]
    #    self._test_correctness(input=self.get_3d_input2(),
    #                           grid=test_grid,
    #                           interpolation='NEAREST',
    #                           boundary='REPLICATE',
    #                           expected_value=expected)

    #def test_resampler_3d_zero_nearest_correctness(self):
    #    test_grid = tf.constant([[[-.05, .25, .25], [.25, .95, .25]],
    #                              [[.75, .25, .25], [.25, .25, .75]]],
    #                             dtype=tf.float32)
    #    expected = [[[1, 101], [3, 103]],
    #                [[13, 113], [10, 110]]]
    #    self._test_correctness(input=self.get_3d_input2(),
    #                           grid=test_grid,
    #                           interpolation='NEAREST',
    #                           boundary='ZEO',
    #                           expected_value=expected)

    #def test_resampler_3d_replicate_linear_correctness(self):
    #    self._test_correctness(input=self.get_3d_input1(),
    #                           grid=tf.constant(
    #                               [[[.25, .25, .25], [.25, .75, .25]],
    #                                [[.75, .25, .25], [.25, .25, .75]]],
    #                               dtype=tf.float32),
    #                           interpolation='LINEAR',
    #                           boundary='REPLICATE',
    #                           expected_value=[[[2.75], [3.75]],
    #                                           [[12.75], [11.25]]])

    def test_resampler_3d_replicate_cubic_correctness(self):
        self._test_correctness(input=self.get_3d_input1(),
                               grid=tf.constant(
                                   [[[.25,.25,.25],[.25,.75,.25]],
                                   [[.75,.25,.25],[.25,.25,.75]]],
                                   dtype=tf.float32),
                               interpolation='BSPLINE',
                               boundary='REPLICATE',
                               expected_value=[[[3.20869954],[3.93501790]],
                                               [[12.63008626],[10.33280436]]])

    #def test_resampler_3d_replicate_nearest_correctness(self):
    #    self._test_correctness(input=self.get_3d_input1(),
    #                           grid=tf.constant(
    #                               [[[.25, .25, .25], [.25, .75, .25]],
    #                                [[.75, .25, .25], [.25, .25, .75]]],
    #                               dtype=tf.float32),
    #                           interpolation='NEAREST',
    #                           boundary='REPLICATE',
    #                           expected_value=[[[1], [3]], [[13], [10]]])

    #def test_resampler_3d_circular_linear_correctness(self):
    #    self._test_correctness(input=self.get_3d_input1(),
    #                           grid=tf.constant([[[.25, .25 + 2, .25 + 3],
    #                                              [.25 - 2, .75 - 2, .25 - 3]],
    #                                             [[.75 + 2, .25 - 2, .25 - 3],
    #                                              [.25 + 2, .25 - 2, .75 + 3]]],
    #                                            dtype=tf.float32),
    #                           interpolation='LINEAR',
    #                           boundary='CIRCULAR',
    #                           expected_value=[[[2.75], [3.75]],
    #                                           [[12.75], [11.25]]])

    #def test_resampler_3d_circular_nearest_correctness(self):
    #    self._test_correctness(input=self.get_3d_input1(),
    #                           grid=tf.constant([[[.25, .25 + 2, .25 + 3],
    #                                              [.25 - 2, .75 - 2, .25 - 3]],
    #                                             [[.75 + 4, .25 - 6, .25 - 6],
    #                                              [.25 + 2, .25 - 4, .75 + 9]]],
    #                                            dtype=tf.float32),
    #                           interpolation='NEAREST',
    #                           boundary='CIRCULAR',
    #                           expected_value=[[[1], [3]], [[13], [10]]])

    #def test_resampler_3d_symmetric_linear_correctness(self):
    #    self._test_correctness(input=self.get_3d_input1(),
    #                           grid=tf.constant([[[-.25, -.25, -.25],
    #                                              [.25 + 2, .75 + 2, .25 + 4]],
    #                                             [[.75, .25, -.25 + 4],
    #                                              [.25, .25, .75]]],
    #                                            dtype=tf.float32),
    #                           interpolation='LINEAR',
    #                           boundary='SYMMETRIC',
    #                           expected_value=[[[2.75], [3.75]],
    #                                           [[12.75], [11.25]]])

    #def test_resampler_3d_symmetric_nearest_correctness(self):
    #    self._test_correctness(input=self.get_3d_input1(),
    #                           grid=tf.constant([[[-.25, -.25, -.25],
    #                                              [.25 + 2, .75 + 2, .25 + 4]],
    #                                             [[.75, .25, -.25 + 4],
    #                                              [.25, .25, .75]]],
    #                                            dtype=tf.float32),
    #                           interpolation='NEAREST',
    #                           boundary='SYMMETRIC',
    #                           expected_value=[[[1], [3]], [[13], [10]]])



if __name__ == "__main__":
    tf.test.main()
