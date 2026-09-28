# Dossier validation results

The local checker passed **264/264 checks** with no failures: 131 structure/dependency checks, 69 document/link checks and 64 independent synthetic arithmetic/model checks.

Run `python checks/validate.py`. Exact results are in [checks/results.json](checks/results.json), with compact manually specified examples in [design-examples.json](design-examples.json).

These checks validate this generated dossier and selected examples only. They do not import OpenERP, compile Effect, apply SQL, prove transaction/concurrency behaviour, run a browser, qualify a statutory rule or call a provider. No repository tests or source files were changed.

Source manifests record targeted reads and prior-archive hashes. SHA256SUMS.txt records final file bytes. Passing these checks is not a claim that any of the 25 new workflows is implemented or qualified for a real company.
