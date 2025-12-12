import yaml
import os

def load_projects():
    if os.path.exists('projects/projects.yml'):
        with open('projects/projects.yml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return []

def generate_featured_markdown(projects):
    featured = [p for p in projects if p.get('status') == 'featured']
    featured = featured[:6]
    
    # HTML Table Layout for Maximum Visual Impact
    md = "## Proyectos Destacados\n\n"
    
    for p in featured:
        name = p['name']
        desc = p['desc']
        demo = p.get('demo', '#')
        repo = p.get('repo', '#')
        preview = p.get('preview', '')
        tech = " \u00B7 ".join(p.get('tech', []))
        
        # Badges
        play_btn = f"<a href='{demo}'><img src='https://img.shields.io/badge/JUGAR_AHORA-38bdf8?style=for-the-badge&logo=google-chrome&logoColor=white' height='28'></a>"
        repo_btn = f"<a href='{repo}'><img src='https://img.shields.io/badge/CÓDIGO-181717?style=for-the-badge&logo=github&logoColor=white' height='28'></a>"
        
        # Visual Card Row
        md += "<table>\n"
        md += "  <tr>\n"
        md += f"    <td width='50%' valign='top'>\n"
        md += f"      <a href='{demo}'>\n"
        md += f"        <img src='{preview}' alt='Preview {name}' width='100%'>\n"
        md += "      </a>\n"
        md += "    </td>\n"
        md += f"    <td valign='top'>\n"
        md += f"      <h3 style='margin-top:0'>{name}</h3>\n"
        md += f"      <p>{desc}</p>\n"
        md += f"      <p><b>Tech:</b> <code>{tech}</code></p>\n"
        md += f"      <br>\n"
        md += f"      {play_btn} &nbsp; {repo_btn}\n"
        md += "    </td>\n"
        md += "  </tr>\n"
        md += "</table>\n<br>\n\n"
        
    return md

def generate_catalog_markdown(projects):
    md = "# \uD83D\uDCC1 Catálogo Completo\n\n"
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

    featured_md = generate_featured_markdown(projects)
    
    readme_path = 'README.md'
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        start = "<!-- PROJECTS:START -->"
        end = "<!-- PROJECTS:END -->"
        
        if start in content and end in content:
            pre = content.split(start)[0]
            post = content.split(end)[1]
            new_content = f"{pre}{start}\n{featured_md}{end}{post}"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
    with open('projects/README.md', 'w', encoding='utf-8') as f:
        f.write(generate_catalog_markdown(projects))

if __name__ == "__main__":
    main()
