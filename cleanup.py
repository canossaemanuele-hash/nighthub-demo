import re

with open('index.html', 'r') as f:
    content = f.read()

# Clean up checkLogin syntax and spacing
pattern = r"if\(email\.includes\('boss'\)\) window\.userRole = 'boss'; // Override for legacy boss.*?if \(email\.includes\('security'\)\) \{"
replacement = "if(email.includes('boss')) window.userRole = 'boss'; // Override for legacy boss\n\n                if (email.includes('security')) {"
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Remove any stray 'TableKey' or 'NightHub' missed
content = content.replace('TableKey', 'Malua 54')
content = content.replace('NightHub', 'Malua 54')

with open('index.html', 'w') as f:
    f.write(content)
