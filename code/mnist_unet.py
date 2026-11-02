"""A small time-conditioned U-Net for 28x28 images, used in the Week 4 and Week 5 notebooks.

The network takes a noisy image x at forward OU time tau (and optionally a class label) and predicts the
noise Z in x = exp(-tau) x0 + sigma_tau Z. The score is then -prediction / sigma_tau (Tweedie's formula).
"""
import math
import torch
from torch import nn
import torch.nn.functional as F


def sinusoidal_embedding(t, dim):
    half = dim // 2
    freqs = torch.exp(-math.log(1000.0) * torch.arange(half, device=t.device) / half)
    args = t[:, None] * freqs[None] * 100.0
    return torch.cat([torch.sin(args), torch.cos(args)], dim=1)


class ResBlock(nn.Module):
    def __init__(self, c_in, c_out, emb_dim):
        super().__init__()
        self.norm1 = nn.GroupNorm(8, c_in)
        self.conv1 = nn.Conv2d(c_in, c_out, 3, padding=1)
        self.emb = nn.Linear(emb_dim, c_out)
        self.norm2 = nn.GroupNorm(8, c_out)
        self.conv2 = nn.Conv2d(c_out, c_out, 3, padding=1)
        self.skip = nn.Conv2d(c_in, c_out, 1) if c_in != c_out else nn.Identity()

    def forward(self, x, emb):
        h = self.conv1(F.silu(self.norm1(x)))
        h = h + self.emb(emb)[:, :, None, None]
        h = self.conv2(F.silu(self.norm2(h)))
        return h + self.skip(x)


class UNet(nn.Module):
    """U-Net on 28x28 images with resolutions 28, 14, 7. If num_classes is given, the label index
    num_classes stands for the null label of classifier-free guidance."""

    def __init__(self, base=32, emb_dim=128, num_classes=None):
        super().__init__()
        self.emb_dim = emb_dim
        self.time_mlp = nn.Sequential(nn.Linear(emb_dim, emb_dim), nn.SiLU(), nn.Linear(emb_dim, emb_dim))
        self.label_emb = nn.Embedding(num_classes + 1, emb_dim) if num_classes is not None else None
        c1, c2, c3 = base, 2 * base, 4 * base
        self.inp = nn.Conv2d(1, c1, 3, padding=1)
        self.down1 = ResBlock(c1, c1, emb_dim)
        self.down2 = ResBlock(c1, c2, emb_dim)
        self.down3 = ResBlock(c2, c3, emb_dim)
        self.mid = ResBlock(c3, c3, emb_dim)
        self.up3 = ResBlock(c3 + c3, c2, emb_dim)
        self.up2 = ResBlock(c2 + c2, c1, emb_dim)
        self.up1 = ResBlock(c1 + c1, c1, emb_dim)
        self.out = nn.Sequential(nn.GroupNorm(8, c1), nn.SiLU(), nn.Conv2d(c1, 1, 3, padding=1))

    def forward(self, x, tau, labels=None):
        emb = self.time_mlp(sinusoidal_embedding(tau, self.emb_dim))
        if self.label_emb is not None:
            emb = emb + self.label_emb(labels)
        h1 = self.down1(self.inp(x), emb)                       # 28x28
        h2 = self.down2(F.avg_pool2d(h1, 2), emb)              # 14x14
        h3 = self.down3(F.avg_pool2d(h2, 2), emb)              # 7x7
        h = self.mid(h3, emb)
        h = self.up3(torch.cat([h, h3], 1), emb)
        h = self.up2(torch.cat([F.interpolate(h, scale_factor=2), h2], 1), emb)
        h = self.up1(torch.cat([F.interpolate(h, scale_factor=2), h1], 1), emb)
        return self.out(h)
