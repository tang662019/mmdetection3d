from mmdet.models.backbones import RegNet
from ..builder import BACKBONES


@BACKBONES.register_module()
class NoStemRegNet(RegNet):
    """RegNet backbone without Stem for 3D detection.

    More details can be found in `paper <https://arxiv.org/abs/2003.13678>`_ .

    Args:
        arch (dict): The parameter of RegNets.
            - w0 (int): initial width
            - wa (float): slope of width
            - wm (float): quantization parameter to quantize the width
            - depth (int): depth of the backbone
            - group_w (int): width of group
            - bot_mul (float): bottleneck ratio, i.e. expansion of bottlneck.
        strides (Sequence[int]): Strides of the first block of each stage.
        base_channels (int): Base channels after stem layer.
        in_channels (int): Number of input image channels. Normally 3.
        dilations (Sequence[int]): Dilation of each stage.
        out_indices (Sequence[int]): Output from which stages.
        style (str): `pytorch` or `caffe`. If set to "pytorch", the stride-two
            layer is the 3x3 conv layer, otherwise the stride-two layer is
            the first 1x1 conv layer.
        frozen_stages (int): Stages to be frozen (all param fixed). -1 means
            not freezing any parameters.
        norm_cfg (dict): dictionary to construct and config norm layer.
        norm_eval (bool): Whether to set norm layers to eval mode, namely,
            freeze running stats (mean and var). Note: Effect on Batch Norm
            and its variants only.
        with_cp (bool): Use checkpoint or not. Using checkpoint will save some
            memory while slowing down the training speed.
        zero_init_residual (bool): whether to use zero init for last norm layer
            in resblocks to let them behave as identity.

    Example:
        >>> from mmdet3d.models import NoStemRegNet
        >>> import torch
        >>> self = NoStemRegNet(
                arch=dict(
                    w0=88,
                    wa=26.31,
                    wm=2.25,
                    group_w=48,
                    depth=25,
                    bot_mul=1.0))
        >>> self.eval()
        >>> inputs = torch.rand(1, 64, 16, 16)
        >>> level_outputs = self.forward(inputs)
        >>> for level_out in level_outputs:
        ...     print(tuple(level_out.shape))
        (1, 96, 8, 8)
        (1, 192, 4, 4)
        (1, 432, 2, 2)
        (1, 1008, 1, 1)
    """

    def __init__(self, arch, **kwargs):
        super(NoStemRegNet, self).__init__(arch, **kwargs)

    def _make_stem_layer(self, in_channels, base_channels):
        return

    def forward(self, x):
        outs = []
        for i, layer_name in enumerate(self.res_layers):
            res_layer = getattr(self, layer_name)
            x = res_layer(x)
            if i in self.out_indices:
                outs.append(x)
        return tuple(outs)
