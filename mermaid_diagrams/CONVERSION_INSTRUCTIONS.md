# Mermaid Diagram Conversion Instructions

This directory contains 3 Mermaid diagrams extracted from the KoinToss FYP report.

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
