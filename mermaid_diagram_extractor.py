"""
Mermaid Diagram Extractor and Converter
Extracts Mermaid diagrams from the FYP report and provides instructions for conversion.
"""

import re
import os

def extract_mermaid_diagrams(input_file):
    """Extract all Mermaid diagrams from the markdown file"""
    print(f"Extracting Mermaid diagrams from {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all Mermaid code blocks
    mermaid_pattern = r'```mermaid\n(.*?)\n```'
    diagrams = re.findall(mermaid_pattern, content, re.DOTALL)
    
    if not diagrams:
        print("No Mermaid diagrams found.")
        return
    
    print(f"Found {len(diagrams)} Mermaid diagrams")
    
    # Create output directory
    output_dir = "mermaid_diagrams"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save each diagram to a separate file
    for i, diagram in enumerate(diagrams, 1):
        # Determine diagram type
        diagram_type = "flowchart"
        if "sequenceDiagram" in diagram:
            diagram_type = "sequence"
        elif "classDiagram" in diagram:
            diagram_type = "class"
        elif "graph" in diagram:
            diagram_type = "graph"
        
        # Save diagram
        filename = f"diagram_{i}_{diagram_type}.mmd"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(diagram)
        
        print(f"Saved: {filepath}")
    
    # Create conversion instructions
    create_conversion_instructions(output_dir, len(diagrams))

def create_conversion_instructions(output_dir, num_diagrams):
    """Create instructions for converting diagrams to images"""
    instructions_file = os.path.join(output_dir, "CONVERSION_INSTRUCTIONS.md")
    
    instructions = f"""# Mermaid Diagram Conversion Instructions

This directory contains {num_diagrams} Mermaid diagrams extracted from the KoinToss FYP report.

## Method 1: Online Conversion (Recommended)

1. Visit the Mermaid Live Editor: https://mermaid.live/
2. For each .mmd file:
   - Copy the content of the file
   - Paste it into the Mermaid Live Editor
   - Click "Download SVG" or "Download PNG"
   - Save the image with a descriptive name

## Method 2: Using VS Code Extension

1. Install the "Mermaid Markdown Syntax Highlighting" extension
2. Install the "Mermaid Preview" extension
3. Open each .mmd file in VS Code
4. Use the preview feature to view the diagram
5. Take a screenshot or export if the extension supports it

## Method 3: Command Line (if Mermaid CLI is installed)

```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Convert diagrams to PNG
mmdc -i diagram_1_graph.mmd -o diagram_1_graph.png
mmdc -i diagram_2_sequence.mmd -o diagram_2_sequence.png
mmdc -i diagram_3_class.mmd -o diagram_3_class.png
```

## Inserting into Word Document

1. Open KoinToss_FYP_Report_Professional.docx
2. Find the diagram placeholders (marked as "[Diagram X - To be inserted]")
3. Replace each placeholder with the corresponding converted image
4. Add proper captions: "Figure X: [Diagram Description]"
5. Ensure diagrams are properly sized and centered

## Diagram Descriptions

Use these descriptions for figure captions:

- Diagram 1: System Architecture Overview
- Diagram 2: User Interaction Flow
- Diagram 3: Data Processing Sequence
- (Add more as needed based on actual diagram content)

## Quality Guidelines

- Use PNG format for better quality in Word documents
- Ensure diagrams are at least 300 DPI for print quality
- Keep consistent styling across all diagrams
- Make sure text in diagrams is readable when printed
"""
    
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"Created conversion instructions: {instructions_file}")

def create_html_preview(output_dir):
    """Create an HTML file to preview all diagrams"""
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>KoinToss FYP - Mermaid Diagrams Preview</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .diagram { margin: 30px 0; padding: 20px; border: 1px solid #ddd; }
        .diagram h3 { color: #333; }
        pre { background: #f5f5f5; padding: 10px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>KoinToss FYP - Mermaid Diagrams Preview</h1>
    <p>This page shows all the Mermaid diagrams from the FYP report.</p>
"""
    
    # Add each diagram
    mmd_files = [f for f in os.listdir(output_dir) if f.endswith('.mmd')]
    
    for i, filename in enumerate(sorted(mmd_files), 1):
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            diagram_content = f.read()
        
        html_content += f"""
    <div class="diagram">
        <h3>Diagram {i}: {filename}</h3>
        <div class="mermaid">
{diagram_content}
        </div>
        <h4>Source Code:</h4>
        <pre>{diagram_content}</pre>
    </div>
"""
    
    html_content += """
    <script>
        mermaid.initialize({startOnLoad:true});
    </script>
</body>
</html>
"""
    
    html_file = os.path.join(output_dir, "diagrams_preview.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created HTML preview: {html_file}")
    print("Open this file in a web browser to see all diagrams rendered")

def main():
    """Main function"""
    input_file = "KoinToss_FYP_Report.md"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return
    
    try:
        extract_mermaid_diagrams(input_file)
        
        output_dir = "mermaid_diagrams"
        if os.path.exists(output_dir):
            create_html_preview(output_dir)
            
        print("\nNext steps:")
        print(f"1. Check the '{output_dir}' directory for extracted diagrams")
        print("2. Follow the instructions in CONVERSION_INSTRUCTIONS.md")
        print("3. Open diagrams_preview.html in a web browser to see rendered diagrams")
        print("4. Convert diagrams to images and insert into the Word document")
        
    except Exception as e:
        print(f"Error during extraction: {e}")

if __name__ == "__main__":
    main()
