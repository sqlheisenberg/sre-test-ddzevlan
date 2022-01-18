# 2 Tornado async network library

Date: 2022-01-17

## Status

Accepted

## Context

We need to choose framework and network library which will ensure high-perfromance, scalability, multi-thread/process in handiling requests. Framework should be good documented and simple to use.

## Decision

We will use Tornado framework and asynchronous networking library. It will provide to us high performances and scalability. It's stable, robust and it's easy to add new business logic. Also it's able to serve many clients with each server thread using event-driven I/O, with process-forking, working C10k problem solution.

Tornado documentation can be found on the following [link](https://www.tornadoweb.org/en/stable/guide/intro.html)

## Consequences

Tornado has a non-blocking paradigm while writing `IOLoop`. This can be an issue for developers since they need to remember to keep the `IOLoop` unblocked while writing code.