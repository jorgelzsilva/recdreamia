# Pragmatic Programming Concepts

This document allows you to explore the concepts of Pragmatic Programming, providing definitions, advantages, risks, and examples of related tools or languages.

## Code Design

### Design by Contract (DbC)
- **Description**: A technique that defines formal contracts (preconditions, postconditions, and invariants) between modules to ensure software correctness. Focuses on clearly defining rights and responsibilities.
- **Main Advantages**: Ensures correctness; helps diagnose problems by 'failing early'; serves as executable documentation; reduces the need for excessive defensive programming.
- **Challenges or Risks**: Requires language support; can impact runtime performance; difficulty in formulating rigorous contracts; should not replace user input validation.
- **Related Language/Tool**: Eiffel, 'deal' library (Python), iContract (Java), Nana (C/C++), Bond (Elixir), D, Ada

### Tracer Bullets
- **Description**: A development style that quickly and visibly connects requirements to an end-to-end functional slice of the final system to get immediate feedback.
- **Main Advantages**: Users see progress early; provides a continuous integration structure; low cost of change due to low inertia; reduces risks early.
- **Challenges or Risks**: Often confused with disposable prototyping; requires the code to be 'for real' (with error handling and documentation) from the start.
- **Related Language/Tool**: Incremental development; Agile Methodologies

### DRY (Don't Repeat Yourself)
- **Description**: A principle that states that every piece of knowledge must have a single, unambiguous, and authoritative representation within a system.
- **Main Advantages**: Facilitates maintenance (changes are made in only one place); avoids logical contradictions and reduces cognitive load and redundant effort.
- **Challenges or Risks**: Risk of confusing code coincidence with knowledge duplication; duplication may be imposed by deadlines or design failures.
- **Related Language/Tool**: Code generators, Metadata, Automation

### Refactoring
- **Description**: The disciplined process of restructuring existing code to improve its internal structure and design without altering its external behavior.
- **Main Advantages**: Fights software entropy; eliminates duplication; improves readability and keeps the code current with new requirements.
- **Challenges or Risks**: Risk of breaking functionality without solid regression tests; time pressure can discourage the practice.
- **Related Language/Tool**: Refactoring Browser (Smalltalk), modern IDEs

### Law of Demeter (LoD)
- **Description**: A set of guidelines (Principle of Least Knowledge) that restricts method calls to directly known objects, aiming to minimize coupling.
- **Main Advantages**: Creates 'shy' code that does not reveal internal details; makes the software more adaptable, robust, and less fragile to changes in third parties.
- **Challenges or Risks**: Can lead to excessive creation of 'wrapper' methods, increasing verbosity and runtime cost.
- **Related Language/Tool**: C++, Java, C#

### Property-Based Testing
- **Description**: A methodology where the computer generates large volumes of random inputs to validate whether certain logical properties or invariants of the software remain true.
- **Main Advantages**: Discovers unforeseen edge cases; validates assumptions comprehensively; serves as living documentation of invariants.
- **Challenges or Risks**: Difficulty in writing effective data generators and complexity in identifying the correct properties to test.
- **Related Language/Tool**: Hypothesis (Python), QuickCheck (Haskell, OCaml, Rust), pytest

### Mixins
- **Description**: Classes that encapsulate reusable behaviors to be 'mixed in' with other classes via multiple inheritance, without forming rigid hierarchies.
- **Main Advantages**: Allows the reuse of isolated functionalities; promotes the separation of concerns; avoids the stiffness of traditional inheritance.
- **Challenges or Risks**: Conflicts in Method Resolution Order (MRO); risks of name collision and implicit dependencies if there is internal state.
- **Related Language/Tool**: Python, Ruby, Django, Swift

