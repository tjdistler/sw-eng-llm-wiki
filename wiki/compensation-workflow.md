# Compensation Workflow

**Summary**: A workflow that tolerates partial failure and resolves the consequences *after the fact* with business-level remedies, rather than rolling the transaction back. Named by Bellemare as a pragmatic alternative to strict distributed-transaction / [[saga]] semantics when reversal would hurt the customer or the business more than completing best-effort would. Common in ticketing, inventory, and travel systems.

**Sources**: `raw/building-event-driven-microservices/chapter-08-building-workflows-with-microservices.md`

**Last updated**: 2026-04-17

---

## The idea

Not all workflows need to be perfectly reversible. Many business processes have "unforeseen issues that can arise" and in many cases "you might just have to do your best to complete it." When something goes wrong, there are actions you can take *after the fact* to remedy the situation (source: chapter-08-building-workflows-with-microservices.md).

A strict transactional approach (see [[saga]] and [[distributed-transactions]]) would require every step to have a compensating rollback action and would unwind the entire transaction on any failure. A compensating *workflow* does something different — it completes what it can and then invokes a business-level remediation path for the pieces that failed.

## Bellemare's worked example

A retailer accepts an order and charges the customer. Settling payments and checking inventory later, the retailer discovers it does not have enough stock to fulfill the order (source: chapter-08-building-workflows-with-microservices.md).

- **Strict-transaction path:** refund the payment, cancel the order, tell the customer the item is out of stock. Technically correct. Poor customer experience; undermines trust.
- **Compensation-workflow path:** order replenishment stock, notify the customer of the delay, offer a discount code for the next purchase. Give the customer the option to cancel if they don't want to wait.

The second path is not a rollback — the order stays placed, the payment stays charged, and the system continues forward. The business absorbs the operational consequences with a remedial action driven by its customer-satisfaction policy.

## Where it fits

Bellemare names the domains where compensation workflows are common (source: chapter-08-building-workflows-with-microservices.md):

- **Ticketing** (sports, concerts, theatres) — oversold tickets trigger compensation (refunds, upgrades, future credits) rather than preventing the sale in the first place.
- **Airlines and travel agents** — overbooking with post-hoc vouchers, rebooking, hotel nights. A well-known industry pattern.
- **Physical inventory / retail** — orders accepted against predicted stock; shortfalls handled by replenishment + apology discounts rather than refunds.

## When to use compensation vs saga

| | Saga (strict rollback) | Compensation workflow |
|---|---|---|
| Is a rollback operationally possible? | Yes | Maybe, but undesirable |
| Is a rollback business-appropriate? | Yes | No — hurts customer experience or trust |
| Does failure have a remediation policy? | N/A | Yes — the business has a defined response |
| Who executes the remedy? | The workers (compensating transactions) | Often non-technical parts of the business (customer service, replenishment, fulfillment ops) |

Compensation workflows are *not always possible* — some operations really do need to be atomic and reversible. But when the business already has a customer-facing policy for "what to do when this goes wrong," a compensation workflow is often simpler and kinder than forcing an all-or-nothing saga.

## Relationship to sagas

Both patterns handle the same underlying problem (partial failure in a multi-step workflow) but with different philosophies:

- A **[[saga]]** prefers *technical consistency*: every step has a compensating undo; on failure the system reverts to its prior state.
- A **compensation workflow** prefers *business continuity*: complete what can be completed, remediate what cannot. The system may end up in a state that the *initial intent* did not describe, but that the business considers acceptable and recoverable.

In practice the two are composable. A saga can include a step whose "failure" is handled by a compensation workflow rather than by a rollback. And a compensation workflow can use a mini-saga internally for steps that really do need to be undone. Bellemare's framing makes the distinction explicit so that teams do not reflexively reach for strict rollback when the business would prefer best-effort plus remediation.

## Relationship to forward recovery

Compensation workflows are closely related to the **forward recovery** mode of the original 1987 Saga paper (see [[saga]]). Forward recovery picks up from the failure point and keeps going; compensation workflows do the same, but with an explicit business-policy remediation rather than a technical retry. The common thread: failure does not always mean "undo everything and pretend nothing happened."

## Related pages

- [[saga]]
- [[distributed-transactions]]
- [[workflows-in-edm]]
- [[event-driven-microservices]]
- [[idempotence]]
- [[eventual-consistency]]
