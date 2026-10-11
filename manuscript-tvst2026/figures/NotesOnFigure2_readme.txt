In the manuscript (Google Docs): 
insert Figure2_mapping_decision_logic.png (300 dpi) using Insert → Image → Upload from computer.
For the vector PDF: use the Figure2_mapping_decision_logic.pdf that was generated.

Graphviz generated it directly from the .dot file, so it’s cropped to the diagram and sharp at any size. Replace your PowerPoint-exported PDF with it.
On GitHub: commit the .dot, my PDF and the PNG. Leave out the .pptx, because it adds nothing the .dot file doesn’t do better.

To edit Figure 2 later, 
change the text in the .dot file and rerun 
>> dot -Tpdf Figure2_mapping_decision_logic.dot -o Figure2_mapping_decision_logic.pdf. Or you can have claude re-render it. 


check-in the .dot, .pdf, .png, and .tiff files to the GitHub under the manuscript figures directory.