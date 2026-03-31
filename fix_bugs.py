import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Dynamic Map Image
modal_mappa_pattern = r'<div id="modal-mappa".*?>.*?<img id="mappa-img-viewer".*?>.*?</div></div>'
updated_modal_mappa = '<div id="modal-mappa" class="hidden fixed inset-0 bg-black z-[4000] flex flex-col"><div class="p-5 flex justify-between bg-slate-950 items-center"><span class="text-yellow-500 font-black text-[10px] uppercase italic">Piantina Serata</span><button onclick="toggleMappa(false)" class="bg-white text-black px-4 py-2 rounded-xl text-xs font-black uppercase italic">Esci</button></div><div class="flex-1 img-viewer overflow-auto flex items-center justify-center p-4"><img id="mappa-img-viewer" src="" class="max-w-full max-h-full object-contain"></div></div>'
content = re.sub(modal_mappa_pattern, updated_modal_mappa, content, flags=re.DOTALL)

# Update toggleMappa logic to set the URL
toggle_mappa_pattern = r'function toggleMappa\(s\) \{ document\.getElementById\(\'modal-mappa\'\)\.classList\.toggle\(\'hidden\', !s\); \}'
updated_toggle_mappa = """function toggleMappa(s) {
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
        }"""
content = re.sub(toggle_mappa_pattern, updated_toggle_mappa, content, flags=re.DOTALL)

# 2. Delete Event (Boss)
render_serate_pattern = r'(container\.innerHTML \+= `.*?<div><h3 class="font-black text-2xl uppercase italic text-white">\$\{s\.nome\}</h3><p class="text-\[10px\] text-yellow-500 font-bold uppercase italic">\$\{s\.data\}</p></div>.*?)(</span>\s*</div>\s*</div>\s*</div>`;)'
# We need to distinguish between Client view and Boss view in the future, but for now we'll just add it if the user is boss.
delete_btn_html = r'\1</span><button onclick="event.stopPropagation(); if(confirm(\'Vuoi eliminare questa serata?\')) eliminaSerata(${s.id})" class="ml-2 bg-red-600 text-white p-2 rounded-lg text-[9px] font-black uppercase shadow-lg hover:bg-red-700 transition-colors">🗑️ Elimina</button>\2'
# Let's try a different approach: wrap the card content in a template and append the button if window.userRole is boss.
# Actually, the user asked for it specifically in the 'Boss' section.
# But renderSerate is used in the landing page.
# I'll add the button but keep it hidden unless window.userRole is 'boss'.
delete_btn_html = r'\1</span><button onclick="event.stopPropagation(); if(confirm(\'Vuoi eliminare questa serata?\')) eliminaSerata(${s.id})" class="${window.userRole === \'boss\' ? \'\' : \'hidden\'} ml-2 bg-red-600 text-white p-2 rounded-lg text-[9px] font-black uppercase shadow-lg">🗑️ Elimina</button>\2'
content = re.sub(render_serate_pattern, delete_btn_html, content, flags=re.DOTALL)

# Add eliminaSerata function
js_functions = """
        async function eliminaSerata(id) {
            const { error } = await client.from('serate').delete().eq('id', id);
            if (error) {
                showToast("Errore eliminazione", "⛔");
                console.error(error);
            } else {
                showToast("Serata eliminata", "🗑️");
                fetchSerate();
            }
        }
"""
content = content.replace('async function fetchSerate()', js_functions + '\n        async function fetchSerate()')

# 3. Fix Table Booking
# The error might be because 'selectedTavolo' isn't initialized when clicking the card.
# Or in 'processaPagamentoReale' some variables are missing.
# Let's add console.log(error) to the insert call.
booking_pattern = r'(const \{ error \} = await client\.from\(\'prenotazioni\'\)\.insert\(\[\{.*?\}\]\);)'
updated_booking = r'\1\n                if(error) { console.error("SUPABASE ERROR:", error); throw error; }'
content = re.sub(booking_pattern, updated_booking, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
