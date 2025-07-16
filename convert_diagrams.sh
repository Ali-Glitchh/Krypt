#!/bin/bash
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