### Test-Driven Development (TDD)
- **Description**: A practice where tests are written before functionality, following the 'fail-pass-refactor' cycle to guide the design.
- **Main Advantages**: Ensures test coverage; reduces coupling; helps understand requirements before coding.
- **Challenges or Risks**: Risk of excessive focus on minutiae or code coverage to the detriment of the actual problem solution.
- **Related Language/Tool**: Extreme Programming, ppx_quickcheck (OCaml)

### Multiple Inheritance
- **Description**: A type of inheritance where a class derives functionality and attributes from multiple superclasses simultaneously.
- **Main Advantages**: Allows combining behaviors from multiple sources directly.
- **Challenges or Risks**: Diamond problem (ambiguity in common superclasses); complexity in method resolution (MRO).
- **Related Language/Tool**: Python, C++, Eiffel

### Crash Early
- **Description**: The principle of immediately terminating execution upon detecting an invalid state or contract violation, preventing error propagation.
- **Main Advantages**: Facilitates root cause diagnosis; prevents silent corruption of system data and states.
- **Challenges or Risks**: Inappropriate if critical resources are not released or if there is no fault supervision system.
- **Related Language/Tool**: Erlang, Elixir (supervisors)

### Technical Debt
- **Description**: The cost of future rework caused by choosing a quick/easy solution now instead of a better-structured approach.
- **Main Advantages**: Allows accelerating time to market in critical or highly uncertain situations.
- **Challenges or Risks**: Accumulation of technical 'interest'; degradation of code quality and progressive slowdown in development.
- **Related Language/Tool**: Project Management, DevOps

### Class Invariant
- **Description**: A logical condition that must always be true for all instances of a class in stable states (before and after public methods).
- **Main Advantages**: Ensures internal object consistency and facilitates early detection of state logic errors.
- **Challenges or Risks**: Verbose manual implementation in languages that do not have native support for the concept.
- **Related Language/Tool**: Eiffel, Python (via 'deal' or `invariant`)

### Prototyping
- **Description**: Creation of disposable code aimed at exploring technical risks, testing algorithms, or validating experimental interfaces.
- **Main Advantages**: Mitigates technical risks quickly and promotes learning without compromising the main codebase.
- **Challenges or Risks**: Risk of prototype 'hacks' accidentally being incorporated into the production system.
- **Related Language/Tool**: Not in source

## Complexity

### Big-O Notation
- **Description**: A mathematical tool that describes the upper bound of an algorithm's resource consumption (time or memory) in relation to the growth of the input ( $n$ ).
- **Main Advantages**: Allows estimating scalability and comparing algorithm efficiency objectively before implementation.
- **Challenges or Risks**: Does not reveal the actual execution time (ignores constants); focuses on the worst-case scenario; complexities above $O(n^2)$ quickly become unfeasible.
- **Related Language/Tool**: Search and sort algorithms; Rust

## Architecture

### Actor Model
- **Description**: A concurrent computation model that treats 'actors' as basic units that communicate via asynchronous message passing, without shared state.
- **Main Advantages**: Eliminates the need for locks and race conditions; offers massive scalability and fault tolerance via supervision.
- **Challenges or Risks**: Requires optimization for efficiency; message order is not guaranteed; debugging and tracing messages can be complex.
- **Related Language/Tool**: Erlang, Elixir, Akka (Scala/Java), Nact (JS), Orleans (.NET), Smalltalk

### Orthogonality
- **Description**: The concept of independence where a change in one component does not affect others. Two components are orthogonal if they are decoupled from each other.
- **Main Advantages**: Increases productivity through localized changes; reduces risks by isolating faulty parts; promotes the reuse of independent components.
- **Challenges or Risks**: Misuse of multiple inheritance or global variables can break it; requires constant vigilance to avoid circular dependencies.
- **Related Language/Tool**: Model-View-Controller (MVC), Layers, EJB

### Microservices
- **Description**: An approach that builds applications as a suite of small, independent, and separately deployable services, with their own codebases.
- **Main Advantages**: Decoupling; independent scalability; technological freedom for each service and agility in deployment.
- **Challenges or Risks**: Increased operational complexity; network latency; challenges in distributed debugging and data consistency management.
- **Related Language/Tool**: Docker, Kubernetes, AWS, Google Cloud

