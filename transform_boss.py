import re

with open('index.html', 'r') as f:
    content = f.read()

# Modify Boss Panel HTML to include Map Upload
boss_panel_pattern = r'(<label class="text-\[9px\] uppercase text-slate-500 font-black ml-2">Locandina \(PNG/JPG\)</label>\s*<input type="file" id="event-poster".*?>)(\s*</div>\s*<button onclick="creaNuovaSerata\(\)")'
map_upload_html = r'\1<label class="text-[9px] uppercase text-slate-500 font-black ml-2 mt-2 block">Piantina Tavoli (Mappa)</label><input type="file" id="event-map" accept="image/*" class="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-[10px] file:font-black file:bg-yellow-500 file:text-black hover:file:bg-yellow-600 mb-2">\2'
content = re.sub(boss_panel_pattern, map_upload_html, content, flags=re.DOTALL)

# Modify creaNuovaSerata JS to handle Map Upload
crea_nuova_serata_pattern = r'async function creaNuovaSerata\(\) {.*?let imageUrl = null;.*?if \(fileInput\.files\.length > 0\) {.*?const { data: urlData } = client\.storage\.from\("posters"\)\.getPublicUrl\(filePath\);.*?imageUrl = urlData\.publicUrl;.*?}.*?const { error } = await client\.from\("serate"\)\.insert\(\[\{.*?\}\]\);'
updated_js = """
        async function creaNuovaSerata() {
            const title = document.getElementById("event-title").value.trim();
            const date = document.getElementById("event-date").value;
            const desc = document.getElementById("event-desc").value.trim();
            const fileInput = document.getElementById("event-poster");
            const mapInput = document.getElementById("event-map");
            const btn = document.getElementById("btn-crea-serata");

            if (!title || !date) return showToast("Titolo e Data obbligatori", "⚠️");

            btn.innerText = "PUBBLICAZIONE IN CORSO...";
            btn.disabled = true;

            let imageUrl = null;
            if (fileInput.files.length > 0) {
                const file = fileInput.files[0];
                const fileName = `${Math.random()}-${file.name}`;
                const { error: uploadError } = await client.storage.from("posters").upload(fileName, file);
                if (!uploadError) {
                    const { data: urlData } = client.storage.from("posters").getPublicUrl(fileName);
                    imageUrl = urlData.publicUrl;
                }
            }

            let mapUrl = null;
            if (mapInput.files.length > 0) {
                const file = mapInput.files[0];
                const fileName = `${Math.random()}-${file.name}`;
                const { error: uploadError } = await client.storage.from("maps").upload(fileName, file);
                if (!uploadError) {
                    const { data: urlData } = client.storage.from("maps").getPublicUrl(fileName);
                    mapUrl = urlData.publicUrl;
                }
            }

            const { error } = await client.from("serate").insert([{
                nome: title,
                data: date,
                descrizione: desc,
                immagine_url: imageUrl,
                mappa_url: mapUrl,
                attiva: true
            }]);
"""
# This is a bit complex for a simple re.sub because of the nested braces.
# Let's use a simpler marker replacement.
content = re.sub(r'async function creaNuovaSerata\(\) {.*?const { error } = await client\.from\("serate"\)\.insert\(\[\{.*?\}\]\);', updated_js, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
