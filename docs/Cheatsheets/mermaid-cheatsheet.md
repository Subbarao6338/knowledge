<!-- {% raw %} -->
# Mermaid Charts Cheatsheet (.mmd)

Mermaid diagrams are defined in plain text and rendered as SVG. Files use the `.mmd` extension standalone, or are embedded in fenced ` ```mermaid ` code blocks in Markdown (GitHub, GitLab, Notion, and most modern renderers support this natively).

## Flowcharts

```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Do Thing]
    B -->|No| D[Do Other Thing]
    C --> E[End]
    D --> E
```

**Direction keywords:** `TD`/`TB` (top-down), `BT` (bottom-top), `LR` (left-right), `RL` (right-left).

**Node shapes:**
```mermaid
graph LR
    A[Rectangle]
    B(Rounded)
    C([Stadium])
    D[[Subroutine]]
    E[(Database)]
    F((Circle))
    G{Diamond/Decision}
    H{{Hexagon}}
    I[/Parallelogram/]
    J[\Parallelogram alt\]
    K[/Trapezoid\]
```

**Link/arrow types:**
```mermaid
graph LR
    A --> B
    A --- B
    A -.-> B
    A ==> B
    A -->|labeled| B
    A -.->|dotted labeled| B
    A ~~~ B
```

**Subgraphs:**
```mermaid
graph TD
    subgraph Cluster1 [My Group]
        A --> B
    end
    subgraph Cluster2
        C --> D
    end
    B --> C
```

**Styling nodes:**
```mermaid
graph TD
    A[Start] --> B[End]
    style A fill:#f9f,stroke:#333,stroke-width:2px
    classDef important fill:#f96,stroke:#333
    class B important
```

## Sequence Diagrams

```mermaid
sequenceDiagram
    participant User
    participant API
    participant DB

    User->>API: POST /login
    API->>DB: query credentials
    DB-->>API: user record
    API-->>User: 200 OK + token

    Note over User,API: Session established

    alt invalid credentials
        API-->>User: 401 Unauthorized
    else valid credentials
        API-->>User: 200 OK
    end

    loop every 30s
        User->>API: heartbeat
    end

    par parallel calls
        User->>API: request A
    and
        User->>API: request B
    end

    activate API
    User->>API: another call
    deactivate API
```

**Arrow types:** `->>` (solid, async), `-->>` (dashed, response), `->` (solid, no arrowhead), `-x` (async lost message).

## Class Diagrams

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        -bool isAlive
        +makeSound() void
        +eat(food) void
    }

    class Dog {
        +bark() void
    }

    class Cat {
        +meow() void
    }

    Animal <|-- Dog : inherits
    Animal <|-- Cat : inherits
    Animal "1" --> "many" Food : eats

    class Shape {
        <<interface>>
        +area() float
    }
```

**Relationship types:** `<|--` (inheritance), `*--` (composition), `o--` (aggregation), `-->` (association), `..>` (dependency), `..|>` (realization/interface).

## Entity Relationship Diagrams

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    CUSTOMER {
        int id PK
        string name
        string email
    }
    ORDER {
        int id PK
        int customer_id FK
        date created_at
    }
    LINE_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
    }
```

**Cardinality notation:** `||--||` (one-to-one), `||--o{` (one-to-many), `}o--o{` (many-to-many), `||--|{` (one-to-one-or-many).

## State Diagrams

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing : start
    Processing --> Success : complete
    Processing --> Failed : error
    Success --> [*]
    Failed --> Idle : retry

    state Processing {
        [*] --> Validating
        Validating --> Executing
        Executing --> [*]
    }
```

## Gantt Charts

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    axisFormat %m/%d

    section Design
    Requirements       :done, des1, 2026-07-01, 5d
    Wireframes          :active, des2, after des1, 3d

    section Development
    Backend                :dev1, after des2, 10d
    Frontend                 :dev2, after des2, 8d

    section Testing
    QA                          :crit, test1, after dev1, 5d
```

## Pie Charts

```mermaid
pie title Cloud Spend by Provider
    "AWS" : 45
    "GCP" : 35
    "Azure" : 20
```

## Git Graphs

```mermaid
gitGraph
    commit id: "init"
    branch feature
    checkout feature
    commit id: "add feature"
    commit id: "fix bug"
    checkout main
    merge feature
    commit id: "release"
```

## Mindmaps

```mermaid
mindmap
  root((FinOps))
    Cost Visibility
      Dashboards
      Tagging
    Optimization
      Rightsizing
      Reserved Instances
    Governance
      Budgets
      Alerts
```

## Journey Diagrams (user experience mapping)

```mermaid
journey
    title User Signup Flow
    section Discovery
      Visit homepage: 5: User
      Click signup: 4: User
    section Signup
      Fill form: 3: User
      Verify email: 2: User
    section Onboarding
      Complete tutorial: 4: User
```

## Quadrant Charts

```mermaid
quadrantChart
    title Effort vs Impact
    x-axis Low Effort --> High Effort
    y-axis Low Impact --> High Impact
    quadrant-1 Quick Wins
    quadrant-2 Major Projects
    quadrant-3 Fill-ins
    quadrant-4 Thankless Tasks
    Task A: [0.3, 0.8]
    Task B: [0.7, 0.6]
```

## Timeline

```mermaid
timeline
    title Product Roadmap
    2026 Q1 : Planning : Research
    2026 Q2 : MVP Launch
    2026 Q3 : Feature Expansion
    2026 Q4 : Scale
```

## Comments & Config

```mermaid
%% This is a comment, ignored by the renderer
graph TD
    A --> B
```

```mermaid
%%{init: {'theme': 'dark', 'themeVariables': {'primaryColor': '#ff0000'}}}%%
graph TD
    A --> B
```

## Rendering Options

```bash
# CLI (mermaid-cli / mmdc)
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.mmd -o diagram.svg
mmdc -i diagram.mmd -o diagram.png -theme dark

# In Markdown, most modern renderers auto-render fenced blocks:
```

````markdown
```mermaid
graph TD
    A --> B
```
````

## Common Gotchas

- Node IDs must be consistent — `A[Start]` and later just `A` refer to the same node; redefining `A[...]` again with different label text elsewhere can cause unexpected duplicate rendering in some diagram types.
- Special characters in labels (parentheses, quotes) can break parsing — wrap the label in quotes: `A["Node (with parens)"]`.
- Diagram type keyword (`graph`, `sequenceDiagram`, `classDiagram`, etc.) must be the very first line — no blank lines or comments before it.
- Not all renderers support every diagram type or the newest syntax (`stateDiagram-v2` vs `stateDiagram`, `quadrantChart`, `timeline`) — check what your target platform (GitHub, GitLab, Notion, VS Code extension) actually supports before relying on newer features.

<!-- {% endraw %} -->
