# KoinToss System Diagrams - PlantUML Format

This document contains all system diagrams in PlantUML format, which can be rendered in various documentation systems and converted to multiple formats.

## 1. System Architecture (Component Diagram)

```plantuml
@startuml KoinToss_System_Architecture
!theme aws-orange

package "Frontend Layer" {
    [Embeddable JavaScript Widget] as Widget
    [Direct API Integration] as DirectAPI
    [Streamlit Web Interface] as Streamlit
}

package "API Gateway Layer" {
    [Enhanced FastAPI Server] as FastAPI
    [REST Endpoints] as REST
    [WebSocket Support] as WebSocket
    [Session Management] as Sessions
    [Rate Limiting] as RateLimit
    [CORS Protection] as CORS
}

package "Core Bot Engine" {
    [Dual Personality Chatbot] as DualBot
    [Normal Personality Trainer] as NormalTrainer
    [SubZero Personality Trainer] as SubZeroTrainer
}

package "Learning & Training Layer" {
    [Advanced Autonomous Trainer] as AdvancedTrainer
    [Dual Personality Intensive Trainer] as IntensiveTrainer
    [Training Monitor] as Monitor
    [Training Orchestrator] as Orchestrator
}

package "Data Integration Layer" {
    [CoinGecko API] as CoinGecko
    [News Sources] as News
    [Training Datasets] as Datasets
    [User Feedback] as Feedback
}

Widget --> FastAPI
DirectAPI --> FastAPI
Streamlit --> FastAPI

FastAPI --> REST
FastAPI --> WebSocket
FastAPI --> Sessions
FastAPI --> RateLimit
FastAPI --> CORS

FastAPI --> DualBot

DualBot --> NormalTrainer
DualBot --> SubZeroTrainer

DualBot --> AdvancedTrainer
DualBot --> IntensiveTrainer

AdvancedTrainer --> Monitor
IntensiveTrainer --> Monitor
Monitor --> Orchestrator

DualBot --> CoinGecko
DualBot --> News
AdvancedTrainer --> Datasets
IntensiveTrainer --> Feedback

note right of DualBot : Core processing engine\nwith dual personalities
note bottom of Monitor : Continuous learning\nand improvement

@enduml
```

## 2. Sequence Diagram - Chat Request Flow

```plantuml
@startuml Chat_Request_Flow
!theme aws-orange

actor User
participant "Widget/API" as Widget
participant "FastAPI Server" as FastAPI
participant "Chatbot Engine" as Chatbot
participant "Personality Trainer" as Trainer
participant "External APIs" as APIs

User -> Widget: Send Message
activate Widget

Widget -> FastAPI: POST /chat
activate FastAPI

FastAPI -> FastAPI: Validate & Rate Limit
FastAPI -> Chatbot: Process Message
activate Chatbot

Chatbot -> Trainer: Route to Personality
activate Trainer

Trainer -> Trainer: Generate Response

alt Market Data Needed
    Trainer -> APIs: Fetch Market Data
    activate APIs
    APIs --> Trainer: Return Data
    deactivate APIs
end

Trainer --> Chatbot: Return Response
deactivate Trainer

Chatbot -> Chatbot: Log for Training
Chatbot --> FastAPI: Return Processed Response
deactivate Chatbot

FastAPI --> Widget: JSON Response
deactivate FastAPI

Widget --> User: Display Response
deactivate Widget

note over Chatbot, Trainer: Autonomous training runs\ncontinuously in background

@enduml
```

## 3. Class Diagram - Core Components

