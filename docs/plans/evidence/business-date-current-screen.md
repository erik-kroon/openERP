# Bank period receipt qualification.

Remote main7e9d89e CI37140195363 passed validation and356/357native tests. The business-date browser case failed because its global bank request list ended with the overview window ending2026-10-03 while the Accounts assertion expected the selected fiscal window ending2026-12-31. The source bankWorkspaceParams independently selects the owned fiscal period when URL dates are absent. The listener includes requests from every bank-workspace consumer, so its last entry is not qualified to the current screen or a deliberate Accounts action. This source finding explains why the observation is inadequate; the precise request/cache timing remains unproved.

Before correction, retain obligations. Browser clock skew cannot alter the overview's server-owned business date. Accounts default From/To must match the owned fiscal period; an explicit March range must remain exact. A normal accessible Refresh action must produce a successful public bank workspace response for that exact selected range. Capture the response alongside the visible inputs, rather than treating the last global request as current-screen evidence. No timeout, expected dates, server policy or production source changes are authorized by this test correction.

Local verification is pending. Original remote native.json/native.log retained under /tmp/main-7e9d89e-evidence.