### Uniform Access Principle (UAP)
- **Description**: States that all services of a module must be accessed via uniform notation, regardless of whether they are stored fields or computed functions.
- **Main Advantages**: Gives the provider freedom to change the internal implementation without affecting the client's code.
- **Challenges or Risks**: Can hide varied computational costs from the client (e.g., a simple lookup vs. a heavy calculation).
- **Related Language/Tool**: Java (Interfaces/Getters), Eiffel (native)

### ETC (Easier to Change)
- **Description**: A principle that prioritizes flexibility, aiming for the system to be transformable with low cost and risk.
- **Main Advantages**: Fights entropy and allows the software to adapt to uncertain future requirements.
- **Challenges or Risks**: Pressures for immediate deliveries can conflict with flexible design, generating technical debt.
- **Related Language/Tool**: Not in source

## Design Patterns

### Observer Design Pattern
- **Description**: Defines a one-to-many dependency between objects, where a 'subject' automatically notifies all of its 'observers' about state changes.
- **Main Advantages**: Decouples the data object from its views; ensures efficient updates (avoids periodic calls/polling).
- **Challenges or Risks**: Risk of overload if there is an excess of notifications; graph complexity $O(m \cdot n)$ in many-to-many relationships.
- **Related Language/Tool**: Event-driven design; monitoring systems

### Blackboards
- **Description**: A forum where consumers and producers of knowledge anonymously and asynchronously exchange data, completely decoupling the objects.
- **Main Advantages**: Eliminates complex direct interaction APIs; handles unpredictable data orders well; coordinates distributed flows.
- **Challenges or Risks**: Can become confusing with large volumes of data, requiring complex partitioning into zones.
- **Related Language/Tool**: JavaSpaces, T Spaces, Linda

### Visitor Design Pattern
- **Description**: Separates algorithms and operations from the object structure they operate on, allowing new functions to be added without changing the structure classes.
- **Main Advantages**: Obeys the Open/Closed Principle (OCP) for new operations.
- **Challenges or Risks**: Makes it difficult to add new elements to the original structure (violates the structure's OCP).
- **Related Language/Tool**: OO languages; expression operation clusters

### Composite Design Pattern
- **Description**: Composes objects into tree structures to represent whole-part hierarchies, treating individual objects and compositions uniformly.
- **Main Advantages**: Allows clients to use polymorphism to process complex structures simply and uniformly.
- **Challenges or Risks**: Can make the design excessively general by including composition features in 'leaf' objects that should not have them.
- **Related Language/Tool**: Manufacturing systems; window managers

### Singleton Design Pattern
- **Description**: Ensures that a class has only a single instance across the system, providing a global access point.
- **Main Advantages**: Useful for managing limited shared resources or data that must be globally consistent.
- **Challenges or Risks**: Can hide dependencies and complicate testing; risk of multiple instances if the implementation is not thread-safe.
- **Related Language/Tool**: 'once' routines (Eiffel); Print Spoolers

### Reactive Programming and Streams
- **Description**: Treating events as asynchronous data collections, allowing manipulation, filtering, and combination via common APIs.
- **Main Advantages**: Unifies synchronous and asynchronous processing; facilitates the creation of responsive, event-driven systems.
- **Challenges or Risks**: Difficulty in visualizing the complete data flow in highly complex and chained systems.
- **Related Language/Tool**: RxJS, React, Vue.js, ReactiveX

### "Tell, Don't Ask"
- **Description**: The principle of instructing an object what to do instead of requesting its data to make decisions externally.
- **Main Advantages**: Reinforces encapsulation and prevents the creation of 'anemic data objects'.
- **Challenges or Risks**: Can be misapplied to objects that are purely data containers (DTOs) without associated behavior.
- **Related Language/Tool**: Object-Oriented Programming
