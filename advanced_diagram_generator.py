#!/usr/bin/env python3
"""
Advanced Diagram Generator for KoinToss Project
Generates multiple types of diagrams from existing codebase
"""

import ast
import os
import json
import networkx as nx
from pathlib import Path
from collections import defaultdict, Counter
import subprocess
import sys

class AdvancedDiagramGenerator:
    """Enhanced diagram generator with multiple output formats"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.code_files = []
        self.classes = {}
        self.functions = {}
        self.imports = {}
        self.call_graph = defaultdict(set)
        self.complexity_metrics = {}
        
    def scan_project(self):
        """Scan project for Python files"""
        print("🔍 Scanning project files...")
        
        self.code_files = list(self.project_root.glob("*.py"))
        print(f"📁 Found {len(self.code_files)} Python files")
        
        for file_path in self.code_files:
            try:
                self.analyze_file(file_path)
            except Exception as e:
                print(f"❌ Error analyzing {file_path.name}: {e}")
    
    def analyze_file(self, file_path: Path):
        """Analyze a single Python file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read(), filename=str(file_path))
                visitor = CodeVisitor(file_path.name)
                visitor.visit(tree)
                
                self.classes[file_path.name] = visitor.classes
                self.functions[file_path.name] = visitor.functions
                self.imports[file_path.name] = visitor.imports
                self.complexity_metrics[file_path.name] = visitor.complexity
                
            except SyntaxError as e:
                print(f"⚠️ Syntax error in {file_path.name}: {e}")
    
    def generate_enhanced_class_diagram(self) -> str:
        """Generate enhanced class diagram with relationships"""
        diagram = ["classDiagram"]
        diagram.append("    direction TB")
        
        # Class definitions with complexity indicators
        for file_name, classes in self.classes.items():
            for cls in classes:
                class_name = cls['name']
                complexity = cls.get('complexity', 0)
                
                # Color coding by complexity
                if complexity > 10:
                    diagram.append(f"    class {class_name}:::high-complexity")
                elif complexity > 5:
                    diagram.append(f"    class {class_name}:::medium-complexity")
                else:
                    diagram.append(f"    class {class_name}:::low-complexity")
                
                diagram.append(f"    {class_name} : +complexity: {complexity}")
                
                # Add methods with visibility
                for method in cls['methods']:
                    visibility = "🔒" if method['is_private'] else "🔓"
                    args_str = ", ".join(method['args'][:3])  # Limit args for readability
                    if len(method['args']) > 3:
                        args_str += "..."
                    diagram.append(f"    {class_name} : {visibility}{method['name']}({args_str})")
                
                # Add relationships
                for base in cls['base_classes']:
                    if base != 'object':
                        diagram.append(f"    {base} <|-- {class_name}")
        
        # CSS styling
        diagram.extend([
            "    classDef high-complexity fill:#ff6b6b,stroke:#333,stroke-width:2px",
            "    classDef medium-complexity fill:#ffd93d,stroke:#333,stroke-width:2px", 
            "    classDef low-complexity fill:#6bcf7f,stroke:#333,stroke-width:2px"
        ])
        
        return "\n".join(diagram)
    
    def generate_architecture_flow_diagram(self) -> str:
        """Generate system architecture flow diagram"""
        diagram = ["flowchart TD"]
        
        # Define layers
        layers = {
            "Frontend": ["streamlit", "iframe", "widget", "demo"],
            "API": ["api", "server", "enhanced_kointoss"],
            "Core": ["chatbot", "personality", "improved_dual"],
            "Training": ["trainer", "autonomous", "learning"],
            "Data": ["dataset", "crypto_news", "insights"],
            "Utils": ["utils", "article_manager", "test"]
        }
        
        # Add subgraphs for each layer
        for layer_name, keywords in layers.items():
            files = []
            for file_path in self.code_files:
                if any(keyword in file_path.name.lower() for keyword in keywords):
                    files.append(file_path.name.replace('.py', ''))
            
            if files:
                diagram.append(f"    subgraph {layer_name}[{layer_name} Layer]")
                for file in files[:5]:  # Limit to 5 files per layer
                    safe_name = file.replace('-', '_').replace('.', '_')
                    diagram.append(f"        {safe_name}[{file}]")
                diagram.append("    end")
        
        # Add flow connections
        diagram.extend([
            "    Frontend --> API",
            "    API --> Core",
            "    Core --> Training",
            "    Training --> Data",
            "    Data --> Utils",
            "    Utils --> Core"
        ])
        
        return "\n".join(diagram)
    
    def generate_interaction_sequence(self) -> str:
        """Generate user interaction sequence diagram"""
        diagram = ["sequenceDiagram"]
        diagram.extend([
            "    participant U as User",
            "    participant F as Frontend",
            "    participant A as API Server", 
            "    participant C as Chatbot",
            "    participant T as Trainer",
            "    participant D as Data Sources",
            "",
            "    U->>+F: Open Chat Interface",
            "    F->>+A: Initialize Session",
            "    A->>+C: Load Chatbot",
            "    C->>+T: Load Personalities",
            "    T-->>-C: Normal & SubZero Ready",
            "    C-->>-A: Chatbot Ready",
            "    A-->>-F: Session Created",
            "    F-->>-U: Interface Ready",
            "",
            "    loop Chat Interaction",
            "        U->>+F: Send Message",
            "        F->>+A: POST /chat",
            "        A->>+C: Process Message",
            "        ",
            "        alt Market Data Needed",
            "            C->>+D: Fetch Crypto Data",
            "            D-->>-C: Return Market Info",
            "        end",
            "        ",
            "        C->>+T: Generate Response",
            "        T-->>-C: Personality Response",
            "        C-->>-A: Final Response",
            "        A-->>-F: JSON Response",
            "        F-->>-U: Display Message",
            "    end"
        ])
        
        return "\n".join(diagram)
    
    def generate_complexity_heatmap(self) -> str:
        """Generate complexity visualization"""
        diagram = ["graph TB"]
        
        for file_name, complexity in self.complexity_metrics.items():
            safe_name = file_name.replace('.py', '').replace('-', '_')
            
            if complexity > 20:
                diagram.append(f"    {safe_name}[{file_name}<br/>Complexity: {complexity}]:::critical")
            elif complexity > 10:
                diagram.append(f"    {safe_name}[{file_name}<br/>Complexity: {complexity}]:::high")
            elif complexity > 5:
                diagram.append(f"    {safe_name}[{file_name}<br/>Complexity: {complexity}]:::medium")
            else:
                diagram.append(f"    {safe_name}[{file_name}<br/>Complexity: {complexity}]:::low")
        
        # Add styling
        diagram.extend([
            "    classDef critical fill:#dc3545,stroke:#000,stroke-width:2px,color:#fff",
            "    classDef high fill:#fd7e14,stroke:#000,stroke-width:2px,color:#fff",
            "    classDef medium fill:#ffc107,stroke:#000,stroke-width:2px,color:#000",
            "    classDef low fill:#28a745,stroke:#000,stroke-width:2px,color:#fff"
        ])
        
        return "\n".join(diagram)
    
    def generate_dependency_network(self) -> str:
        """Generate network-style dependency graph"""
        diagram = ["graph LR"]
        
        # Build dependency graph
        dependencies = {}
        for file_name, imports in self.imports.items():
            clean_name = file_name.replace('.py', '')
            dependencies[clean_name] = []
            
            for imp in imports:
                module = imp.get('module', '')
                if module and not module.startswith('.'):
                    # Focus on project internal dependencies
                    for other_file in self.code_files:
                        if module in other_file.name:
                            dependencies[clean_name].append(other_file.name.replace('.py', ''))
        
        # Add nodes and connections
        for source, targets in dependencies.items():
            safe_source = source.replace('-', '_')
            
            for target in targets:
                safe_target = target.replace('-', '_')
                diagram.append(f"    {safe_source} --> {safe_target}")
        
        return "\n".join(diagram)
    
    def export_diagrams(self):
        """Export all diagram types"""
        diagrams = {
            'enhanced_class_diagram.mermaid': self.generate_enhanced_class_diagram(),
            'architecture_flow.mermaid': self.generate_architecture_flow_diagram(),
            'interaction_sequence.mermaid': self.generate_interaction_sequence(),
            'complexity_heatmap.mermaid': self.generate_complexity_heatmap(),
            'dependency_network.mermaid': self.generate_dependency_network()
        }
        
        for filename, content in diagrams.items():
            output_path = self.project_root / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Generated: {filename}")
      def generate_interactive_html(self):
        """Generate interactive HTML with all diagrams"""
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>KoinToss Advanced Diagrams</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .diagram-section {{ margin: 30px 0; border: 1px solid #ddd; padding: 20px; }}
        .diagram-title {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .diagram-container {{ margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>🚀 KoinToss Advanced System Diagrams</h1>
    
    <div class="diagram-section">
        <h2 class="diagram-title">📊 Enhanced Class Diagram</h2>
        <div class="diagram-container">
            <div class="mermaid">
{enhanced_class}
            </div>
        </div>
    </div>
    
    <div class="diagram-section">
        <h2 class="diagram-title">🏗️ Architecture Flow</h2>
        <div class="diagram-container">
            <div class="mermaid">
{architecture_flow}
            </div>
        </div>
    </div>
    
    <div class="diagram-section">
        <h2 class="diagram-title">🔄 Interaction Sequence</h2>
        <div class="diagram-container">
            <div class="mermaid">
{interaction_sequence}
            </div>
        </div>
    </div>
    
    <div class="diagram-section">
        <h2 class="diagram-title">🌡️ Complexity Heatmap</h2>
        <div class="diagram-container">
            <div class="mermaid">
{complexity_heatmap}
            </div>
        </div>
    </div>
    
    <div class="diagram-section">
        <h2 class="diagram-title">🌐 Dependency Network</h2>
        <div class="diagram-container">
            <div class="mermaid">
{dependency_network}
            </div>
        </div>
    </div>
    
    <script>
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'neutral',
            themeVariables: {{
                primaryColor: '#3498db',
                primaryTextColor: '#2c3e50',
                primaryBorderColor: '#2980b9',
                lineColor: '#34495e'
            }}
        }});
    </script>
</body>
</html>"""
        
        diagrams = {
            'enhanced_class': self.generate_enhanced_class_diagram(),
            'architecture_flow': self.generate_architecture_flow_diagram(),
            'interaction_sequence': self.generate_interaction_sequence(),
            'complexity_heatmap': self.generate_complexity_heatmap(),
            'dependency_network': self.generate_dependency_network()
        }
        
        formatted_html = html_content.format(**diagrams)
        
        output_path = self.project_root / 'KoinToss_Advanced_Diagrams.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_html)
        
        print(f"✅ Generated interactive HTML: KoinToss_Advanced_Diagrams.html")


class CodeVisitor(ast.NodeVisitor):
    """AST visitor for code analysis"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.classes = []
        self.functions = []
        self.imports = []
        self.complexity = 0
        self.current_class = None
    
    def visit_ClassDef(self, node):
        """Visit class definition"""
        class_info = {
            'name': node.name,
            'base_classes': [base.id if isinstance(base, ast.Name) else 'Unknown' for base in node.bases],
            'methods': [],
            'attributes': [],
            'complexity': 0
        }
        
        self.current_class = class_info
        self.generic_visit(node)
        
        # Calculate class complexity
        class_info['complexity'] = len(class_info['methods']) + len(class_info['attributes'])
        self.classes.append(class_info)
        self.current_class = None
    
    def visit_FunctionDef(self, node):
        """Visit function definition"""
        func_complexity = self._calculate_complexity(node)
        self.complexity += func_complexity
        
        func_info = {
            'name': node.name,
            'args': [arg.arg for arg in node.args.args],
            'is_private': node.name.startswith('_'),
            'complexity': func_complexity
        }
        
        if self.current_class:
            self.current_class['methods'].append(func_info)
        else:
            self.functions.append(func_info)
        
        self.generic_visit(node)
    
    def visit_Import(self, node):
        """Visit import statement"""
        for alias in node.names:
            self.imports.append({
                'module': alias.name,
                'alias': alias.asname
            })
    
    def visit_ImportFrom(self, node):
        """Visit from import statement"""
        for alias in node.names:
            self.imports.append({
                'module': node.module,
                'name': alias.name,
                'alias': alias.asname
            })
    
    def _calculate_complexity(self, node):
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity


if __name__ == "__main__":
    print("🚀 Advanced Diagram Generator for KoinToss")
    print("=" * 50)
    
    # Initialize and run
    generator = AdvancedDiagramGenerator(".")
    generator.scan_project()
    generator.export_diagrams()
    generator.generate_interactive_html()
    
    print("\n🎉 Advanced diagram generation complete!")
    print("📁 Generated files:")
    print("   • enhanced_class_diagram.mermaid")
    print("   • architecture_flow.mermaid") 
    print("   • interaction_sequence.mermaid")
    print("   • complexity_heatmap.mermaid")
    print("   • dependency_network.mermaid")
    print("   • KoinToss_Advanced_Diagrams.html")
