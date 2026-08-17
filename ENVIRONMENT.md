# Environment and verification boundary

## Pinned environment

The project requires Python 3.12 and the locked dependencies in
<code>pyproject.toml</code> and <code>uv.lock</code>:

~~~sh
uv sync --frozen
~~~

## Lightweight publication check

The existing publication surface can be checked without rerunning long
training:

~~~sh
uv run python repro/src/publication_gate.py --skip-producers
python3 verify_final.py
~~~

The first command validates the committed theorem, exact-bound, training
boundary, HardNet, source, branch, and stale-state records. The second command
also queries the live GitHub branch set and checks the hash manifest.

## Optional producers

The theorem and exact-bound producers are short CPU checks. The full producer
commands and the optional PyTorch training protocol are documented in the
README and <code>docs/TRAINING_AUDIT.md</code>. Ordinary publication
verification does not rerun the 50,000-epoch or 10,000-epoch training jobs.

## Reproduction boundary

The paper's unpublished matrices, seeds, weights, and official score are
unavailable. A fresh local or remote build of those artifacts is therefore
not part of this dossier, and no finite clean-room substitute is promoted to
paper-wide evidence.
