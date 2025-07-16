# KoinToss System Architecture Diagrams

This document contains comprehensive diagrams showing the architecture, flow, and components of the KoinToss dual-personality crypto chatbot system.

## 1. System Architecture Diagram

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Embeddable JavaScript Widget]
        B[Direct API Integration]
        C[Streamlit Web Interface]
    end
    
    subgraph "API Gateway Layer"
        D[Enhanced FastAPI Server<br/>enhanced_kointoss_api_server.py]
        D --> D1[REST Endpoints]
        D --> D2[WebSocket Support]
        D --> D3[Session Management]
        D --> D4[Rate Limiting]
        D --> D5[CORS Protection]
    end
    
    subgraph "Core Bot Engine"
        E[Dual Personality Chatbot<br/>improved_dual_personality_chatbot.py]
        E --> F[Normal Personality<br/>PureNormalTrainer]
        E --> G[SubZero Personality<br/>PureSubZeroTrainer]
    end
    
    subgraph "Learning & Training Layer"
        H[Advanced Autonomous Trainer<br/>advanced_autonomous_trainer.py]
        I[Dual Personality Intensive Trainer<br/>dual_personality_intensive_trainer.py]
        J[Training Monitor<br/>training_monitor.py]
        K[Training Orchestrator<br/>training_orchestrator.py]
    end
    
    subgraph "Data Integration Layer"
        L[CoinGecko API<br/>Market Data]
        M[News Sources<br/>Sentiment Analysis]
        N[Training Datasets<br/>JSON Files]
        O[User Feedback<br/>Real-time Data]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
    E --> H
    E --> I
    H --> J
    I --> J
    J --> K
    E --> L
    E --> M
    H --> N
    I --> O
```

## 2. Request Flow Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant W as Widget/API
    participant F as FastAPI Server
    participant C as Chatbot Engine
    participant T as Trainer
    participant E as External APIs
    
    U->>W: Send Message
    W->>F: POST /chat
    F->>F: Validate & Rate Limit
    F->>C: Process Message
    C->>T: Route to Personality
    T->>T: Generate Response
    T->>E: Fetch Market Data (if needed)
    E-->>T: Return Data
    T-->>C: Return Response
    C->>C: Log for Training
    C-->>F: Return Processed Response
    F-->>W: JSON Response
    W-->>U: Display Response
    
    Note over C,T: Autonomous training runs<br/>in background continuously
```

## 3. Dual Personality Architecture

```mermaid
graph LR
    subgraph "Message Processing"
        A[User Input] --> B[Message Router]
    end
    
    subgraph "Personality Selection"
        B --> C{Current Personality?}
        C -->|Normal| D[Normal Trainer]
        C -->|SubZero| E[SubZero Trainer]
    end
    
    subgraph "Normal Personality"
        D --> D1[Professional Tone]
        D --> D2[Educational Focus]
        D --> D3[Risk Awareness]
        D --> D4[Beginner Friendly]
    end
    
    subgraph "SubZero Personality"
        E --> E1[Crypto Native Slang]
        E --> E2[Meme References]
        E --> E3[Bold Predictions]
        E --> E4[Community Insights]
    end
    
    subgraph "Response Generation"
        D1 --> F[Context Analysis]
        D2 --> F
        D3 --> F
        D4 --> F
        E1 --> G[Character Consistency]
        E2 --> G
        E3 --> G
        E4 --> G
        F --> H[Response Output]
        G --> H
    end
    
    H --> I[Learning System]
    I --> J[Quality Assessment]
    J --> K[Training Data Update]
```

## 4. Training System Flow

```mermaid
flowchart TD
    A[Autonomous Training Start] --> B[Market Data Collection]
    B --> C[Generate Training Scenarios]
    C --> D[Test Both Personalities]
    D --> E[Quality Evaluation]
    E --> F{Quality Score > Threshold?}
    F -->|Yes| G[Update Training Data]
    F -->|No| H[Generate Alternative Response]
    H --> E
    G --> I[Performance Metrics Update]
    I --> J[Training Analytics]
    J --> K{Continue Training?}
    K -->|Yes| B
    K -->|No| L[Training Session Complete]
    
    subgraph "Background Processes"
        M[Real-time Market Monitoring]
        N[User Interaction Logging]
        O[Pattern Recognition]
    end
    
    M --> B
    N --> C
    O --> E
```

## 5. API Endpoint Structure

