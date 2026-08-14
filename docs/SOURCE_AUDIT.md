# Source and provenance audit

## Paper

- **Title:** *CAffNet: Hard Constraint-Affine Neural Networks*
- **Authors:** Yang Zhao, Jungeun Lee, Jeong hwan Jeon, Sze Zheng Yong
- **arXiv:** [2605.24437](https://arxiv.org/abs/2605.24437)
- **OpenReview:** [20hdQQQrA4](https://openreview.net/forum?id=20hdQQQrA4)
- **Primary HTML used for section-level reading:**
  [ar5iv HTML](https://ar5iv.labs.arxiv.org/html/2605.24437)
- **Audited source PDF SHA-256:**
  `33db803823608bdb76db20732f0a3a20aef32c5f4e22f4c4b148a2b7b6da9520`

The paper metadata and equations were read from the public arXiv/OpenReview
record. The hash identifies the source PDF retained by the earlier audit; it is
included so a future audit can detect a different source revision.

## Official-code boundary

No official CAffNet implementation, benchmark matrices, training seeds,
trained weights, or official score artifact is treated as available here. The
dimension-matched neural run therefore reports feasibility but does not claim
the paper's Table 3 objective values. The public artifact bucket used by the
earlier campaign is recorded in `sources.json`, but it is not treated as an
official author release.

## HardNet comparison source

The supplemental control uses only the named HardNet-Aff enforcement formula,
not a claim that HardNet is the CAffNet implementation:

- upstream repository: `azizanlab/hardnet`
- pinned revision: `4f3ebe496c4081489c486e2711f25697a4c312fa`
- transcribed file: `hardnet_aff.py`
- pinned file SHA-256: `7fb545ba991719d89cca1553bd4aef824a416ea2ad07cf97e54565c405586f1b`

The audit transcribes the paper's velocity-controlled unicycle task and gives
both methods the same zero learned correction. This isolates enforcement-layer
behavior and deliberately excludes trained-weight and goal-arrival claims.

## Clean-room decisions

- Proofs are implemented independently in `repro/src/theorem_certificates.py`.
- Raw generated outputs remain alongside compact summaries under `evidence/`.
- Historical Trackio state and the root logbook are not part of the publication
  surface; they are ignored or removed so stale verdicts cannot be mistaken for
  current evidence.
- Every claim has a named source file, output artifact, interpretation, and
  limitation in [`CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md).
