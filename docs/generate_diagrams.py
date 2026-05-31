"""
Utility script to generate design diagrams for the EdTech platform.

This script uses networkx and matplotlib to draw three diagrams:

1. Logical Data Design (LDD): Shows the entities (User, Course, Enrollment,
   Payment, Review, Certification) and their relationships.
2. High‑Level Design (HDD): Illustrates the major components of the system,
   including the frontend, backend, database and AI services.
3. System Design Diagram (SDD): Breaks down the backend into functional
   modules and shows their interactions with the database and external AI
   components.

Run this script with::

    python generate_diagrams.py

The images will be saved in the same directory as PNG files.
"""

import os
import matplotlib.pyplot as plt
import networkx as nx


def draw_ldd(output_path: str):
    """Draw the Logical Data Design (entity‑relationship diagram)."""
    G = nx.DiGraph()

    # Define entity nodes
    entities = [
        "User", "Course", "Enrollment", "Payment", "Review", "Certification"
    ]
    for ent in entities:
        G.add_node(ent)

    # Define relationships (directed for clarity)
    G.add_edge("Enrollment", "User", label="student_id")
    G.add_edge("Enrollment", "Course", label="course_id")
    G.add_edge("Enrollment", "Payment", label="payment_id")
    G.add_edge("Payment", "User", label="student_id")
    G.add_edge("Payment", "Course", label="course_id")
    G.add_edge("Review", "User", label="student_id")
    G.add_edge("Review", "Course", label="course_id")
    G.add_edge("Certification", "User", label="student_id")
    G.add_edge("Certification", "Course", label="course_id")
    G.add_edge("Course", "User", label="instructor_id")

    pos = nx.spring_layout(G, seed=42, k=1)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color="#a3c1da", node_size=3000, font_size=10, arrowsize=20)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.title("Logical Data Design (LDD)")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def draw_hdd(output_path: str):
    """Draw the High‑Level Design diagram."""
    G = nx.DiGraph()
    components = [
        "Frontend (Web UI)",
        "FastAPI Backend",
        "Database (SQLite/PostgreSQL)",
        "AI Services (Models & Research)"
    ]
    for comp in components:
        G.add_node(comp)
    # Connections
    G.add_edge("Frontend (Web UI)", "FastAPI Backend", label="HTTP/REST")
    G.add_edge("FastAPI Backend", "Database (SQLite/PostgreSQL)", label="SQLAlchemy")
    G.add_edge("FastAPI Backend", "AI Services (Models & Research)", label="API Calls")

    pos = {
        "Frontend (Web UI)": (-1, 0),
        "FastAPI Backend": (0, 0),
        "Database (SQLite/PostgreSQL)": (1, 0.5),
        "AI Services (Models & Research)": (1, -0.5)
    }
    plt.figure(figsize=(8, 4))
    nx.draw(G, pos, with_labels=True, node_color="#cdebc7", node_size=3500, font_size=9, arrowsize=20)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.title("High‑Level Design (HDD)")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def draw_sdd(output_path: str):
    """Draw the System Design Diagram."""
    G = nx.DiGraph()
    # Modules inside the backend
    modules = [
        "User Service",
        "Course Service",
        "Enrollment Service",
        "Payment Service",
        "Review Service",
        "Certification Service",
        "AI Module"
    ]
    for mod in modules:
        G.add_node(mod)

    # Add external components
    G.add_node("Database")
    G.add_node("AI Models & Search")

    # Connect services to the database
    for mod in modules:
        if mod != "AI Module":
            G.add_edge(mod, "Database", label="ORM")
    # AI Module interacts with AI Models
    G.add_edge("AI Module", "AI Models & Search", label="API")

    # Basic interactions between services
    G.add_edge("Enrollment Service", "User Service")
    G.add_edge("Enrollment Service", "Course Service")
    G.add_edge("Payment Service", "Enrollment Service")
    G.add_edge("Review Service", "User Service")
    G.add_edge("Review Service", "Course Service")
    G.add_edge("Certification Service", "Enrollment Service")
    G.add_edge("Certification Service", "Course Service")

    pos = nx.spring_layout(G, seed=24, k=1)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color="#f9e79f", node_size=3000, font_size=8, arrowsize=15)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    plt.title("System Design Diagram (SDD)")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    os.makedirs('images', exist_ok=True)
    draw_ldd('images/ldd.png')
    draw_hdd('images/hdd.png')
    draw_sdd('images/sdd.png')
    print("Diagrams generated in the 'images' directory.")


if __name__ == '__main__':
    main()