```mermaid
graph TB
    subgraph "Chat Endpoints"
        A1[POST /chat<br/>Send message to chatbot]
        A2[POST /chat/personality<br/>Switch personality mode]
        A3[GET /chat/history/{session_id}<br/>Retrieve conversation history]
    end
    
    subgraph "WebSocket Endpoints"
        B1[WS /ws/{session_id}<br/>Real-time chat connection]
    end
    
    subgraph "Management Endpoints"
        C1[GET /health<br/>Health check and system status]
        C2[GET /metrics<br/>Performance and usage metrics]
        C3[POST /admin/training/start<br/>Start autonomous training]
        C4[GET /admin/sessions<br/>Active session management]
    end
    
    subgraph "Widget Endpoints"
        D1[GET /widget<br/>Embeddable widget HTML]
        D2[GET /static/kointoss-widget.js<br/>Widget JavaScript]
        D3[GET /widget/config<br/>Widget configuration]
    end
    
    subgraph "Core Features"
        E[Session Management]
        F[Rate Limiting]
        G[CORS Protection]
        H[Input Validation]
    end
    
    A1 --> E
    A2 --> E
    A3 --> E
    B1 --> E
    A1 --> F
    B1 --> F
    A1 --> G
    B1 --> G
    A1 --> H
    A2 --> H
```

## 6. Data Flow Architecture

```mermaid
graph TD
    subgraph "Input Sources"
        A[User Messages]
        B[Market Data APIs]
        C[News Sources]
        D[Training Datasets]
    end
    
    subgraph "Processing Layer"
        E[Message Preprocessor]
        F[Context Analyzer]
        G[Personality Router]
        H[Response Generator]
    end
    
    subgraph "Knowledge Base"
        I[Crypto Knowledge DB]
        J[Conversation History]
        K[Market Context]
        L[User Preferences]
    end
    
    subgraph "Output Layer"
        M[Response Formatter]
        N[Learning Logger]
        O[Metrics Collector]
        P[User Interface]
    end
    
    A --> E
    B --> F
    C --> F
    D --> I
    
    E --> G
    F --> G
    G --> H
    
    I --> H
    J --> H
    K --> H
    L --> H
    
    H --> M
    H --> N
    H --> O
    M --> P
    N --> J
    O --> L
```

