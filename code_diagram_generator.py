#!/usr/bin/env python3
"""
KoinToss Code Analysis and Diagram Generator
============================================

This script analyzes the KoinToss codebase and generates various diagrams
including dependency graphs, call flow diagrams, and class relationships.
"""

import os
import ast
import json
import re
from typing import Dict, List, Set, Tuple
from pathlib import Path

class CodeAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.python_files = []
        self.classes = {}
        self.functions = {}
        self.imports = {}
        self.dependencies = {}
        
    def scan_project(self):
        """Scan project for Python files and analyze them"""
        print(f"🔍 Scanning project at: {self.project_root}")
        
        # Find all Python files
        for file_path in self.project_root.glob("*.py"):
            if file_path.name.startswith('.') or '__pycache__' in str(file_path):
                continue
            self.python_files.append(file_path)
            
        print(f"📁 Found {len(self.python_files)} Python files")
        
        # Analyze each file
        for file_path in self.python_files:
            self.analyze_file(file_path)
            
    def analyze_file(self, file_path: Path):
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            tree = ast.parse(content)
            file_info = {
                'classes': [],
                'functions': [],
                'imports': [],
                'dependencies': []
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = self.analyze_class(node)
                    file_info['classes'].append(class_info)
                    
                elif isinstance(node, ast.FunctionDef):
                    func_info = self.analyze_function(node)
                    file_info['functions'].append(func_info)
                    
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    import_info = self.analyze_import(node)
                    file_info['imports'].extend(import_info)
                    
            self.classes[file_path.name] = file_info['classes']
            self.functions[file_path.name] = file_info['functions']
            self.imports[file_path.name] = file_info['imports']
            
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
            
    def analyze_class(self, node: ast.ClassDef) -> Dict:
        """Analyze a class definition"""
        methods = []
        attributes = []
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append({
                    'name': item.name,
                    'args': [arg.arg for arg in item.args.args],
                    'is_private': item.name.startswith('_'),
                    'is_property': any(
                        isinstance(d, ast.Name) and d.id == 'property' 
                        for d in item.decorator_list
                    )
                })
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)
                        
        return {
            'name': node.name,
            'base_classes': [base.id if isinstance(base, ast.Name) else str(base) for base in node.bases],
            'methods': methods,
            'attributes': attributes,
            'docstring': ast.get_docstring(node)
        }
        
    def analyze_function(self, node: ast.FunctionDef) -> Dict:
        """Analyze a function definition"""
        return {
            'name': node.name,
            'args': [arg.arg for arg in node.args.args],
            'returns': str(node.returns) if node.returns else None,
            'is_async': isinstance(node, ast.AsyncFunctionDef),
            'docstring': ast.get_docstring(node)
        }
        
    def analyze_import(self, node) -> List[Dict]:
        """Analyze import statements"""
        imports = []
        
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    'module': alias.name,
                    'alias': alias.asname,
                    'type': 'import'
                })
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.append({
                    'module': module,
                    'name': alias.name,
                    'alias': alias.asname,
                    'type': 'from_import'
                })
                
        return imports
        
    def generate_class_diagram_mermaid(self) -> str:
        """Generate Mermaid class diagram from analyzed code"""
        diagram = ["classDiagram"]
        
        # Add classes
        for file_name, classes in self.classes.items():
            for cls in classes:
                class_name = cls['name']
                diagram.append(f"    class {class_name} {{")
                
                # Add attributes
                for attr in cls['attributes']:
                    diagram.append(f"        +{attr}")
                    
                # Add methods
                for method in cls['methods']:
                    visibility = "-" if method['is_private'] else "+"
                    args_str = ", ".join(method['args'])
                    diagram.append(f"        {visibility}{method['name']}({args_str})")
                    
                diagram.append("    }")
                
                # Add inheritance relationships
                for base in cls['base_classes']:
                    if base != 'object':
                        diagram.append(f"    {base} <|-- {class_name}")
                        
        return "\n".join(diagram)
        
    def generate_dependency_graph_mermaid(self) -> str:
        """Generate Mermaid dependency graph"""
        diagram = ["graph TD"]
        
        # Track all modules
        all_modules = set()
        relationships = set()
        
        for file_name, imports in self.imports.items():
            file_module = file_name.replace('.py', '')
            all_modules.add(file_module)
            
            for imp in imports:
                module = imp['module']
                if module and not module.startswith('.'):
                    # External dependency
                    all_modules.add(module)
                    relationships.add((file_module, module))
                    
        # Add nodes
        for module in sorted(all_modules):
            safe_name = module.replace('-', '_').replace('.', '_')
            diagram.append(f"    {safe_name}[{module}]")
            
        # Add relationships
        for source, target in sorted(relationships):
            safe_source = source.replace('-', '_').replace('.', '_')
            safe_target = target.replace('-', '_').replace('.', '_')
            diagram.append(f"    {safe_source} --> {safe_target}")
            
        return "\n".join(diagram)
        
    def generate_file_structure_mermaid(self) -> str:
        """Generate project structure diagram"""
        diagram = ["graph TB"]
        
        # Group files by type
        core_files = []
        api_files = []
        training_files = []
        test_files = []
        config_files = []
        
        for file_path in self.python_files:
            file_name = file_path.name
            
            if 'test' in file_name.lower():
                test_files.append(file_name)
            elif 'api' in file_name.lower() or 'server' in file_name.lower():
                api_files.append(file_name)
            elif 'train' in file_name.lower() or 'autonomous' in file_name.lower():
                training_files.append(file_name)
            elif 'chatbot' in file_name.lower() or 'personality' in file_name.lower():
                core_files.append(file_name)
            else:
                config_files.append(file_name)
                
        # Add subgraphs
        if core_files:
            diagram.append('    subgraph "Core Chatbot"')
            for file in core_files:
                safe_name = file.replace('.py', '').replace('-', '_')
                diagram.append(f'        {safe_name}[{file}]')
            diagram.append('    end')
            
        if api_files:
            diagram.append('    subgraph "API Layer"')
            for file in api_files:
                safe_name = file.replace('.py', '').replace('-', '_')
                diagram.append(f'        {safe_name}[{file}]')
            diagram.append('    end')
            
        if training_files:
            diagram.append('    subgraph "Training System"')
            for file in training_files:
                safe_name = file.replace('.py', '').replace('-', '_')
                diagram.append(f'        {safe_name}[{file}]')
            diagram.append('    end')
            
        if test_files:
            diagram.append('    subgraph "Testing"')
            for file in test_files:
                safe_name = file.replace('.py', '').replace('-', '_')
                diagram.append(f'        {safe_name}[{file}]')
            diagram.append('    end')
            
        return "\n".join(diagram)
        
    def generate_call_flow_diagram(self, entry_point: str = 'improved_dual_personality_chatbot.py') -> str:
        """Generate call flow diagram for a specific entry point"""
        diagram = ["sequenceDiagram"]
        
        if entry_point in self.classes:
            main_class = None
            for cls in self.classes[entry_point]:
                if 'chatbot' in cls['name'].lower():
                    main_class = cls
                    break
                    
            if main_class:
                diagram.append("    participant User")
                diagram.append(f"    participant {main_class['name']}")
                
                # Add key methods as sequence
                key_methods = ['process_message', 'get_response', 'switch_personality']
                for method in main_class['methods']:
                    if any(key in method['name'] for key in key_methods):
                        diagram.append(f"    User->>+{main_class['name']}: {method['name']}()")
                        diagram.append(f"    {main_class['name']}-->>-User: response")
                        
        return "\n".join(diagram)
        
    def export_analysis_report(self, output_file: str = 'code_analysis_report.md'):
        """Export comprehensive analysis report"""
        report = [
            "# KoinToss Code Analysis Report",
            "",
            f"## Project Overview",
            f"- **Total Python Files**: {len(self.python_files)}",
            f"- **Total Classes**: {sum(len(classes) for classes in self.classes.values())}",
            f"- **Total Functions**: {sum(len(functions) for functions in self.functions.values())}",
            "",
            "## File Structure Diagram",
            "```mermaid",
            self.generate_file_structure_mermaid(),
            "```",
            "",
            "## Class Relationships",
            "```mermaid", 
            self.generate_class_diagram_mermaid(),
            "```",
            "",
            "## Dependency Graph",
            "```mermaid",
            self.generate_dependency_graph_mermaid(),
            "```",
            "",
            "## Call Flow Diagram",
            "```mermaid",
            self.generate_call_flow_diagram(),
            "```",
            "",
            "## Detailed Analysis",
            ""
        ]
        
        # Add file-by-file analysis
        for file_name in sorted(self.python_files, key=lambda x: x.name):
            report.append(f"### {file_name.name}")
            
            if file_name.name in self.classes and self.classes[file_name.name]:
                report.append("**Classes:**")
                for cls in self.classes[file_name.name]:
                    report.append(f"- `{cls['name']}`")
                    if cls['docstring']:
                        report.append(f"  - {cls['docstring'][:100]}...")
                    report.append(f"  - Methods: {len(cls['methods'])}")
                    report.append(f"  - Attributes: {len(cls['attributes'])}")
                    
            if file_name.name in self.functions and self.functions[file_name.name]:
                report.append("**Functions:**")
                for func in self.functions[file_name.name]:
                    report.append(f"- `{func['name']}()`")
                    if func['docstring']:
                        report.append(f"  - {func['docstring'][:100]}...")
                        
            if file_name.name in self.imports and self.imports[file_name.name]:
                external_imports = [
                    imp for imp in self.imports[file_name.name] 
                    if not imp['module'].startswith('.')
                ]
                if external_imports:
                    report.append("**Key Dependencies:**")
                    for imp in external_imports[:5]:  # Limit to top 5
                        report.append(f"- {imp['module']}")
                        
            report.append("")
            
        # Write report
        with open(self.project_root / output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
            
        print(f"📊 Analysis report exported to: {output_file}")

def main():
    """Main function to run code analysis"""
    print("🚀 KoinToss Code Analysis and Diagram Generator")
    print("=" * 50)
    
    # Get project root
    project_root = os.getcwd()
    print(f"📍 Project root: {project_root}")
    
    # Initialize analyzer
    analyzer = CodeAnalyzer(project_root)
    
    # Scan and analyze project
    analyzer.scan_project()
    
    # Generate individual diagram files
    diagrams = {
        'file_structure.mermaid': analyzer.generate_file_structure_mermaid(),
        'class_diagram.mermaid': analyzer.generate_class_diagram_mermaid(),
        'dependency_graph.mermaid': analyzer.generate_dependency_graph_mermaid(),
        'call_flow.mermaid': analyzer.generate_call_flow_diagram()
    }
    
    for filename, content in diagrams.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📈 Generated: {filename}")
        
    # Generate comprehensive analysis report
    analyzer.export_analysis_report()
    
    print("\n✅ Code analysis complete!")
    print("🎯 Generated files:")
    print("   - code_analysis_report.md (comprehensive report)")
    print("   - file_structure.mermaid (project structure)")
    print("   - class_diagram.mermaid (class relationships)")
    print("   - dependency_graph.mermaid (module dependencies)")
    print("   - call_flow.mermaid (execution flow)")
    
    print("\n💡 Tip: Use these Mermaid files in:")
    print("   - GitHub/GitLab (native support)")
    print("   - VS Code (Mermaid Preview extension)")
    print("   - mermaid.live (online editor)")
    print("   - Documentation systems (GitBook, Sphinx, etc.)")

if __name__ == "__main__":
    main()
