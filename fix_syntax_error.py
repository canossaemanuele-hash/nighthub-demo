import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix the broken HTML template at line 611
# The issue was likely escaped quotes or character encoding in the template literal.
pattern = r'<span class="bg-green-500 text-black text-\[9px\] font-black px-3 py-1 rounded-full">LIVE</span><button onclick="event\.stopPropagation\(\); if\(confirm\(\\\'Vuoi eliminare questa serata\?\\\Headererera.*?</button></span>'
# Let's use a simpler marker based search to replace the whole line correctly.

old_line = '<span class="bg-green-500 text-black text-[9px] font-black px-3 py-1 rounded-full">LIVE</span><button onclick="event.stopPropagation(); if(confirm(\\\'Vuoi eliminare questa serata?\\\')) eliminaSerata(${s.id})" class="${window.userRole === \\\'boss\\\' ? \\\'\\\' : \\\'hidden\\\'} ml-2 bg-red-600 text-white p-2 rounded-lg text-[9px] font-black uppercase shadow-lg">🗑️ Elimina</button></span>'

# Actually looking at the 'sed' output from before:
# <span class="bg-green-500 text-black text-[9px] font-black px-3 py-1 rounded-full">LIVE</span><button onclick="event.stopPropagation(); if(confirm(\'Vuoi eliminare questa serata?\')) eliminaSerata(${s.id})" class="${window.userRole === \'boss\' ? \'\' : \'hidden\'} ml-2 bg-red-600 text-white p-2 rounded-lg text-[9px] font-black uppercase shadow-lg">🗑️ Elimina</button></span>

new_line = '<span class="bg-green-500 text-black text-[9px] font-black px-3 py-1 rounded-full">LIVE</span><button onclick="event.stopPropagation(); if(confirm(\'Vuoi eliminare questa serata?\')) eliminaSerata(${s.id})" class="${window.userRole === \'boss\' ? \'\' : \'hidden\'} ml-2 bg-red-600 text-white p-2 rounded-lg text-[9px] font-black uppercase shadow-lg">🗑️ Elimina</button></span>'

# Since there are backslashes from my previous python script that might have been literal:
content = content.replace('\\\'', "'")

with open('index.html', 'w') as f:
    f.write(content)
