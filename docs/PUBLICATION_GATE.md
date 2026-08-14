# Publication gate

The gate is a final hygiene and evidence check for the canonical repository
surface. It is not a substitute for the proof or the focused producers.

Run:

```bash
uv run python repro/src/publication_gate.py --skip-producers
```

The command writes [`outputs/publication_gate.json`](../outputs/publication_gate.json)
and checks:

- the clean final project slug and paper identity;
- the required README, status, claim, source, branch, and citation material;
- valid C1/C2/C3 theorem certificates;
- exact-bound and HardNet audit outputs;
- compact evidence summaries and the absence of tracked `logbook.json`,
  `.trackio`, or old repository identity files;
- the exact MachineLearning-Nerd attribution in the reachable Git history.

Without `--skip-producers`, the gate reruns the fast theorem and exact-bound
producers before checking the artifacts. It does not launch the long PyTorch
training campaign.

The gate is intentionally fail-closed: unavailable official matrices,
checkpoints, or scores cannot be silently converted into a successful paper-wide
reproduction claim.
