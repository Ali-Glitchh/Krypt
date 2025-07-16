"""
Alternative Diagram Converter with Manual Fallback
Creates simplified diagrams and provides manual conversion methods.
"""

import os
import json
import time

def create_simplified_html_diagrams():
    """Create HTML representations of diagrams that can be screenshot"""
    
    # Define diagram data
    diagrams = {
        "diagram_1": {
            "title": "KoinToss System Architecture",
            "type": "Layered Architecture",
            "description": "Modular system design with clear separation of concerns",
            "content": """
            <div class="architecture-diagram">
                <div class="layer frontend">
                    <h4>Frontend Layer</h4>
                    <div class="component">Streamlit Web Interface</div>
                    <div class="component">User Experience Layer</div>
                </div>
                
                <div class="layer application">
                    <h4>Application Layer</h4>
                    <div class="component">Chatbot Manager</div>
                    <div class="component">Personality Manager</div>
                    <div class="component">Training Manager</div>
                </div>
                
                <div class="layer core">
                    <h4>Core Services</h4>
                    <div class="component">NLP Engine</div>
                    <div class="component">Machine Learning</div>
                    <div class="component">API Integration</div>
                </div>
                
                <div class="layer data">
                    <h4>Data Layer</h4>
                    <div class="component">Training Data</div>
                    <div class="component">Conversation Data</div>
                    <div class="component">Market Data</div>
                </div>
                
                <div class="layer external">
                    <h4>External Services</h4>
                    <div class="component">CoinGecko API</div>
                    <div class="component">CryptoCompare API</div>
                    <div class="component">News Services</div>
                </div>
            </div>
            """
        },
        
        "diagram_2": {
            "title": "High-Level System Components",
            "type": "Component Interaction",
            "description": "Detailed view of internal component relationships",
            "content": """
            <div class="component-diagram">
                <div class="flow-container">
                    <div class="flow-item start">
                        <div class="box">User Interface</div>
                        <div class="arrow">↓</div>
                    </div>
                    
                    <div class="flow-item">
                        <div class="box group">
                            <h5>Application Layer</h5>
                            <div class="sub-component">Personality Manager</div>
                            <div class="sub-component">Training Manager</div>
                            <div class="sub-component">API Manager</div>
                        </div>
                        <div class="arrow">↓</div>
                    </div>
                    
                    <div class="flow-item">
                        <div class="box group">
                            <h5>Core AI Engine</h5>
                            <div class="sub-component">NLP Processor</div>
                            <div class="sub-component">Similarity Engine</div>
                            <div class="sub-component">Response Generator</div>
                        </div>
                        <div class="arrow">↓</div>
                    </div>
                    
                    <div class="flow-item">
                        <div class="box group">
                            <h5>Data Layer</h5>
                            <div class="sub-component">Training Data</div>
                            <div class="sub-component">Conversation History</div>
                            <div class="sub-component">User Preferences</div>
                        </div>
                        <div class="arrow">↓</div>
                    </div>
                    
                    <div class="flow-item end">
                        <div class="box group">
                            <h5>External APIs</h5>
                            <div class="sub-component">CoinGecko API</div>
                            <div class="sub-component">CryptoCompare API</div>
                            <div class="sub-component">News Services</div>
                        </div>
                    </div>
                </div>
            </div>
            """
        },
        
        "diagram_3": {
            "title": "Dual Personality Processing Flow",
            "type": "Process Flow",
            "description": "Decision flow for personality-based response generation",
            "content": """
            <div class="flowchart-diagram">
                <div class="flowchart-container">
                    <div class="flow-step start">
                        <div class="oval">User Input</div>
                        <div class="arrow">↓</div>
                    </div>
                    
                    <div class="flow-step">
                        <div class="rectangle">Parse Input</div>
                        <div class="arrow">↓</div>
                    </div>
                    
                    <div class="flow-step">
                        <div class="diamond">Personality Switch?</div>
                        <div class="branch">
                            <div class="branch-left">
                                <div class="label">Yes</div>
                                <div class="arrow-left">→</div>
                                <div class="rectangle">Switch Personality</div>
                                <div class="arrow-down">↓</div>
                            </div>
                            <div class="branch-right">
                                <div class="label">No</div>
                                <div class="arrow-down">↓</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="flow-step">
                        <div class="rectangle">Route to Current Personality</div>
                        <div class="arrow">↓</div>
                    </div>
                    
                    <div class="flow-step">
                        <div class="diamond">Normal Personality?</div>
                        <div class="branch">
                            <div class="branch-left">
                                <div class="label">Yes</div>
                                <div class="arrow-left">→</div>
                                <div class="rectangle">Enhanced Normal Trainer</div>
                            </div>
                            <div class="branch-right">
                                <div class="label">No</div>
                                <div class="arrow-right">→</div>
                                <div class="rectangle">Pure SubZero Trainer</div>
                            </div>
                        </div>
                        <div class="merge-arrow">↓</div>
                    </div>
                    
                    <div class="flow-step">
                        <div class="rectangle">Generate Response</div>
                        <div class="arrow">↓</div>
                    </div>
                    
                    <div class="flow-step">
                        <div class="rectangle">Record Interaction</div>
                        <div class="arrow">↓</div>
                    </div>
                    
                    <div class="flow-step end">
                        <div class="oval">Return Response</div>
                    </div>
                </div>
            </div>
            """
        }
    }
    
    # Create comprehensive HTML with all diagrams
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>KoinToss FYP - System Diagrams (Ready for Screenshots)</title>
    <style>
        body {{
            font-family: 'Times New Roman', serif;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        
        .diagram-container {{
            background-color: white;
            margin: 30px auto;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            max-width: 1000px;
            page-break-after: always;
        }}
        
        .diagram-title {{
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .diagram-subtitle {{
            text-align: center;
            font-size: 14px;
            color: #7f8c8d;
            margin-bottom: 30px;
            font-style: italic;
        }}
        
        /* Architecture Diagram Styles */
        .architecture-diagram {{
            display: flex;
            flex-direction: column;
            gap: 15px;
            padding: 20px;
        }}
        
        .layer {{
            border: 2px solid #34495e;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            position: relative;
        }}
        
        .layer h4 {{
            margin: 0 0 15px 0;
            font-weight: bold;
            color: #2c3e50;
            font-size: 16px;
        }}
        
        .layer.frontend {{ background-color: #e8f5e8; border-color: #27ae60; }}
        .layer.application {{ background-color: #e8f4f8; border-color: #3498db; }}
        .layer.core {{ background-color: #fef9e7; border-color: #f39c12; }}
        .layer.data {{ background-color: #f4e8f8; border-color: #9b59b6; }}
        .layer.external {{ background-color: #f8e8e8; border-color: #e74c3c; }}
        
        .component {{
            background-color: white;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 8px 12px;
            margin: 5px;
            display: inline-block;
            font-size: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* Component Diagram Styles */
        .component-diagram {{
            padding: 20px;
        }}
        
        .flow-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }}
        
        .flow-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        
        .box {{
            border: 2px solid #34495e;
            border-radius: 6px;
            padding: 12px 20px;
            background-color: #ecf0f1;
            min-width: 200px;
            text-align: center;
            font-weight: bold;
            font-size: 14px;
        }}
        
        .box.group {{
            background-color: #d5dbdb;
            border-style: dashed;
            min-width: 300px;
        }}
        
        .box h5 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
            font-size: 16px;
        }}
        
        .sub-component {{
            background-color: white;
            border: 1px solid #95a5a6;
            border-radius: 4px;
            padding: 6px 10px;
            margin: 3px;
            display: inline-block;
            font-size: 11px;
            font-weight: normal;
        }}
        
        .arrow {{
            font-size: 24px;
            color: #3498db;
            margin: 5px 0;
            font-weight: bold;
        }}
        
        /* Flowchart Diagram Styles */
        .flowchart-diagram {{
            padding: 20px;
        }}
        
        .flowchart-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 15px;
        }}
        
        .flow-step {{
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }}
        
        .oval {{
            border: 2px solid #27ae60;
            border-radius: 50px;
            padding: 12px 25px;
            background-color: #e8f5e8;
            font-weight: bold;
            text-align: center;
            min-width: 120px;
        }}
        
        .rectangle {{
            border: 2px solid #3498db;
            border-radius: 6px;
            padding: 12px 20px;
            background-color: #e8f4f8;
            font-weight: bold;
            text-align: center;
            min-width: 150px;
        }}
        
        .diamond {{
            border: 2px solid #f39c12;
            background-color: #fef9e7;
            padding: 15px 20px;
            font-weight: bold;
            text-align: center;
            transform: rotate(45deg);
            min-width: 120px;
            position: relative;
        }}
        
        .diamond::before {{
            content: attr(data-text);
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-45deg);
            white-space: nowrap;
        }}
        
        .branch {{
            display: flex;
            justify-content: space-around;
            width: 100%;
            margin: 20px 0;
            position: relative;
        }}
        
        .branch-left, .branch-right {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }}
        
        .label {{
            font-size: 12px;
            color: #e74c3c;
            font-weight: bold;
        }}
        
        .arrow-left, .arrow-right, .arrow-down {{
            font-size: 20px;
            color: #3498db;
            font-weight: bold;
        }}
        
        .merge-arrow {{
            font-size: 24px;
            color: #3498db;
            margin-top: 20px;
            font-weight: bold;
        }}
        
        .instruction-box {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
            font-size: 14px;
        }}
        
        .instruction-box h4 {{
            color: #856404;
            margin-top: 0;
        }}
        
        @media print {{
            .diagram-container {{
                page-break-after: always;
                margin: 0;
                box-shadow: none;
                border: 1px solid #ddd;
            }}
        }}
    </style>
</head>
<body>
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #2c3e50;">KoinToss FYP Report - System Diagrams</h1>
        <p style="color: #7f8c8d; font-style: italic;">Professional diagrams ready for Word document integration</p>
    </div>
    
    <div class="instruction-box">
        <h4>📸 How to Use These Diagrams</h4>
        <p><strong>Method 1 (Recommended):</strong> Take high-quality screenshots of each diagram below</p>
        <ol>
            <li>Use Windows Snipping Tool or Snip & Sketch (Windows + Shift + S)</li>
            <li>Capture each diagram individually with some white space around it</li>
            <li>Save as PNG format for best quality</li>
            <li>Insert into your Word document</li>
        </ol>
        <p><strong>Method 2:</strong> Print to PDF and extract images</p>
        <p><strong>Method 3:</strong> Use browser developer tools to save individual diagram elements</p>
    </div>
"""
    
    # Add each diagram
    for diagram_id, diagram_data in diagrams.items():
        html_content += f"""
    <div class="diagram-container" id="{diagram_id}">
        <div class="diagram-title">Figure {diagram_id[-1]}: {diagram_data['title']}</div>
        <div class="diagram-subtitle">{diagram_data['description']}</div>
        {diagram_data['content']}
    </div>
"""
    
    html_content += f"""
    <div style="text-align: center; padding: 30px; color: #7f8c8d;">
        <p><em>Generated on {time.strftime('%B %d, %Y at %I:%M %p')}</em></p>
        <p><strong>File:</strong> professional_diagrams_for_word.html</p>
    </div>
</body>
</html>
"""
    
    return html_content

def create_word_integration_guide():
    """Create a detailed guide for integrating diagrams into Word"""
    guide_content = """# KoinToss FYP - Diagram Integration Guide

## 📊 Diagrams Created

### Figure 1: KoinToss System Architecture
- **Type:** Layered Architecture Diagram
- **Purpose:** Shows the modular design with clear separation of frontend, application, core services, data, and external layers
- **Caption:** "Figure 1: KoinToss System Architecture - Overview of the modular, layered architecture showing frontend, application, core services, data layer, and external API integration."

### Figure 2: High-Level System Components  
- **Type:** Component Interaction Diagram
- **Purpose:** Illustrates detailed component relationships and data flow
- **Caption:** "Figure 2: High-Level System Components - Detailed view of the application layer components including personality manager, training manager, and API manager with their interconnections."

### Figure 3: Dual Personality Processing Flow
- **Type:** Process Flow Diagram  
- **Purpose:** Shows the decision-making process for personality-based responses
- **Caption:** "Figure 3: Dual Personality Processing Flow - Process flow showing how user input is parsed, routed to appropriate personality trainer, and response generation workflow."

## 🔧 Integration Steps

### Step 1: Capture Diagrams
1. Open `professional_diagrams_for_word.html` in your web browser
2. Use Windows Snipping Tool (Windows + Shift + S) to capture each diagram
3. Save each diagram as PNG with descriptive names:
   - `Figure1_SystemArchitecture.png`
   - `Figure2_SystemComponents.png` 
   - `Figure3_PersonalityFlow.png`

### Step 2: Insert into Word Document
1. Open `KoinToss_FYP_Report_Professional.docx`
2. Navigate to each diagram placeholder
3. Replace placeholder text with actual images:
   - Insert → Pictures → This Device
   - Select the appropriate PNG file
   - Resize to fit page width (usually 6-7 inches wide)

### Step 3: Add Captions
1. Right-click on each inserted image
2. Select "Insert Caption"
3. Use the captions provided above
4. Ensure caption numbering is sequential

### Step 4: Format Diagrams
1. Center-align all diagrams
2. Ensure consistent sizing (6-7 inches wide)
3. Add proper spacing before and after
4. Verify diagrams are referenced in the text

## 📝 Text References

Add these references in your document text:

**In Section 3.2 (System Architecture):**
"The KoinToss system follows a modular, layered architecture design as illustrated in Figure 1."

**In Section 3.3 (Component Design):**
"Figure 2 shows the detailed component interactions within the application layer."

**In Section 4.2.1 (Dual Personality Engine):**
"The personality switching process follows the workflow shown in Figure 3."

## 🎨 Formatting Guidelines

- **Image Quality:** Minimum 300 DPI for print quality
- **Size:** 6-7 inches wide, maintain aspect ratio  
- **Alignment:** Center-aligned
- **Spacing:** 12pt before and after each figure
- **Caption Format:** "Figure X: Title - Description"
- **Font:** Times New Roman, 11pt for captions

## ✅ Quality Checklist

- [ ] All three diagrams captured in high quality
- [ ] Images inserted and properly sized
- [ ] Captions added with correct numbering
- [ ] Diagrams referenced in text
- [ ] Consistent formatting throughout
- [ ] Professional appearance maintained

## 🔄 Alternative Methods

### Method 1: Print to PDF
1. Print the HTML page to PDF
2. Use PDF editing software to extract images
3. Convert to PNG format

### Method 2: Browser Developer Tools
1. Right-click on diagram → Inspect Element
2. Find the diagram container
3. Use browser screenshot tools
4. Save as PNG

### Method 3: Online Screenshot Tools
1. Use tools like Lightshot or Greenshot
2. Capture full-screen diagrams
3. Crop to diagram boundaries
4. Save in PNG format

Your diagrams are now ready for professional presentation in your FYP report!
"""
    
    return guide_content

def main():
    """Main function to create professional diagrams"""
    print("🎨 Creating professional diagrams for Word document...")
    
    # Create output directory
    output_dir = "professional_diagrams"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created directory: {output_dir}")
    
    # Create HTML diagrams
    html_content = create_simplified_html_diagrams()
    html_file = os.path.join(output_dir, "professional_diagrams_for_word.html")
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Created professional diagrams: {html_file}")
    
    # Create integration guide
    guide_content = create_word_integration_guide()
    guide_file = os.path.join(output_dir, "WORD_INTEGRATION_GUIDE.md")
    
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"✅ Created integration guide: {guide_file}")
    
    print(f"\n🎉 Professional Diagrams Ready!")
    print(f"📂 Files created in: {output_dir}/")
    print(f"🌐 Open: {html_file}")
    print(f"📖 Read: {guide_file}")
    
    print(f"\n📋 Next Steps:")
    print("1. Open professional_diagrams_for_word.html in your web browser")
    print("2. Use Windows Snipping Tool to capture each diagram")
    print("3. Save as PNG files with descriptive names")
    print("4. Insert into your Word document")
    print("5. Follow the integration guide for proper formatting")
    
    print(f"\n🎯 Result: Professional, publication-ready diagrams for your FYP report!")

if __name__ == "__main__":
    main()
