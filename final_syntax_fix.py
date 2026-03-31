import re

with open('index.html', 'r') as f:
    content = f.read()

# The issue is likely how the onclick string is handled within the template literal.
# Incorrect: onclick="confirm('...')"
# Let's use double quotes for the inner string or escape correctly.

pattern = r'<span class="bg-green-500 text-black text-\[9px\] font-black px-3 py-1 rounded-full">LIVE</span><button onclick="event\.stopPropagation\(\); if\(confirm\(.*?\)\) eliminaSerata\(\$\{s\.id\}\)" class="\$\{window\.userRole === \'boss\' \? \'\' : \'hidden\'\} ml-2 bg-red-600 text-white p-2 rounded-lg text-\[9px\] font-black uppercase shadow-lg">🗑️ Elimina</button></span>'

correct_line = '<span class="bg-green-500 text-black text-[9px] font-black px-3 py-1 rounded-full">LIVE</span><button onclick="event.stopPropagation(); if(confirm(\'Vuoi eliminare questa serata?\')) eliminaSerata(${s.id})" class="${window.userRole === \'boss\' ? \'\' : \'hidden\'} ml-2 bg-red-600 text-white p-2 rounded-lg text-[9px] font-black uppercase shadow-lg">🗑️ Elimina</button></span>'

# Actually, let's just rewrite the whole renderSerate function to be safe.
render_serate_func = """
        function renderSerate(serate) {
            const container = document.getElementById('lista-serate');
            if (!container) return;
            container.innerHTML = "";
            if (serate.length === 0) {
                container.innerHTML = '<p class="text-[10px] text-slate-600 text-center py-10 italic uppercase font-black">Nessuna serata in programma.</p>';
                return;
            }
            serate.forEach(s => {
                const img = s.immagine_url || 'https://images.unsplash.com/photo-1574094939582-9357dedc6361?auto=format&fit=crop&w=600&q=80';
                const deleteBtn = window.userRole === 'boss' ? `<button onclick="event.stopPropagation(); if(confirm('Vuoi eliminare questa serata?')) eliminaSerata(${s.id})" class="ml-2 bg-red-600 text-white p-2 rounded-lg text-[9px] font-black uppercase shadow-lg">🗑️ Elimina</button>` : '';

                container.innerHTML += `
                    <div onclick="entraNelLocale('${s.nome}', ${s.id})" class="relative cursor-pointer overflow-hidden rounded-3xl md:rounded-[2.5rem] border border-yellow-500/40 bg-slate-900 shadow-2xl active:scale-95 transition-transform">
                        <div class="h-44 bg-cover bg-center opacity-70" style="background-image: url('${img}');"></div>
                        <div class="p-6 absolute bottom-0 left-0 right-0 glass rounded-t-[2rem]">
                            <div class="flex justify-between items-center">
                                <div><h3 class="font-black text-2xl uppercase italic text-white">${s.nome}</h3><p class="text-[10px] text-yellow-500 font-bold uppercase italic">${s.data}</p></div>
                                <span class="flex items-center gap-2">
                                    <span class="bg-green-500 text-black text-[9px] font-black px-3 py-1 rounded-full">LIVE</span>
                                    ${deleteBtn}
                                </span>
                            </div>
                        </div>
                    </div>`;
            });
        }
"""

content = re.sub(r'function renderSerate\(serate\) \{.*?\}', render_serate_func, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
