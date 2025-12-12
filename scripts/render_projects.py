import yaml
import os

def load_projects():
    # Only run if file exists
    if os.path.exists('projects/projects.yml'):
        with open('projects/projects.yml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return []

def generate_featured_markdown(projects):
    featured = [p for p in projects if p.get('status') == 'featured']
    featured = featured[:6]
    
    md = "### \u2B50 Proyectos Destacados (Featured)\n\n"
    # Grid using table
    md += "| Proyecto | Detalles | Preview |\n"
    md += "| :--- | :--- | :---: |\n"
    
    for p in featured:
        name = p['name']
        desc = p['desc']
        demo = p.get('demo', '#')
        repo = p.get('repo', '#')
        preview = p.get('preview', '')
        
        tech_txt = " ".join([f"`{t}`" for t in p.get('tech', [])])
        
        # Badges
        badges = f"[<img src='https://img.shields.io/badge/GitHub-Repo-181717?style=flat-square&logo=github&logoColor=white' height='20'>]({repo})"
        if demo and demo != "#":
            badges += f" [<img src='https://img.shields.io/badge/Live-Demo-38bdf8?style=flat-square&logo=google-chrome&logoColor=white' height='20'>]({demo})"
            
        preview_img = ""
        if preview:
            preview_img = f"<img src='{preview}' width='200'>"
            
        md += f"| **{name}**<br>{desc}<br><br>{tech_txt}<br>{badges} | {preview_img} |\n"
        
    return md

def generate_catalog_markdown(projects):
    md = "# \uD83D\uDCC1 Catálogo Completo de Proyectos\n\n"
    md += "[< Volver al Perfil Principal](../README.md)\n\n"
    
    grouped = {}
    for p in projects:
        s = p.get('status', 'other')
        if s not in grouped: grouped[s] = []
        grouped[s].append(p)
        
    order = ['featured', 'active', 'completed', 'planned', 'archived']
    
    for s in order:
        if s in grouped:
            md += f"## {s.title()}\n"
            for p in grouped[s]:
                md += f"- **{p['name']}**: {p['desc']}\n"
                md += f"  - Repo: {p['repo']}\n"
                md += f"  - Demo: {p['demo']}\n\n"
    return md

def main():
    projects = load_projects()
    if not projects: return

    # Featured
    featured_md = generate_featured_markdown(projects)
    
    # Update README
    readme_path = 'README.md'
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        start = "<!-- PROJECTS:START -->"
        end = "<!-- PROJECTS:END -->"
        
        if start in content and end in content:
            pre = content.split(start)[0]
            post = content.split(end)[1]
            new_content = f"{pre}{start}\n{featured_md}\n{end}{post}"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
    # Create Catalog
    with open('projects/README.md', 'w', encoding='utf-8') as f:
        f.write(generate_catalog_markdown(projects))

if __name__ == "__main__":
    main()
