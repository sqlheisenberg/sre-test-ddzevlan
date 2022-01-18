# 3. Command parsing scheme

Date: 2022-01-17

## Status

Accepted

## Context
Message protocol design
 
## Decision
All messages/commands are of fixed length, if a command identifier/constant does not have enough characters, it's padded 
to expected length with agreed pad-character 'x'
"WHOxx WHERE WHYxx"


## Consequences
Ease of parsing, unpacking received bytes streams from clients, for more complex commands, they would also have a request/message body size in bytes. 
Suggestion for moving forward, enforce a more declarative way of specifiying schemas, for example move to ProtoBuffers.


