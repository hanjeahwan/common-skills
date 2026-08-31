---
id: P001
status: implemented
---

# Increase request timeout

## Summary

Increase the API timeout from 30 to 45 seconds.

## Problem

Requests need more processing time.

## Scope

The API request timeout.

## Non-goals

No retry changes.

## Proposal

Set the timeout to 45 seconds.

## Migration

Update the API contract.

## Verification

Verify requests may run for 45 seconds.

## Outcome

The timeout change was implemented.