## 7. Deployment Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        A[Local Development<br/>Python 3.8+]
        B[Testing Suite<br/>Pytest, Integration Tests]
        C[Code Quality<br/>Black, Flake8, MyPy]
    end
    
    subgraph "Containerization"
        D[Docker Container<br/>Dockerfile]
        E[Docker Compose<br/>Multi-service setup]
        F[Environment Variables<br/>.env configuration]
    end
    
    subgraph "Cloud Deployment"
        G[AWS ECS/Fargate]
        H[Google Cloud Run]
        I[Microsoft Azure]
        J[Heroku/Railway]
    end
    
    subgraph "Production Services"
        K[Load Balancer<br/>Nginx/ALB]
        L[SSL Termination<br/>Let's Encrypt]
        M[Monitoring<br/>Health Checks]
        N[Logging<br/>Centralized Logs]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
    E --> F
    F --> G
    F --> H
    F --> I
    F --> J
    G --> K
    H --> K
    I --> K
    J --> K
    K --> L
    K --> M
    K --> N
```

## 8. Security Architecture

```mermaid
graph TB
    subgraph "Input Security"
        A[Rate Limiting<br/>60 req/min default]
        B[Input Sanitization<br/>XSS protection]
        C[Request Validation<br/>Pydantic models]
    end
    
    subgraph "Authentication & Authorization"
        D[Session Management<br/>UUID-based sessions]
        E[API Key Authentication<br/>Optional]
        F[CORS Configuration<br/>Domain restrictions]
    end
    
    subgraph "Data Protection"
        G[PII Detection<br/>Regex patterns]
        H[Conversation Encryption<br/>At rest & transit]
        I[Session Timeout<br/>1 hour default]
    end
    
    subgraph "Infrastructure Security"
        J[HTTPS Enforcement<br/>Production only]
        K[Environment Variables<br/>Secret management]
        L[Dependency Scanning<br/>Security updates]
    end
    
    subgraph "Monitoring & Alerts"
        M[Anomaly Detection<br/>Unusual patterns]
        N[Security Logging<br/>Audit trails]
        O[Incident Response<br/>Automated alerts]
    end
    
    A --> D
    B --> D
    C --> D
    D --> G
    E --> G
    F --> G
    G --> J
    H --> J
    I --> J
    J --> M
    K --> M
    L --> M
    M --> N
    N --> O
```

## 9. Performance Architecture

```mermaid
graph TB
    subgraph "Response Optimization"
        A[Async Operations<br/>FastAPI/Asyncio]
        B[Connection Pooling<br/>HTTP clients]
        C[Request Batching<br/>External APIs]
    end
    
    subgraph "Caching Strategy"
        D[In-Memory Cache<br/>LRU Cache]
        E[Redis Cache<br/>Session & responses]
        F[Response Memoization<br/>Similar queries]
    end
    
    subgraph "Database Optimization"
        G[Conversation Indexing<br/>Fast retrieval]
        H[Training Data Compression<br/>Storage efficiency]
        I[Query Optimization<br/>Vector operations]
    end
    
    subgraph "Monitoring & Analytics"
        J[Response Time Tracking<br/>Performance metrics]
        K[Resource Monitoring<br/>CPU, Memory, Disk]
        L[Load Analysis<br/>Traffic patterns]
    end
    
    A --> D
    B --> E
    C --> F
    D --> G
    E --> G
    F --> H
    G --> I
    H --> J
    I --> J
    J --> K
    K --> L
```

## 10. Use Case Diagram

```mermaid
graph TB
    subgraph "User Roles"
        A[General User]
        B[Crypto Enthusiast]
        C[Developer]
        D[System Administrator]
    end
    
    subgraph "Primary Use Cases"
        E[Chat with Bot]
        F[Switch Personalities]
        G[Get Market Data]
        H[Receive News Updates]
    end
    
    subgraph "Advanced Use Cases"
        I[Embed Widget]
        J[API Integration]
        K[Monitor Performance]
        L[Manage Training]
    end
    
    subgraph "Administrative Use Cases"
        M[Configure System]
        N[View Analytics]
        O[Manage Sessions]
        P[Deploy Updates]
    end
    
    A --> E
    A --> F
    A --> G
    A --> H
    
    B --> E
    B --> F
    B --> G
    B --> H
    
    C --> I
    C --> J
    C --> K
    
    D --> L
    D --> M
    D --> N
    D --> O
    D --> P
```

## 11. Error Handling Flow

```mermaid
flowchart TD
    A[User Request] --> B{Input Valid?}
    B -->|No| C[Validation Error]
    B -->|Yes| D{Rate Limit OK?}
    D -->|No| E[Rate Limit Error]
    D -->|Yes| F{Chatbot Available?}
    F -->|No| G[Service Unavailable]
    F -->|Yes| H[Process Message]
    H --> I{External API Call Needed?}
    I -->|Yes| J{API Available?}
    J -->|No| K[Use Cached Data]
    J -->|Yes| L[Fetch Fresh Data]
    I -->|No| M[Generate Response]
    K --> M
    L --> M
    M --> N{Response Generated?}
    N -->|No| O[Fallback Response]
    N -->|Yes| P[Return Response]
    
    C --> Q[Log Error]
    E --> Q
    G --> Q
    O --> Q
    Q --> R[Error Response to User]
    P --> S[Success Response]
    
    style C fill:#ffcccc
    style E fill:#ffcccc
    style G fill:#ffcccc
    style O fill:#ffffcc
    style P fill:#ccffcc
```

## 12. Training Data Pipeline

```mermaid
graph LR
    subgraph "Data Sources"
        A[User Conversations]
        B[Market Events]
        C[News Articles]
        D[Synthetic Data]
    end
    
    subgraph "Data Processing"
        E[Data Cleaning]
        F[Format Standardization]
        G[Quality Filtering]
        H[Personality Tagging]
    end
    
    subgraph "Training Pipeline"
        I[Scenario Generation]
        J[Response Testing]
        K[Quality Assessment]
        L[Model Updates]
    end
    
    subgraph "Validation & Deployment"
        M[A/B Testing]
        N[Performance Validation]
        O[Production Deployment]
        P[Monitoring]
    end
    
    A --> E
    B --> E
    C --> F
    D --> F
    E --> G
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N
    N --> O
    O --> P
    P --> A
```

---

## Diagram Usage Instructions

### For Development Teams:
1. **System Architecture**: Use for understanding component relationships
2. **Request Flow**: Debug API interactions and performance bottlenecks
3. **Training System**: Optimize learning algorithms and data flow
4. **Security Architecture**: Implement security best practices

### For Deployment Teams:
1. **Deployment Architecture**: Plan cloud infrastructure and scaling
2. **Performance Architecture**: Optimize resource allocation and caching
3. **Error Handling Flow**: Design robust error recovery systems

### For Business Stakeholders:
1. **Use Case Diagram**: Understand user journeys and feature scope
2. **Dual Personality Architecture**: Visualize unique selling proposition
3. **API Endpoint Structure**: Plan integrations and partnerships

### Converting to Visual Diagrams:

These Mermaid diagrams can be rendered using:
- **GitHub/GitLab**: Native Mermaid support
- **Mermaid Live Editor**: https://mermaid.live
- **VS Code**: Mermaid Preview extension
- **Draw.io**: Import Mermaid syntax
- **Lucidchart**: Convert to professional diagrams
- **Confluence/Notion**: Embedded Mermaid support

### Exporting Options:
- **PNG/SVG**: For documentation and presentations
- **PDF**: For formal documentation
- **Interactive HTML**: For web-based documentation
- **Editable formats**: For further customization

---

*These diagrams represent the complete KoinToss system architecture as of December 2024. For the latest updates, refer to the main documentation.*
