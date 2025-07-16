#!/usr/bin/env python3
"""
Use Case and Flow Diagram Generator for KoinToss Project
Generates detailed use case diagrams, flow charts, and user journey maps
"""

import json
from pathlib import Path
from typing import Dict, List, Any

class UseFlowDiagramGenerator:
    """Generate use case and flow diagrams"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        
    def generate_user_journey_mermaid(self) -> str:
        """Generate user journey diagram"""
        diagram = ["journey"]
        diagram.extend([
            "    title User Journey with KoinToss Chatbot",
            "    section Discovery",
            "      Visit Website: 5: User",
            "      See Chat Widget: 4: User",
            "      Read About Features: 3: User",
            "    section First Interaction",
            "      Send First Message: 5: User",
            "      Receive Welcome: 5: User, Bot",
            "      Ask About Crypto: 4: User",
            "      Get Normal Response: 4: User, Bot",
            "    section Personality Discovery",
            "      Learn About SubZero: 3: User",
            "      Switch to SubZero: 5: User",
            "      Experience Personality: 5: User, Bot",
            "      Compare Responses: 4: User",
            "    section Advanced Usage",
            "      Ask Market Questions: 5: User",
            "      Get Real-time Data: 5: User, Bot, APIs",
            "      Receive News Updates: 4: User, Bot, APIs",
            "      Share Feedback: 3: User, Bot",
            "    section Integration",
            "      Embed Widget: 4: Developer",
            "      Use API: 5: Developer",
            "      Monitor Analytics: 3: Admin"
        ])
        
        return "\n".join(diagram)
    
    def generate_use_case_mermaid(self) -> str:
        """Generate comprehensive use case diagram"""
        diagram = ["graph TB"]
        diagram.extend([
            "    subgraph Users[Actors]",
            "        GU[General User]",
            "        CE[Crypto Enthusiast]", 
            "        DEV[Developer]",
            "        ADMIN[System Admin]",
            "    end",
            "",
            "    subgraph Core[Core Use Cases]",
            "        CHAT[Chat with Bot]",
            "        SWITCH[Switch Personalities]",
            "        MARKET[Get Market Data]",
            "        NEWS[Receive News]",
            "        LEARN[Learn About Crypto]",
            "    end",
            "",
            "    subgraph Advanced[Advanced Use Cases]",
            "        EMBED[Embed Widget]",
            "        API[API Integration]",
            "        TRAIN[Continuous Training]",
            "        ANALYTICS[View Analytics]",
            "        CONFIG[System Configuration]",
            "    end",
            "",
            "    subgraph System[System Use Cases]",
            "        MONITOR[Performance Monitoring]",
            "        DEPLOY[Deployment Management]",
            "        BACKUP[Data Backup]",
            "        SECURITY[Security Management]",
            "    end",
            "",
            "    %% User connections",
            "    GU --> CHAT",
            "    GU --> LEARN",
            "    GU --> NEWS",
            "    ",
            "    CE --> CHAT", 
            "    CE --> SWITCH",
            "    CE --> MARKET",
            "    CE --> NEWS",
            "    ",
            "    DEV --> EMBED",
            "    DEV --> API",
            "    DEV --> ANALYTICS",
            "    ",
            "    ADMIN --> TRAIN",
            "    ADMIN --> CONFIG",
            "    ADMIN --> MONITOR",
            "    ADMIN --> DEPLOY",
            "    ADMIN --> BACKUP",
            "    ADMIN --> SECURITY",
            "",
            "    %% Use case relationships",
            "    CHAT -.-> SWITCH",
            "    CHAT -.-> MARKET",
            "    CHAT -.-> NEWS",
            "    MARKET -.-> NEWS",
            "    EMBED -.-> API",
            "    ANALYTICS -.-> MONITOR",
            "",
            "    %% Styling",
            "    classDef userClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px",
            "    classDef coreClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px", 
            "    classDef advancedClass fill:#fff3e0,stroke:#e65100,stroke-width:2px",
            "    classDef systemClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px",
            "",
            "    class GU,CE,DEV,ADMIN userClass",
            "    class CHAT,SWITCH,MARKET,NEWS,LEARN coreClass",
            "    class EMBED,API,TRAIN,ANALYTICS,CONFIG advancedClass",
            "    class MONITOR,DEPLOY,BACKUP,SECURITY systemClass"
        ])
        
        return "\n".join(diagram)
    
    def generate_conversation_flow_mermaid(self) -> str:
        """Generate conversation flow diagram"""
        diagram = ["flowchart TD"]
        diagram.extend([
            "    START([User starts chat]) --> INPUT[User sends message]",
            "    INPUT --> VALIDATE{Valid input?}",
            "    VALIDATE -->|No| ERROR[Show error message]",
            "    ERROR --> INPUT",
            "    VALIDATE -->|Yes| PREPROCESS[Preprocess message]",
            "    ",
            "    PREPROCESS --> DETECT{Detect intent}",
            "    DETECT -->|Greeting| WELCOME[Welcome response]",
            "    DETECT -->|Market query| MARKET_FLOW[Market data flow]",
            "    DETECT -->|News request| NEWS_FLOW[News flow]",
            "    DETECT -->|Personality switch| SWITCH_FLOW[Switch flow]",
            "    DETECT -->|General chat| PERSONALITY{Current personality?}",
            "    ",
            "    PERSONALITY -->|Normal| NORMAL[Generate normal response]",
            "    PERSONALITY -->|SubZero| SUBZERO[Generate SubZero response]",
            "    ",
            "    MARKET_FLOW --> FETCH_MARKET[Fetch market data]",
            "    FETCH_MARKET --> FORMAT_MARKET[Format market response]",
            "    FORMAT_MARKET --> PERSONALITY",
            "    ",
            "    NEWS_FLOW --> FETCH_NEWS[Fetch crypto news]",
            "    FETCH_NEWS --> ANALYZE_SENTIMENT[Analyze sentiment]",
            "    ANALYZE_SENTIMENT --> FORMAT_NEWS[Format news response]",
            "    FORMAT_NEWS --> PERSONALITY",
            "    ",
            "    SWITCH_FLOW --> VALIDATE_SWITCH{Valid personality?}",
            "    VALIDATE_SWITCH -->|Yes| UPDATE_MODE[Update personality mode]",
            "    VALIDATE_SWITCH -->|No| SWITCH_ERROR[Invalid personality error]",
            "    UPDATE_MODE --> CONFIRM[Confirm switch]",
            "    SWITCH_ERROR --> DISPLAY",
            "    ",
            "    WELCOME --> DISPLAY[Display response]", 
            "    NORMAL --> LOG[Log interaction]",
            "    SUBZERO --> LOG",
            "    CONFIRM --> DISPLAY",
            "    ",
            "    LOG --> TRAIN{Training enabled?}",
            "    TRAIN -->|Yes| UPDATE_TRAINING[Update training data]",
            "    TRAIN -->|No| DISPLAY",
            "    UPDATE_TRAINING --> DISPLAY",
            "    ",
            "    DISPLAY --> WAIT[Wait for next input]",
            "    WAIT --> INPUT",
            "    ",
            "    %% Styling",
            "    classDef startEnd fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px",
            "    classDef process fill:#bbdefb,stroke:#1976d2,stroke-width:2px",
            "    classDef decision fill:#fff3c4,stroke:#f57f17,stroke-width:2px",
            "    classDef error fill:#ffcdd2,stroke:#c62828,stroke-width:2px",
            "    classDef data fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px",
            "    ",
            "    class START,DISPLAY,WAIT startEnd",
            "    class INPUT,PREPROCESS,NORMAL,SUBZERO,FETCH_MARKET,FETCH_NEWS process",
            "    class VALIDATE,DETECT,PERSONALITY,VALIDATE_SWITCH,TRAIN decision",
            "    class ERROR,SWITCH_ERROR error",
            "    class LOG,UPDATE_TRAINING,FORMAT_MARKET,FORMAT_NEWS data"
        ])
        
        return "\n".join(diagram)
    
    def generate_api_flow_mermaid(self) -> str:
        """Generate API interaction flow"""
        diagram = ["sequenceDiagram"]
        diagram.extend([
            "    participant Client as Client App",
            "    participant Gateway as API Gateway",
            "    participant Auth as Authentication",
            "    participant Rate as Rate Limiter",
            "    participant Bot as Chatbot Engine",
            "    participant Normal as Normal Trainer",
            "    participant SubZero as SubZero Trainer",
            "    participant News as News Service",
            "    participant Market as Market API",
            "    participant DB as Database",
            "",
            "    Note over Client,DB: Chat API Request Flow",
            "",
            "    Client->>+Gateway: POST /api/chat",
            "    Gateway->>+Auth: Validate API Key",
            "    Auth-->>-Gateway: Token Valid",
            "    Gateway->>+Rate: Check Rate Limit",
            "    Rate-->>-Gateway: Request Allowed",
            "    ",
            "    Gateway->>+Bot: Process Message",
            "    Bot->>Bot: Analyze Input",
            "    ",
            "    alt Market Data Needed",
            "        Bot->>+Market: Get Crypto Data",
            "        Market-->>-Bot: Market Information",
            "    end",
            "    ",
            "    alt News Required",
            "        Bot->>+News: Get Latest News",
            "        News-->>-Bot: News Articles",
            "    end",
            "    ",
            "    alt Normal Personality",
            "        Bot->>+Normal: Generate Response",
            "        Normal-->>-Bot: Professional Response",
            "    else SubZero Personality",
            "        Bot->>+SubZero: Generate Response",
            "        SubZero-->>-Bot: Crypto Native Response",
            "    end",
            "    ",
            "    Bot->>+DB: Log Interaction",
            "    DB-->>-Bot: Logged Successfully",
            "    ",
            "    Bot-->>-Gateway: Response Generated",
            "    Gateway-->>-Client: JSON Response",
            "",
            "    Note over Client,DB: Background Training Process",
            "",
            "    loop Continuous Learning",
            "        Bot->>+DB: Fetch Recent Interactions",
            "        DB-->>-Bot: Interaction Data",
            "        Bot->>+Normal: Update Training",
            "        Bot->>+SubZero: Update Training",
            "        Normal-->>-Bot: Training Complete",
            "        SubZero-->>-Bot: Training Complete",
            "    end"
        ])
        
        return "\n".join(diagram)
    
    def generate_system_state_mermaid(self) -> str:
        """Generate system state diagram"""
        diagram = ["stateDiagram-v2"]
        diagram.extend([
            "    [*] --> Initializing",
            "    ",
            "    Initializing --> Loading : Start System",
            "    Loading --> Ready : All Components Loaded",
            "    Loading --> Error : Load Failed",
            "    ",
            "    Ready --> Processing : Receive Request",
            "    Ready --> Training : Background Training",
            "    Ready --> Maintenance : Admin Request",
            "    ",
            "    Processing --> NormalMode : Normal Personality Selected",
            "    Processing --> SubZeroMode : SubZero Personality Selected",
            "    Processing --> Error : Processing Failed",
            "    ",
            "    NormalMode --> Responding : Generate Response",
            "    SubZeroMode --> Responding : Generate Response",
            "    ",
            "    Responding --> Ready : Response Sent",
            "    Responding --> Error : Response Failed",
            "    ",
            "    Training --> ModelUpdate : New Data Available",
            "    Training --> Ready : Training Complete",
            "    ",
            "    ModelUpdate --> Validating : Test Model",
            "    Validating --> Ready : Validation Passed",
            "    Validating --> Training : Validation Failed",
            "    ",
            "    Maintenance --> Updating : Apply Updates",
            "    Maintenance --> Monitoring : Check Health",
            "    Maintenance --> Backup : Create Backup",
            "    ",
            "    Updating --> Ready : Update Complete",
            "    Monitoring --> Ready : Health OK",
            "    Monitoring --> Error : Health Issues",
            "    Backup --> Ready : Backup Complete",
            "    ",
            "    Error --> Recovering : Auto Recovery",
            "    Error --> Shutdown : Critical Error",
            "    ",
            "    Recovering --> Ready : Recovery Successful",
            "    Recovering --> Shutdown : Recovery Failed",
            "    ",
            "    Shutdown --> [*]",
            "",
            "    note right of NormalMode",
            "        Professional responses",
            "        Educational focus",
            "        Risk awareness",
            "    end note",
            "",
            "    note right of SubZeroMode",
            "        Crypto native slang",
            "        Bold predictions", 
            "        Meme references",
            "    end note"
        ])
        
        return "\n".join(diagram)
    
    def generate_data_flow_mermaid(self) -> str:
        """Generate detailed data flow diagram"""
        diagram = ["flowchart LR"]
        diagram.extend([
            "    subgraph External[External Data Sources]",
            "        CG[CoinGecko API]",
            "        NEWS[News APIs]",
            "        SOCIAL[Social Media]",
            "        MARKET[Market Feeds]",
            "    end",
            "",
            "    subgraph Input[Data Input Layer]",
            "        COLLECTOR[Data Collector]",
            "        VALIDATOR[Data Validator]",
            "        NORMALIZER[Data Normalizer]",
            "    end",
            "",
            "    subgraph Processing[Processing Layer]",
            "        ANALYZER[Sentiment Analyzer]",
            "        FORMATTER[Response Formatter]",
            "        ROUTER[Personality Router]",
            "        CONTEXT[Context Manager]",
            "    end",
            "",
            "    subgraph Storage[Data Storage]",
            "        CACHE[Response Cache]",
            "        HISTORY[Conversation History]",
            "        TRAINING[Training Data]",
            "        METRICS[Performance Metrics]",
            "    end",
            "",
            "    subgraph Output[Output Layer]",
            "        RENDERER[Response Renderer]",
            "        LOGGER[Interaction Logger]",
            "        MONITOR[Performance Monitor]",
            "    end",
            "",
            "    %% External to Input",
            "    CG --> COLLECTOR",
            "    NEWS --> COLLECTOR",
            "    SOCIAL --> COLLECTOR",
            "    MARKET --> COLLECTOR",
            "",
            "    %% Input Layer Flow",
            "    COLLECTOR --> VALIDATOR",
            "    VALIDATOR --> NORMALIZER",
            "",
            "    %% Processing Flow",
            "    NORMALIZER --> ANALYZER",
            "    ANALYZER --> FORMATTER",
            "    FORMATTER --> ROUTER",
            "    ROUTER --> CONTEXT",
            "",
            "    %% Storage Interactions",
            "    CONTEXT <--> CACHE",
            "    CONTEXT <--> HISTORY",
            "    ROUTER <--> TRAINING",
            "    FORMATTER --> METRICS",
            "",
            "    %% Output Flow",
            "    CONTEXT --> RENDERER",
            "    RENDERER --> LOGGER",
            "    LOGGER --> MONITOR",
            "",
            "    %% Feedback Loop",
            "    MONITOR -.-> TRAINING",
            "    METRICS -.-> ROUTER",
            "",
            "    %% Styling",
            "    classDef external fill:#ffebee,stroke:#c62828,stroke-width:2px",
            "    classDef input fill:#e3f2fd,stroke:#1565c0,stroke-width:2px",
            "    classDef processing fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px",
            "    classDef storage fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px",
            "    classDef output fill:#fff3e0,stroke:#ef6c00,stroke-width:2px",
            "",
            "    class CG,NEWS,SOCIAL,MARKET external",
            "    class COLLECTOR,VALIDATOR,NORMALIZER input",
            "    class ANALYZER,FORMATTER,ROUTER,CONTEXT processing",
            "    class CACHE,HISTORY,TRAINING,METRICS storage",
            "    class RENDERER,LOGGER,MONITOR output"
        ])
        
        return "\n".join(diagram)
    
    def export_use_flow_diagrams(self):
        """Export all use case and flow diagrams"""
        diagrams = {
            'user_journey.mermaid': self.generate_user_journey_mermaid(),
            'use_case_diagram.mermaid': self.generate_use_case_mermaid(),
            'conversation_flow.mermaid': self.generate_conversation_flow_mermaid(),
            'api_flow.mermaid': self.generate_api_flow_mermaid(),
            'system_state.mermaid': self.generate_system_state_mermaid(),
            'data_flow_detailed.mermaid': self.generate_data_flow_mermaid()
        }
        
        for filename, content in diagrams.items():
            output_path = self.project_root / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Generated: {filename}")
        
        # Generate comprehensive HTML viewer
        self.generate_use_flow_html(diagrams)
    
    def generate_use_flow_html(self, diagrams: Dict[str, str]):
        """Generate HTML viewer for all use case and flow diagrams"""
        html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>KoinToss Use Case & Flow Diagrams</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        }}
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        .header {{ 
            background: linear-gradient(45deg, #74b9ff, #0984e3); 
            color: white; 
            padding: 30px; 
            text-align: center; 
        }}
        .nav {{ 
            background: #f8f9fa; 
            padding: 15px; 
            border-bottom: 1px solid #dee2e6;
            text-align: center;
        }}
        .nav button {{ 
            background: #74b9ff; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            margin: 0 5px;
            border-radius: 25px; 
            cursor: pointer; 
            transition: all 0.3s;
        }}
        .nav button:hover {{ background: #0984e3; }}
        .nav button.active {{ background: #0984e3; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }}
        .diagram-section {{ 
            display: none; 
            padding: 30px; 
        }}
        .diagram-section.active {{ display: block; }}
        .diagram-title {{ 
            color: #2d3436; 
            border-bottom: 3px solid #74b9ff; 
            padding-bottom: 10px; 
            margin-bottom: 20px;
        }}
        .diagram-container {{ 
            background: #f8f9fa; 
            border-radius: 10px; 
            padding: 20px; 
            margin: 20px 0;
            border-left: 5px solid #74b9ff;
        }}
        .description {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #1976d2;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 KoinToss Use Case & Flow Diagrams</h1>
            <p>Comprehensive user stories, flows, and system interactions</p>
        </div>
        
        <div class="nav">
            <button onclick="showDiagram('journey')" class="active">👤 User Journey</button>
            <button onclick="showDiagram('usecase')">🎯 Use Cases</button>
            <button onclick="showDiagram('conversation')">💬 Conversation Flow</button>
            <button onclick="showDiagram('api')">🔌 API Flow</button>
            <button onclick="showDiagram('state')">⚡ System States</button>
            <button onclick="showDiagram('dataflow')">📊 Data Flow</button>
        </div>
        
        <div id="journey" class="diagram-section active">
            <h2 class="diagram-title">👤 User Journey Map</h2>
            <div class="description">
                <strong>Purpose:</strong> Maps the complete user experience from discovery to advanced usage, showing touchpoints and emotional states throughout the interaction with KoinToss.
            </div>
            <div class="diagram-container">
                <div class="mermaid">
{user_journey}
                </div>
            </div>
        </div>
        
        <div id="usecase" class="diagram-section">
            <h2 class="diagram-title">🎯 Use Case Diagram</h2>
            <div class="description">
                <strong>Purpose:</strong> Comprehensive overview of all system functionalities, showing different user types and their interactions with KoinToss features.
            </div>
            <div class="diagram-container">
                <div class="mermaid">
{use_case_diagram}
                </div>
            </div>
        </div>
        
        <div id="conversation" class="diagram-section">
            <h2 class="diagram-title">💬 Conversation Flow</h2>
            <div class="description">
                <strong>Purpose:</strong> Detailed flow of how conversations are processed, from user input through personality routing to response generation.
            </div>
            <div class="diagram-container">
                <div class="mermaid">
{conversation_flow}
                </div>
            </div>
        </div>
        
        <div id="api" class="diagram-section">
            <h2 class="diagram-title">🔌 API Interaction Flow</h2>
            <div class="description">
                <strong>Purpose:</strong> Sequence diagram showing the complete API request lifecycle, including authentication, processing, and response generation.
            </div>
            <div class="diagram-container">
                <div class="mermaid">
{api_flow}
                </div>
            </div>
        </div>
        
        <div id="state" class="diagram-section">
            <h2 class="diagram-title">⚡ System State Diagram</h2>
            <div class="description">
                <strong>Purpose:</strong> Shows all possible system states and transitions, including error handling, maintenance modes, and personality switching.
            </div>
            <div class="diagram-container">
                <div class="mermaid">
{system_state}
                </div>
            </div>
        </div>
        
        <div id="dataflow" class="diagram-section">
            <h2 class="diagram-title">📊 Detailed Data Flow</h2>
            <div class="description">
                <strong>Purpose:</strong> Comprehensive data flow showing how information moves through the system, from external sources to user responses.
            </div>
            <div class="diagram-container">
                <div class="mermaid">
{data_flow_detailed}
                </div>
            </div>
        </div>
    </div>
    
    <script>
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'neutral',
            themeVariables: {{
                primaryColor: '#74b9ff',
                primaryTextColor: '#2d3436',
                primaryBorderColor: '#0984e3',
                lineColor: '#636e72'
            }}
        }});
        
        function showDiagram(diagramId) {{
            // Hide all sections
            document.querySelectorAll('.diagram-section').forEach(section => {{
                section.classList.remove('active');
            }});
            
            // Remove active class from all buttons
            document.querySelectorAll('.nav button').forEach(button => {{
                button.classList.remove('active');
            }});
            
            // Show selected section
            document.getElementById(diagramId).classList.add('active');
            
            // Add active class to clicked button
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>'''.format(**diagrams)
        
        output_path = self.project_root / 'KoinToss_UseFlow_Diagrams.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Generated interactive HTML: KoinToss_UseFlow_Diagrams.html")


if __name__ == "__main__":
    print("🎯 Use Case & Flow Diagram Generator")
    print("=" * 40)
    
    generator = UseFlowDiagramGenerator(".")
    generator.export_use_flow_diagrams()
    
    print("\n🎉 Use case and flow diagram generation complete!")
    print("📁 Generated files:")
    print("   • user_journey.mermaid")
    print("   • use_case_diagram.mermaid")
    print("   • conversation_flow.mermaid")
    print("   • api_flow.mermaid")
    print("   • system_state.mermaid")
    print("   • data_flow_detailed.mermaid")
    print("   • KoinToss_UseFlow_Diagrams.html")