```plantuml
@startuml Core_Components_Class_Diagram
!theme aws-orange

class ImprovedDualPersonalityChatbot {
    -personality_mode: str
    -normal_trainer: PureNormalTrainer
    -subzero_trainer: PureSubZeroTrainer
    -news_service: CryptoNewsInsights
    -conversation_history: List
    -learning_stats: Dict
    +__init__()
    +process_message(message: str): str
    +switch_personality(mode: str): bool
    +get_response(input: str): Dict
    +get_learning_stats(): Dict
}

class PureNormalTrainer {
    -dataset: List[Dict]
    -vocabulary: Set[str]
    -conversation_pairs: List
    +__init__()
    +load_dataset(): bool
    +preprocess_message(text: str): str
    +find_best_response(query: str): str
    +calculate_similarity(text1: str, text2: str): float
    +generate_response(message: str): str
}

class PureSubZeroTrainer {
    -responses: List[str]
    -crypto_keywords: Set[str]
    -character_phrases: List[str]
    +__init__()
    +load_subzero_responses(): bool
    +generate_response(message: str): str
    +maintain_character(): str
    +integrate_crypto_knowledge(response: str): str
}

class AdvancedAutonomousTrainer {
    -training_active: bool
    -market_data_collector: MarketDataCollector
    -quality_threshold: float
    -training_scenarios: List[Dict]
    -performance_metrics: Dict
    +__init__()
    +start_autonomous_training(): bool
    +generate_training_scenarios(): List[Dict]
    +evaluate_response_quality(question: str, response: str): float
    +record_interaction(user_input: str, bot_response: str): bool
    +get_training_statistics(): Dict
}

class CryptoNewsInsights {
    -news_sources: List[str]
    -sentiment_analyzer: VaderSentiment
    -api_clients: Dict
    +__init__()
    +get_crypto_news(symbol: str): List[Dict]
    +analyze_sentiment(text: str): Dict
    +get_market_insights(coin_id: str): Dict
    +format_news_response(news: List[Dict]): str
}

class SessionManager {
    -sessions: Dict[str, Dict]
    -cleanup_interval: int
    +__init__()
    +create_session(session_id: str): str
    +get_session(session_id: str): Dict
    +update_session(session_id: str, data: Dict): bool
    +cleanup_expired_sessions(): int
}

class EnhancedKoinTossAPIServer {
    -app: FastAPI
    -chatbot: ImprovedDualPersonalityChatbot
    -session_manager: SessionManager
    -rate_limiter: RateLimiter
    +__init__()
    +chat_endpoint(request: ChatRequest): ChatResponse
    +websocket_endpoint(websocket: WebSocket, session_id: str)
    +health_check(): HealthResponse
    +start_training(): TrainingResponse
}

ImprovedDualPersonalityChatbot *-- PureNormalTrainer
ImprovedDualPersonalityChatbot *-- PureSubZeroTrainer
ImprovedDualPersonalityChatbot *-- CryptoNewsInsights
ImprovedDualPersonalityChatbot *-- AdvancedAutonomousTrainer

EnhancedKoinTossAPIServer *-- ImprovedDualPersonalityChatbot
EnhancedKoinTossAPIServer *-- SessionManager

@enduml
```

## 4. State Diagram - Personality Switching

```plantuml
@startuml Personality_State_Diagram
!theme aws-orange

[*] --> Normal : Initialize

state Normal {
    Normal : Professional responses
    Normal : Educational focus
    Normal : Risk-aware advice
    Normal : Beginner friendly
}

state SubZero {
    SubZero : Crypto native slang
    SubZero : Meme references
    SubZero : Bold predictions
    SubZero : Character consistency
}

Normal --> SubZero : switch_personality("subzero")\nUser command detected
SubZero --> Normal : switch_personality("normal")\nUser command detected

Normal : exit / log personality change
SubZero : exit / log personality change

state ProcessingMessage {
    [*] --> AnalyzeInput
    AnalyzeInput --> RouteToPersonality
    RouteToPersonality --> GenerateResponse
    GenerateResponse --> LogInteraction
    LogInteraction --> [*]
}

Normal --> ProcessingMessage : process_message()
SubZero --> ProcessingMessage : process_message()
ProcessingMessage --> Normal : return to normal mode
ProcessingMessage --> SubZero : return to subzero mode

@enduml
```

## 5. Activity Diagram - Training Process

```plantuml
@startuml Training_Process_Activity
!theme aws-orange

start

:Start Autonomous Training;

:Collect Market Data;

:Generate Training Scenarios;

:Test Both Personalities;

fork
    :Test Normal Personality;
    :Evaluate Normal Response;
fork again
    :Test SubZero Personality;
    :Evaluate SubZero Response;
end fork

:Calculate Quality Scores;

if (Quality Score > Threshold?) then (yes)
    :Update Training Data;
    :Record Successful Pattern;
else (no)
    :Generate Alternative Response;
    :Re-evaluate Quality;
endif

:Update Performance Metrics;

:Generate Training Analytics;

if (Continue Training?) then (yes)
    :Wait for Next Cycle;
    backward :Collect Market Data;
else (no)
    :Save Training Session;
    :Generate Report;
    stop
endif

note right
    Background processes:
    - Real-time market monitoring
    - User interaction logging
    - Pattern recognition
    - Quality assessment
end note

@enduml
```

## 6. Deployment Diagram

