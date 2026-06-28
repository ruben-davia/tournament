# Publishing Notes

The public repository should contain the reusable framework, not private work artifacts.

Keep out of git by default:

- local datasets
- scrape exports
- market snapshots
- generated reports
- simulation runs
- private rules PDFs
- side experiments

Before publishing:

1. run the public tests
2. run the public example
3. scan for secrets and personal data
4. check the public file list

```bash
python -m unittest tests.test_framework tests.test_scoring
python examples/basic_football_pool/run_example.py
git ls-files --others --exclude-standard
```
