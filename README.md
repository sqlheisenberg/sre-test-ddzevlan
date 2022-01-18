# blockchain_tcp_service (SRE Proficiency Test - Part 1)

Non-critical API service (~90% SLO) used for existing **Blockchain.com** internal services. 
Service is accepting commands on TCP port composed of ASCII strings.
More info about the task can be foound here: [doc/sre_proficiency_test.pdf](doc/sre_proficiency_test.pdf)
**The following commands are accepted:**

`WHO` - outputs the total number of clients connected;  
`WHERE` - outputst heidoftheserver (a unique identifier);   
`WHY` - output the string 42;

## ADRs
Project decisions are documented through Architectual Decision Records (ADRs) and can be found inside [doc/adr](doc/adr).  
To generate and add new files inside our ADR log we are using [adr-tools](https://pypi.org/project/adr-tools-python/)

## Coding styles
We are using [PEP 8 — the Style Guide for Python Code](https://pep8.org/)
To verify code style we are using [pylint](https://pylint.org/).  

**NOTE:** Following pylint error messages are ignored:  

**C0014 missing-module-docstring** - Missing module docstring Used when a module has no docstring.Empty modules do not require a docstring.

**C0115 missing-class-docstring** - Missing class docstring Used when a class has no docstring.Even an empty class must have a docstring.  

**C0116 missing-function-docstring (C0116)** - Missing function or method docstring Used when a function or method has no docstring.Some special methods like __init__ do not require a docstring.  

## Required changes for production ready system
Before moving this service into the **production environment** pay attention on decisions made durring Part 1 of developing this service which should be improved to make this service production ready.

- Implent message protocol desing (ProtoBuffers)
  [doc/adr/0003-command-parsing-scheme](doc/adr/0003-command-parsing-scheme.md)
- Implement multi-threading
  [doc/adr/0004-single-process-model](doc/adr/0004-single-process-model.md)  

**Additional notes for moving into production:**

- As part of message protocol desing implement heartbeat/KeepAlive connection requests. 
- Implement proxy in front of our service with client certificates to handle secure connection and SSL offloading. 
- Depending on the team choice, an appropriate DI lib should be used.
- Client implementations considerations for different programing languages. Code samples how to implement client for our server.

# System Design (Part 2)
- Target SLO 99.95%  
> Implement APM, ensure monitoring of our system, use Docker to manage/replace/spin-up new instances of the service. Deployments without downtime. We need to ensure that established connections are alive durring deployments, moving connections from one thread to another?! We can use proxy to manage upstreaming.

- How to acchive state replication and fault tolerance
> We need caching database (ie. Redis, Memcache ...), ensure HA, proxy to ensure upstreaming like menitoned above with increased gateway timeout so that we have enough time to replace containers without breaking requests.  
- CAP theoreme - do you need more info from the engineering / product teams?
> Yes. How "important" is response which client is getting back, what are the dependencies? I.e. if we have payment system depending on number of connected clients or security (potentialy dangerous data) then we need to persue Consistency in front of Availiblity. 

# Points for duscussion afterwads
- What counsiderations would you have if the SLO were 99.9999%?
- What changes would you encurage the product team to make in their requirements?  
- How does this service fit into larger microservice ecosystem? What tooling will it require to make it useful?
