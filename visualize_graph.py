import sys
import os
sys.path.append(os.path.join(os.getcwd(), "src"))

from agent.graph.agent import MonteAzulAgent

def visualize():
    try:
        agent = MonteAzulAgent()
        # Generate the mermaid graph in PNG format
        png_data = agent.get_graph_image()
        
        # Save to a file
        output_path = os.path.join(os.getcwd(), "graph_viz.png")
        with open(output_path, "wb") as f:
            f.write(png_data)
        
        print(f"Graph visualization saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Could not generate PNG: {e}")
        print("Mermaid graph code:")
        print(graph.get_graph().draw_mermaid())
        return None

if __name__ == "__main__":
    visualize()
