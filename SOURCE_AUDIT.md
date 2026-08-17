# Source and provenance audit

## Paper identity

- Title: **CAffNet: Hard Constraint-Affine Neural Networks**
- Authors: Yang Zhao, Jungeun Lee, Jeong hwan Jeon, and Sze Zheng Yong
- arXiv: [2605.24437](https://arxiv.org/abs/2605.24437)
- OpenReview: [20hdQQQrA4](https://openreview.net/forum?id=20hdQQQrA4)
- Former repository: <code>icml26-repro-20hdQQQrA4-caffnet-constraint-affine</code>
- Current repository: <code>icml26-caffnet-hard-constraint-affine</code>

The audited arXiv v1 source PDF is represented by SHA-256
<code>33db803823608bdb76db20732f0a3a20aef32c5f4e22f4c4b148a2b7b6da9520</code>
in <code>sources.json</code>. The PDF itself is not silently reconstructed
from a different revision.

## Official-code boundary

No official CAffNet implementation, benchmark matrices, training seeds,
trained weights, or official score artifact is treated as available. The
paper-spec one-dimensional protocol and the dimension-matched clean-room
instance are therefore labeled separately; the latter does not reproduce
Table 3 objectives.

## Supplemental HardNet source

The named HardNet-Aff enforcement formula is pinned independently:

- repository: <code>azizanlab/hardnet</code>
- revision: <code>4f3ebe496c4081489c486e2711f25697a4c312fa</code>
- file: <code>hardnet_aff.py</code>
- file SHA-256: <code>7fb545ba991719d89cca1553bd4aef824a416ea2ad07cf97e54565c405586f1b</code>

The control gives both methods the same zero learned correction. It isolates
the enforcement layer and does not present HardNet as the CAffNet source.

## Historical campaign artifacts

The public bucket and historical Space are recorded in
<code>sources.json</code> for provenance only. They are not official author
releases and are not treated as current evaluator scores.

## Clean-room boundary

Proof certificates and neural controls live in <code>repro/</code> and
<code>outputs/</code>. The old Trackio/logbook state was removed from the
publication surface. The historical C2 qualification remains inspectable on
<code>experiment/joint-optimization-control</code>.