```plantuml
@startuml Deployment_Architecture
!theme aws-orange

node "Development Environment" {
    artifact "Python 3.8+" as Python
    artifact "Testing Suite" as Tests
    artifact "Code Quality Tools" as CodeQuality
}

node "Container Environment" {
    artifact "Docker Container" as Docker
    artifact "docker-compose.yml" as Compose
    artifact "Environment Config" as EnvConfig
}

cloud "Cloud Platforms" {
    node "AWS" {
        component "ECS/Fargate" as AWS_ECS
        component "EC2" as AWS_EC2
    }
    
    node "Google Cloud" {
        component "Cloud Run" as GCP_Run
        component "Compute Engine" as GCP_Compute
    }
    
    node "Azure" {
        component "Container Instances" as Azure_CI
        component "App Service" as Azure_App
    }
    
    node "Other Platforms" {
        component "Heroku" as Heroku
        component "Railway" as Railway
    }
}

node "Production Infrastructure" {
    component "Load Balancer" as LB
    component "SSL Termination" as SSL
    component "Health Monitoring" as Monitor
    component "Centralized Logging" as Logs
}

Python --> Docker
Tests --> Docker
CodeQuality --> Docker

Docker --> Compose
Compose --> EnvConfig

EnvConfig --> AWS_ECS
EnvConfig --> GCP_Run
EnvConfig --> Azure_CI
EnvConfig --> Heroku

AWS_ECS --> LB
GCP_Run --> LB
Azure_CI --> LB
Heroku --> LB

LB --> SSL
LB --> Monitor
LB --> Logs

@enduml
```

## 7. Use Case Diagram

```plantuml
@startuml Use_Case_Diagram
!theme aws-orange

left to right direction

actor "General User" as GeneralUser
actor "Crypto Enthusiast" as CryptoUser
actor "Developer" as Dev
actor "System Admin" as Admin

rectangle "KoinToss System" {
    usecase "Chat with Bot" as Chat
    usecase "Switch Personalities" as Switch
    usecase "Get Market Data" as Market
    usecase "Receive News" as News
    usecase "Embed Widget" as Embed
    usecase "API Integration" as APIInt
    usecase "Monitor Performance" as Monitor
    usecase "Manage Training" as Training
    usecase "Configure System" as Config
    usecase "View Analytics" as Analytics
    usecase "Manage Sessions" as Sessions
    usecase "Deploy Updates" as Deploy
}

GeneralUser --> Chat
GeneralUser --> Switch
GeneralUser --> Market
GeneralUser --> News

CryptoUser --> Chat
CryptoUser --> Switch
CryptoUser --> Market
CryptoUser --> News

Dev --> Embed
Dev --> APIInt
Dev --> Monitor

Admin --> Training
Admin --> Config
Admin --> Analytics
Admin --> Sessions
Admin --> Deploy

Chat .> Switch : includes
Market .> News : includes
APIInt .> Embed : extends
Monitor .> Analytics : extends

note bottom of Chat
    Primary use case for all users.
    System routes to appropriate
    personality based on context.
end note

note bottom of Training
    Continuous background process
    that improves bot responses
    over time.
end note

@enduml
```

## 8. Package Diagram - System Structure

```plantuml
@startuml Package_Structure
!theme aws-orange

package "Core System" {
    package "Chatbot Engine" {
        class ImprovedDualPersonalityChatbot
        class PureNormalTrainer
        class PureSubZeroTrainer
    }
    
    package "API Layer" {
        class EnhancedKoinTossAPIServer
        class SessionManager
        class RateLimiter
    }
    
    package "Training System" {
        class AdvancedAutonomousTrainer
        class DualPersonalityIntensiveTrainer
        class TrainingMonitor
        class TrainingOrchestrator
    }
}

package "External Integrations" {
    package "Data Sources" {
        interface CoinGeckoAPI
        interface NewsAPIs
        interface MarketDataFeeds
    }
    
    package "Storage" {
        class ConversationHistory
        class TrainingDatasets
        class SessionStore
    }
}

package "Frontend Interfaces" {
    package "Web Components" {
        class JavaScriptWidget
        class StreamlitInterface
        class EmbeddableComponents
    }
    
    package "API Clients" {
        class RESTClient
        class WebSocketClient
        class SDKs
    }
}

"Chatbot Engine" --> "Training System"
"API Layer" --> "Chatbot Engine"
"Training System" --> "Data Sources"
"Chatbot Engine" --> "Data Sources"
"API Layer" --> "Storage"
"Web Components" --> "API Layer"
"API Clients" --> "API Layer"

@enduml
```

## 9. Network Diagram - Production Architecture

