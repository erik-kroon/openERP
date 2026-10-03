# Document library integration on main.

P05 was rebased without conflict onto verified template parent `a1b33d3`. The authorized missing-original helper was already upstream and its duplicate commit was dropped. Newer P01 navigation cases remained intact.

Integrated full and current primary strict checks passed. The combined library/browser/navigation cohort retained eight passing cases at stable source `0c3f27df601c8a8d263828a8e7cfa8fb66378df8b8eb53308c3d78a948f7a0cc`. The sole failed bank navigation case still expected the old generic voucher close label after the intentional owner-aware label change. Its literal destination/filter/unknown-owner expectations were preserved; only the accessible label now matches Back to work for bank ownership.

Fast/full/current-primary strict checks passed after that test correction. The bounded bank-owner case passed1/1 in26.11s at stable source `6365503c9ba2ed600794252550b3e2b6baa330653dc83c34c110f885428ed09d`; four unrelated cases were skipped. Thus all nine selected cases passed across the retained cohorts, not a claimed single nine-test final run.

The integrated browser verifies searchable metadata, retained historical owners, archive cursor/filter/selection/focus, keyboard320px navigation and honest missing-original recovery. The prior ordinary filename and owner-search performance receipts remain in [the checkpoint](remainder-checkpoint.md). No performance source changed during integration. Native200% zoom and Paper visual design are unobserved.

The bounded bank navigation run observed one ancillary HTTP500 for bank-connector-feeds while visiting its existing setup owner. That owner was not changed by P05; the cause remains unproved and no connector-feed success is claimed by this slice. Earlier transient module504 diagnostics did not cause the integrated navigation failure; the actual failed assertion was the old close-label lookup.

Repeat the bounded regression with `OPENERP_E2E_ARTIFACTS=test-results/product-P05-bank-owner-final bun run test:e2e apps/api/tests/navigation-context.e2e.test.ts -t 'bank voucher links'`. All fixtures were synthetic disposable local systems. Migration0064 was qualified locally, not deployed.
