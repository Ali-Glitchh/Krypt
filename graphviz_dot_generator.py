#!/usr/bin/env python3
"""
GraphViz DOT Format Generator for KoinToss Project
Generates high-quality diagrams in DOT format for professional documentation
"""

import ast
import os
from pathlib import Path
from collections import defaultdict

class DOTDiagramGenerator:
    """Generate GraphViz DOT format diagrams"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.code_files = []
        self.classes = {}
        self.imports = {}
        
    def scan_project(self):
        """Scan project files"""
        self.code_files = list(self.project_root.glob("*.py"))
        
        for file_path in self.code_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                    visitor = DOTVisitor(file_path.name)
                    visitor.visit(tree)
                    
                    self.classes[file_path.name] = visitor.classes
                    self.imports[file_path.name] = visitor.imports
                    
            except Exception as e:
                print(f"Error analyzing {file_path.name}: {e}")
    
    def generate_class_hierarchy_dot(self) -> str:
        """Generate DOT format class hierarchy diagram"""
        dot = ['digraph ClassHierarchy {']
        dot.extend([
            '    rankdir=TB;',
            '    node [shape=record, style=filled, fillcolor=lightblue];',
            '    edge [color=darkblue, arrowhead=onormal];',
            ''
        ])
        
        # Add class nodes
        for file_name, classes in self.classes.items():
            for cls in classes:
                class_name = cls['name']
                methods = '\\n'.join([f"+ {m['name']}()" for m in cls['methods'][:5]])
                
                dot.append(f'    {class_name} [label="{{')
                dot.append(f'        {class_name}|')
                dot.append(f'        {methods}')
                dot.append('    }}"];')
                
                # Add inheritance relationships
                for base in cls['base_classes']:
                    if base != 'object':
                        dot.append(f'    {base} -> {class_name} [label="inherits"];')
        
        dot.append('}')
        return '\n'.join(dot)
    
    def generate_module_dependency_dot(self) -> str:
        """Generate DOT format module dependency diagram"""
        dot = ['digraph ModuleDependencies {']
        dot.extend([
            '    rankdir=LR;',
            '    node [shape=box, style=filled];',
            '    edge [color=darkgreen];',
            ''
        ])
        
        # Color coding by module type
        colors = {
            'chatbot': 'lightcoral',
            'trainer': 'lightgreen', 
            'api': 'lightblue',
            'test': 'lightyellow',
            'demo': 'lightpink'
        }
        
        # Add nodes with colors
        for file_name in self.code_files:
            clean_name = file_name.name.replace('.py', '')
            color = 'lightgray'
            
            for keyword, file_color in colors.items():
                if keyword in clean_name.lower():
                    color = file_color
                    break
            
            dot.append(f'    "{clean_name}" [fillcolor={color}];')
        
        # Add dependencies
        for file_name, imports in self.imports.items():
            source = file_name.replace('.py', '')
            
            for imp in imports:
                module = imp.get('module', '')
                if module:
                    # Check if it's an internal dependency
                    for other_file in self.code_files:
                        if module in other_file.name:
                            target = other_file.name.replace('.py', '')
                            dot.append(f'    "{source}" -> "{target}";')
        
        dot.append('}')
        return '\n'.join(dot)
    
    def generate_system_architecture_dot(self) -> str:
        """Generate DOT format system architecture"""
        dot = ['digraph SystemArchitecture {']
        dot.extend([
            '    rankdir=TB;',
            '    compound=true;',
            '    node [shape=box, style=filled];',
            ''
        ])
        
        # Define clusters (layers)
        layers = {
            'Frontend': ['streamlit', 'iframe', 'demo'],
            'API': ['api', 'server'],
            'Core': ['chatbot', 'personality'],
            'Training': ['trainer', 'autonomous'],
            'Data': ['dataset', 'crypto_news']
        }
        
        cluster_id = 0
        for layer_name, keywords in layers.items():
            dot.append(f'    subgraph cluster_{cluster_id} {{')
            dot.append(f'        label="{layer_name} Layer";')
            dot.append(f'        color=blue;')
            dot.append(f'        style=filled;')
            dot.append(f'        fillcolor=light{layer_name.lower()};')
            
            # Add matching files
            for file_path in self.code_files:
                if any(keyword in file_path.name.lower() for keyword in keywords):
                    clean_name = file_path.name.replace('.py', '')
                    dot.append(f'        "{clean_name}";')
            
            dot.append('    }')
            cluster_id += 1
        
        # Add inter-layer connections
        dot.extend([
            '    "Frontend" -> "API" [style=bold, color=red];',
            '    "API" -> "Core" [style=bold, color=red];',
            '    "Core" -> "Training" [style=bold, color=red];',
            '    "Training" -> "Data" [style=bold, color=red];'
        ])
        
        dot.append('}')
        return '\n'.join(dot)
    
    def export_dot_files(self):
        """Export all DOT format diagrams"""
        diagrams = {
            'class_hierarchy.dot': self.generate_class_hierarchy_dot(),
            'module_dependencies.dot': self.generate_module_dependency_dot(),
            'system_architecture.dot': self.generate_system_architecture_dot()
        }
        
        for filename, content in diagrams.items():
            output_path = self.project_root / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Generated DOT file: {filename}")
        
        # Generate conversion script
        self.generate_conversion_script()
    
    def generate_conversion_script(self):
        """Generate script to convert DOT files to images"""
        script_content = '''#!/bin/bash
# GraphViz DOT to Image Conversion Script
# Requires GraphViz to be installed: https://graphviz.org/download/

echo "🔄 Converting DOT files to images..."

# Convert to PNG (high quality)
for dot_file in *.dot; do
    base_name=$(basename "$dot_file" .dot)
    echo "   📊 Converting $dot_file to PNG..."
    dot -Tpng "$dot_file" -o "${base_name}.png"
done

# Convert to SVG (scalable)
for dot_file in *.dot; do
    base_name=$(basename "$dot_file" .dot)
    echo "   📈 Converting $dot_file to SVG..."
    dot -Tsvg "$dot_file" -o "${base_name}.svg"
done

# Convert to PDF (professional)
for dot_file in *.dot; do
    base_name=$(basename "$dot_file" .dot)
    echo "   📋 Converting $dot_file to PDF..."
    dot -Tpdf "$dot_file" -o "${base_name}.pdf"
done

echo "✅ Conversion complete!"
echo "📁 Generated files:"
ls -la *.png *.svg *.pdf 2>/dev/null || echo "   No output files found - check GraphViz installation"

# Windows batch version
cat > convert_diagrams.bat << 'EOF'
@echo off
echo Converting DOT files to images...

for %%f in (*.dot) do (
    echo Converting %%f to PNG...
    dot -Tpng "%%f" -o "%%~nf.png"
    
    echo Converting %%f to SVG...
    dot -Tsvg "%%f" -o "%%~nf.svg"
    
    echo Converting %%f to PDF...
    dot -Tpdf "%%f" -o "%%~nf.pdf"
)

echo Conversion complete!
dir *.png *.svg *.pdf
EOF

echo ""
echo "💡 Usage:"
echo "   Linux/Mac: chmod +x convert_diagrams.sh && ./convert_diagrams.sh"
echo "   Windows:   convert_diagrams.bat"
echo ""
echo "📦 Install GraphViz:"
echo "   Ubuntu:    sudo apt-get install graphviz"
echo "   macOS:     brew install graphviz"
echo "   Windows:   Download from https://graphviz.org/download/"
'''
        
        script_path = self.project_root / 'convert_diagrams.sh'
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Make script executable on Unix systems
        try:
            os.chmod(script_path, 0o755)
        except:
            pass
        
        print(f"✅ Generated conversion script: convert_diagrams.sh")


class DOTVisitor(ast.NodeVisitor):
    """AST visitor for DOT diagram generation"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.classes = []
        self.imports = []
        self.current_class = None
    
    def visit_ClassDef(self, node):
        """Visit class definition"""
        class_info = {
            'name': node.name,
            'base_classes': [base.id if isinstance(base, ast.Name) else 'Unknown' for base in node.bases],
            'methods': []
        }
        
        self.current_class = class_info
        self.generic_visit(node)
        self.classes.append(class_info)
        self.current_class = None
    
    def visit_FunctionDef(self, node):
        """Visit function definition"""
        func_info = {
            'name': node.name,
            'is_private': node.name.startswith('_')
        }
        
        if self.current_class:
            self.current_class['methods'].append(func_info)
        
        self.generic_visit(node)
    
    def visit_Import(self, node):
        """Visit import statement"""
        for alias in node.names:
            self.imports.append({'module': alias.name})
    
    def visit_ImportFrom(self, node):
        """Visit from import statement"""
        if node.module:
            self.imports.append({'module': node.module})


if __name__ == "__main__":
    print("🎨 GraphViz DOT Diagram Generator")
    print("=" * 40)
    
    generator = DOTDiagramGenerator(".")
    generator.scan_project()
    generator.export_dot_files()
    
    print("\n🎉 DOT diagram generation complete!")
    print("\n📝 Next steps:")
    print("   1. Install GraphViz: https://graphviz.org/download/")
    print("   2. Run: ./convert_diagrams.sh")
    print("   3. View generated PNG/SVG/PDF files")
