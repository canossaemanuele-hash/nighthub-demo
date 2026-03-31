import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Dynamic Map Image
# Modal remains the same as previous fix but ensure we have the right ID
content = re.sub(r'<div id="modal-mappa".*?>.*?<img id="mappa-img-viewer".*?>.*?</div></div>',
                 '<div id="modal-mappa" class="hidden fixed inset-0 bg-black z-[4000] flex flex-col"><div class="p-5 flex justify-between bg-slate-950 items-center"><span class="text-yellow-500 font-black text-[10px] uppercase italic">Piantina Serata</span><button onclick="toggleMappa(false)" class="bg-white text-black px-4 py-2 rounded-xl text-xs font-black uppercase italic">Esci</button></div><div class="flex-1 img-viewer overflow-auto flex items-center justify-center p-4"><img id="mappa-img-viewer" src="" class="max-w-full max-h-full object-contain"></div></div>',
                 content, flags=re.DOTALL)

# Update toggleMappa logic
content = re.sub(r'function toggleMappa\(s\) \{.*?\}',
                 """function toggleMappa(s) {
            if(s) {
                const serata = serate.find(x => x.id === window.currentSerataId);
                const imgViewer = document.getElementById('mappa-img-viewer');
                if(serata && serata.mappa_url) {
                    imgViewer.src = serata.mappa_url;
                } else {
                    imgViewer.src = "https://i.postimg.cc/8zqmMw4B/Image-6.jpg";
                }
            }
            document.getElementById('modal-mappa').classList.toggle('hidden', !s);
        }""",
                 content, flags=re.DOTALL)

# 2. Elimina Serata (Boss Section)
# Add the list container to the Boss section
boss_section_pattern = r'(<div id="sezione-capo".*?>\s*<div class="glass p-6 rounded-3xl border-yellow-500/30">.*?</div>)'
event_list_html = r'\1\n                <div class="glass p-6 rounded-3xl border-slate-800">\n                    <h3 class="text-[10px] font-black uppercase text-slate-500 mb-4 italic text-center">📅 Lista Serate Live</h3>\n                    <div id="boss-lista-serate" class="space-y-3"></div>\n                </div>'
content = re.sub(boss_section_pattern, event_list_html, content, flags=re.DOTALL)

# Add helper function to render Boss list
render_boss_js = """
        function renderSerateBoss(data) {
            const container = document.getElementById('boss-lista-serate');
            if(!container) return;
            container.innerHTML = "";
            data.forEach(s => {
                container.innerHTML += `
                    <div class="flex justify-between items-center p-4 bg-slate-900 rounded-2xl border border-slate-800">
                        <div>
                            <p class="text-white text-xs font-black uppercase">${s.nome}</p>
                            <p class="text-[9px] text-slate-500 font-bold">${s.data}</p>
                        </div>
                        <button onclick="eliminaSerata(${s.id})" class="bg-red-600 text-white px-3 py-2 rounded-xl text-[9px] font-black uppercase shadow-lg active:scale-95 transition-transform">🗑️ Elimina</button>
                    </div>
                `;
            });
        }
"""
content = content.replace('async function fetchSerate()', render_boss_js + '\n        async function fetchSerate()')

# Update fetchSerate to call renderSerateBoss
content = re.sub(r'renderSerate\(serate\);', 'renderSerate(serate); renderSerateBoss(serate);', content)

# Add eliminaSerata function
elimina_js = """
        async function eliminaSerata(id) {
            if(!confirm("Sei sicuro di voler eliminare questa serata?")) return;
            const { error } = await client.from('serate').delete().eq('id', id);
            if (error) {
                showToast("Errore eliminazione", "⛔");
                console.error(error);
            } else {
                showToast("Serata eliminata!", "🗑️");
                fetchSerate();
            }
        }
"""
content = content.replace('async function fetchSerate()', elimina_js + '\n        async function fetchSerate()')

# 3. Fix Booking Logic
# Ensure all fields are read correctly.
# Problem might be that 'selectedTavolo' is not persisted between views if not careful.
# Or in 'processaPagamentoReale' the 'id' is missing.
# Let's add more logs and check variables.
debug_booking = r"""
            try {
                console.log("DEBUG BOOKING:", {
                    serata: window.currentSerataId,
                    tavolo: selectedTavolo,
                    cliente: window.currentUser
                });

                if(!selectedTavolo || !window.currentSerataId) {
                    throw new Error("Dati prenotazione mancanti (Tavolo o Serata)");
                }
"""
content = re.sub(r'try \{', debug_booking, content, count=1)

# Ensure console.log(error) in the insert catch/error check
content = re.sub(r'const \{ error \} = await client\.from\(\'prenotazioni\'\)\.insert\(\[\{.*?\}\]\);',
                 r'const { error } = await client.from(\'prenotazioni\').insert([{ serata_id: window.currentSerataId, tavolo_id: selectedTavolo.tavolo_id, zona: selectedTavolo.zona, prezzo: selectedTavolo.totale, cliente: document.getElementById("customer-name").value || window.currentUser, status: "Pagato", note: note, bottiglie: [], ingressi_totali: selectedTavolo.persone, ingressi_usati: 0 }]); if(error) console.error("SUPABASE INSERT ERROR:", error);',
                 content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
