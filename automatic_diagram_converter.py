"""
Automatic Mermaid Diagram to Image Converter
Converts Mermaid diagrams to PNG images using online services.
"""

import requests
import base64
import json
import os
import time
from urllib.parse import quote

def read_mermaid_file(filepath):
    """Read Mermaid diagram content from file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().strip()

def convert_mermaid_to_image_kroki(mermaid_code, output_path, diagram_name):
    """Convert Mermaid to PNG using Kroki service"""
    try:
        # Encode the diagram
        encoded = base64.urlsafe_b64encode(mermaid_code.encode('utf-8')).decode('ascii')
        
        # Create Kroki URL
        kroki_url = f"https://kroki.io/mermaid/png/{encoded}"
        
        print(f"Converting {diagram_name} using Kroki...")
        response = requests.get(kroki_url, timeout=30)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Successfully created {output_path}")
            return True
        else:
            print(f"❌ Kroki conversion failed for {diagram_name}: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error converting {diagram_name} with Kroki: {e}")
        return False

def convert_mermaid_to_image_mermaid_ink(mermaid_code, output_path, diagram_name):
    """Convert Mermaid to PNG using mermaid.ink service"""
    try:
        # Encode the diagram for URL
        encoded = base64.b64encode(mermaid_code.encode('utf-8')).decode('ascii')
        
        # Create mermaid.ink URL
        mermaid_ink_url = f"https://mermaid.ink/img/{encoded}"
        
        print(f"Converting {diagram_name} using mermaid.ink...")
        response = requests.get(mermaid_ink_url, timeout=30)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Successfully created {output_path}")
            return True
        else:
            print(f"❌ mermaid.ink conversion failed for {diagram_name}: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error converting {diagram_name} with mermaid.ink: {e}")
        return False

def create_html_with_images(diagrams_info, output_dir):
    """Create an HTML file showing all converted diagrams"""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>KoinToss FYP - Converted Diagrams</title>
    <style>
        body {{ 
            font-family: 'Times New Roman', serif; 
            margin: 40px; 
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ 
            color: #2c3e50; 
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .diagram-section {{ 
            margin: 40px 0; 
            padding: 20px; 
            border: 2px solid #ecf0f1;
            border-radius: 8px;
            background-color: #fafafa;
        }}
        .diagram-title {{ 
            color: #34495e; 
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        .diagram-image {{ 
            text-align: center; 
            margin: 20px 0;
            padding: 15px;
            background-color: white;
            border-radius: 5px;
        }}
        .diagram-image img {{ 
            max-width: 100%; 
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .diagram-description {{
            background-color: #e8f4fd;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin: 15px 0;
            font-style: italic;
        }}
        .usage-instructions {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 20px;
            margin: 30px 0;
        }}
        .usage-instructions h3 {{
            color: #856404;
            margin-top: 0;
        }}
        .file-info {{
            font-size: 12px;
            color: #666;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>KoinToss FYP Report - System Diagrams</h1>
        
        <div class="usage-instructions">
            <h3>📋 How to Use These Diagrams in Your Word Document</h3>
            <ol>
                <li>Right-click on any diagram image below and select "Save image as..."</li>
                <li>Save the image with a descriptive name (e.g., "Figure1_SystemArchitecture.png")</li>
                <li>In your Word document, find the diagram placeholder</li>
                <li>Insert the image: Insert → Pictures → This Device</li>
                <li>Add a caption: Right-click → Insert Caption → "Figure X: [Description]"</li>
                <li>Resize and center the image as needed</li>
            </ol>
        </div>
"""
    
    for i, (filename, diagram_type, description) in enumerate(diagrams_info, 1):
        image_filename = filename.replace('.mmd', '.png')
        
        html_content += f"""
        <div class="diagram-section">
            <div class="diagram-title">Figure {i}: {diagram_type}</div>
            
            <div class="diagram-description">
                {description}
            </div>
            
            <div class="diagram-image">
                <img src="{image_filename}" alt="{diagram_type}" />
                <div class="file-info">Image file: {image_filename}</div>
            </div>
        </div>
"""
    
    html_content += """
        <div class="usage-instructions">
            <h3>📝 Suggested Figure Captions for Word Document</h3>
            <ul>
                <li><strong>Figure 1:</strong> KoinToss System Architecture - Overview of the modular, layered architecture showing frontend, application, core services, data layer, and external API integration.</li>
                <li><strong>Figure 2:</strong> High-Level System Components - Detailed view of the application layer components including personality manager, training manager, and API manager with their interconnections.</li>
                <li><strong>Figure 3:</strong> Dual Personality Flow Diagram - Process flow showing how user input is parsed, routed to appropriate personality trainer, and response generation workflow.</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin-top: 40px; padding: 20px; border-top: 2px solid #ecf0f1;">
            <p style="color: #7f8c8d; font-style: italic;">
                Generated on {time.strftime('%B %d, %Y at %I:%M %p')}<br>
                KoinToss FYP Report - Diagram Conversion Complete
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    html_file = os.path.join(output_dir, "converted_diagrams_gallery.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Created diagram gallery: {html_file}")

def main():
    """Main conversion function"""
    print("🔄 Starting automatic Mermaid diagram conversion...")
    
    # Define diagrams with descriptions
    diagrams_info = [
        ("diagram_1_graph.mmd", "System Architecture Overview", 
         "This diagram illustrates the comprehensive system architecture of KoinToss, showing the modular design with distinct layers for frontend, application logic, core services, data management, and external API integration."),
        
        ("diagram_2_graph.mmd", "High-Level System Components", 
         "Detailed component diagram showing the internal structure of the application layer, including the personality manager, training manager, and API manager components with their data flow relationships."),
        
        ("diagram_3_flowchart.mmd", "Dual Personality Processing Flow", 
         "Process flowchart demonstrating the dual personality system's decision-making process, from user input parsing through personality detection, routing, and response generation.")
    ]
    
    input_dir = "mermaid_diagrams"
    output_dir = "converted_diagrams"
    
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created output directory: {output_dir}")
    
    successful_conversions = []
    
    # Convert each diagram
    for filename, diagram_type, description in diagrams_info:
        input_path = os.path.join(input_dir, filename)
        output_filename = filename.replace('.mmd', '.png')
        output_path = os.path.join(output_dir, output_filename)
        
        if not os.path.exists(input_path):
            print(f"❌ Warning: {input_path} not found, skipping...")
            continue
        
        # Read Mermaid content
        mermaid_code = read_mermaid_file(input_path)
        print(f"\n📊 Processing {diagram_type}...")
        
        # Try multiple conversion services
        success = False
        
        # Try Kroki first
        if convert_mermaid_to_image_kroki(mermaid_code, output_path, diagram_type):
            success = True
        # Try mermaid.ink as fallback
        elif convert_mermaid_to_image_mermaid_ink(mermaid_code, output_path, diagram_type):
            success = True
        
        if success:
            successful_conversions.append((filename, diagram_type, description))
            print(f"✅ {diagram_type} converted successfully!")
        else:
            print(f"❌ Failed to convert {diagram_type}")
    
    # Create HTML gallery
    if successful_conversions:
        create_html_with_images(successful_conversions, output_dir)
        
        print(f"\n🎉 Conversion Complete!")
        print(f"📊 Successfully converted {len(successful_conversions)} diagrams")
        print(f"📁 Images saved in: {output_dir}/")
        print(f"🌐 View gallery: {output_dir}/converted_diagrams_gallery.html")
        
        print("\n📋 Next Steps:")
        print("1. Open converted_diagrams_gallery.html in your web browser")
        print("2. Right-click and save each diagram image")
        print("3. Insert images into your Word document")
        print("4. Add appropriate figure captions")
        print("5. Ensure images are properly sized and centered")
        
    else:
        print("\n❌ No diagrams were successfully converted.")
        print("You may need to convert them manually using:")
        print("- https://mermaid.live/ (recommended)")
        print("- VS Code with Mermaid extensions")

if __name__ == "__main__":
    main()