```plantuml
@startuml Network_Architecture
!theme aws-orange

!define AWSPUML https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v15.0/dist
!includeurl AWSPUML/AWSCommon.puml
!includeurl AWSPUML/ApplicationIntegration/APIGateway.puml
!includeurl AWSPUML/Compute/ECS.puml
!includeurl AWSPUML/Database/ElastiCache.puml
!includeurl AWSPUML/NetworkingContentDelivery/CloudFront.puml

actor Users as users

cloud Internet {
    CloudFront(cdn, "CloudFront CDN", "Static Assets")
}

rectangle "Load Balancer" as lb {
    component "Nginx/ALB" as nginx
    component "SSL Termination" as ssl
}

rectangle "Application Tier" as app {
    ECS(ecs, "Container Service", "FastAPI Application")
    component "KoinToss API" as api
    component "WebSocket Server" as ws
}

rectangle "Caching Layer" as cache {
    ElastiCache(redis, "Redis Cache", "Sessions & Responses")
}

rectangle "External Services" as external {
    component "CoinGecko API" as coingecko
    component "News APIs" as news
    component "Market Data" as market
}

rectangle "Monitoring & Logging" as monitoring {
    component "Health Checks" as health
    component "Metrics Collection" as metrics
    component "Log Aggregation" as logs
}

users --> cdn
users --> nginx
cdn --> nginx
nginx --> ssl
ssl --> ecs
ecs --> api
ecs --> ws
api --> redis
ws --> redis
api --> coingecko
api --> news
api --> market
ecs --> health
health --> metrics
metrics --> logs

note bottom of ecs
    Auto-scaling enabled
    Multiple availability zones
    Rolling deployments
end note

note bottom of redis
    Session persistence
    Response caching
    Rate limiting data
end note

@enduml
```

## 10. Data Flow Diagram

```plantuml
@startuml Data_Flow_Diagram
!theme aws-orange

rectangle "Input Sources" {
    component "User Messages" as input1
    component "Market Data APIs" as input2
    component "News Sources" as input3
    component "Training Datasets" as input4
}

rectangle "Processing Layer" {
    process "Message Preprocessor" as proc1
    process "Context Analyzer" as proc2
    process "Personality Router" as proc3
    process "Response Generator" as proc4
}

rectangle "Knowledge Base" {
    storage "Crypto Knowledge DB" as kb1
    storage "Conversation History" as kb2
    storage "Market Context" as kb3
    storage "User Preferences" as kb4
}

rectangle "Output Layer" {
    process "Response Formatter" as out1
    process "Learning Logger" as out2
    process "Metrics Collector" as out3
    component "User Interface" as out4
}

input1 --> proc1
input2 --> proc2
input3 --> proc2
input4 --> kb1

proc1 --> proc3
proc2 --> proc3
proc3 --> proc4

kb1 --> proc4
kb2 --> proc4
kb3 --> proc4
kb4 --> proc4

proc4 --> out1
proc4 --> out2
proc4 --> out3
out1 --> out4
out2 --> kb2
out3 --> kb4

note bottom of proc3
    Routes to Normal or SubZero
    personality based on context
    and user preferences
end note

note bottom of kb2
    Stores all conversations
    for continuous learning
    and context awareness
end note

@enduml
```

---

## Usage Instructions

### Rendering PlantUML Diagrams

These diagrams can be rendered using:

1. **Online PlantUML Editor**: http://www.plantuml.com/plantuml/
2. **VS Code Extension**: PlantUML extension
3. **IntelliJ IDEA**: Built-in PlantUML support
4. **Command Line**: 
   ```bash
   java -jar plantuml.jar diagram.puml
   ```
5. **Confluence/Jira**: Native PlantUML support
6. **GitHub**: PlantUML proxy service
7. **GitLab**: Built-in PlantUML rendering

### Export Formats

PlantUML supports multiple output formats:
- **PNG**: For documentation and presentations
- **SVG**: For scalable vector graphics
- **PDF**: For formal documentation
- **ASCII**: For text-based documentation
- **LaTeX**: For academic papers

### Integration Options

- **Documentation Systems**: Sphinx, GitBook, MkDocs
- **Wiki Systems**: MediaWiki, Confluence, Notion
- **Issue Tracking**: Jira, GitHub Issues
- **Presentation Tools**: RevealJS, PowerPoint
- **Code Documentation**: Doxygen, JSDoc

### Customization

Each diagram can be customized with:
- **Themes**: AWS, Azure, Google Cloud themes available
- **Colors**: Custom color schemes
- **Fonts**: Typography customization
- **Layout**: Direction and positioning control
- **Styling**: Line styles, shapes, and icons

---

*These PlantUML diagrams provide a comprehensive technical view of the KoinToss system architecture and can be easily integrated into any documentation system or presentation.*
