# 4. Single process model

Date: 2022-01-17

## Status

Accepted

## Context

Single-process approach is used to handle requests. Tornado also offers more complex, production-grade, c10k optimal solutions with multi-process TCPServer, based on process forking.

## Decision

We will use single-process for the current stage of the project.

## Consequences

For production environment this needs to be changed and we should implement multi-process request handling.