# Vegamente — sito statico

Guida italiana ai prodotti vegan (cibo, moda, cosmetici, casa, animali). Sito statico: nessun database, nessun WordPress, si pubblica con un push su GitHub.

## Struttura

```
assets/     CSS, JS, logo e favicon (copiati in public/assets)
content/    una pagina per file: intestazione tra --- + corpo HTML
build.py    genera public/ (pagine, sitemap.xml, robots.txt)
public/     il sito pronto da pubblicare (generato, non modificare a mano)
```

## Aggiungere una pagina

1. Crea `content/NN-nome.html` con questa intestazione:
   ```
   ---
   title: Titolo della pagina
   description: Descrizione per Google (max 155 caratteri)
   path: /categoria/slug/
   ---
   <article class="article"> ... </article>
   ```
2. Esegui `python3 build.py`.
3. Commit e push: Hostinger pubblica in automatico.

Per una guida prodotto, copia `content/21-scarpe-vegan-uomo.html` e sostituisci i segnaposto tra parentesi quadre.

## Pubblicare su Hostinger tramite GitHub

1. Crea un repository su GitHub (es. `vegamente`) e caricaci questa cartella, inclusa `public/`.
2. In hPanel di Hostinger: **Siti web → vegamente.it → Avanzate → GIT**.
3. Incolla l'URL del repository (HTTPS; per repo privati aggiungi la chiave SSH mostrata da Hostinger come Deploy key su GitHub).
4. Branch: `main`. Directory: `public_html`.
5. Dopo il primo deploy, in **Avanzate → GIT → Auto deployment** copia il webhook e incollalo su GitHub in *Settings → Webhooks* del repository: da quel momento ogni push aggiorna il sito.
6. Hostinger copia l'intero repository in `public_html`: perché il sito serva i file di `public/` devi fare una di queste due cose:
   - **Opzione semplice:** in hPanel, *Siti web → Gestisci → Cartella principale* imposta la root del dominio a `public_html/public`.
   - **Opzione alternativa:** crea un file `.htaccess` in `public_html` con:
     ```
     RewriteEngine On
     RewriteCond %{REQUEST_URI} !^/public/
     RewriteRule ^(.*)$ /public/$1 [L]
     ```
7. Attiva il certificato SSL gratuito in **Sicurezza → SSL** e forza HTTPS.

Nota: i passaggi del pannello Hostinger possono cambiare nome; se qualcosa non corrisponde, cerca "Git" nella barra di ricerca di hPanel.

## Da completare prima di andare online

Cerca nei file di `content/` i segnaposto tra parentesi quadre `[...]`: nome autore, email, P.IVA, URL del modulo newsletter (MailerLite), testi privacy. Poi:

- [ ] Collegare Google Search Console e inviare `https://vegamente.it/sitemap.xml`
- [ ] Inserire lo script di statistiche in `assets/site.js` dentro il click su "Accetto"
- [ ] Sostituire i prodotti segnaposto nella guida scarpe con quelli verificati
- [ ] Iscriversi ad Amazon Affiliati e Awin e inserire i link
