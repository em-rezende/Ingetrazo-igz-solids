# Publicar no catálogo de Extensões do IngeTrazo

> **Status: preparado, ainda NÃO publicado.** O código, o empacotador, a ficha
> do catálogo e a captura de tela estão prontos, mas o repositório
> <https://github.com/em-rezende/Ingetrazo-igz-solids>, a tag `v1.0.0` e a
> GitHub Release com o asset `igz_solids.zip` **ainda não existem**. Um
> repositório git local já foi inicializado com o remote `origin` configurado;
> nada foi commitado, etiquetado ou enviado. Publique só quando o autor
> autorizar.

Este documento (PT) e a seção em inglês mais abaixo descrevem como publicar
esta extensão no catálogo <https://github.com/ingelibre/ingetrazo-extensions>
(mostrado em <https://ingetrazo.com/extensiones>).

---

## O que já está pronto

| Item | Onde | Observação |
|---|---|---|
| Código | `packaging/igz_solids/` | `__init__.py`, `_core.py`, os `tb_*.py`, `tb_list.txt`, `i18n/`, `LICENSE` e `THIRD-PARTY.md`. |
| Ícones | `icons/` (raiz) | 28 SVGs (`tb_<nome>.svg` e `tb_<nome>_light.svg`). |
| Empacotador | `packaging/build_extension.ps1` (Windows) e `packaging/build_extension.py` (multi-plataforma) | Gera um `.zip` determinístico com **uma** pasta de topo `igz_solids/`. |
| Script da Release | `packaging/publish_release.ps1` | Cria/reaproveita a Release do GitHub, envia o asset e confere o `sha256` (`-DryRun` só verifica). |
| Notas da Release | `packaging/release_notes/v1.0.0.md` | Texto publicado na Release `v1.0.0` (é o `-Notes` padrão do script). |
| Artefato | `dist/igz_solids.zip` | Já construído. **sha256** = `4ff96b9ff2e963f33da3406063cf96201d2d07e8125911959ebcf5e2a7dbc6ef`. |
| Ficha do catálogo | `ingetrazo-extensions-submission/extensions/igz_solids.toml` | Copiar para `extensions/igz_solids.toml` no repositório do catálogo. |
| Captura de tela | `ingetrazo-extensions-submission/screenshots/igz_solids.png` | Copiar para `screenshots/igz_solids.png` no repositório do catálogo (1201×750, ~68 KB). |

O `.zip` contém exatamente uma pasta de topo:

```
igz_solids/
├── __init__.py   _core.py   tb_box.py ... tb_torus.py
├── tb_list.txt
├── i18n/            # en.json, es.json, pt-BR.json, it.json
├── icons/           # tb_<nome>.svg e tb_<nome>_light.svg
├── LICENSE
├── README.md
├── README_ptBR.md
└── THIRD-PARTY.md
```

O catálogo instala **um arquivo por extensão**: um `.py`, ou um `.zip` com
**uma** pasta contendo um `__init__.py` (ver `TEMPLATE.toml` no repositório do
catálogo). Por isso esta extensão, que traz vários módulos, uma pasta `i18n/`
e uma pasta de ícones, usa o formato `.zip`.

---

## Passos para publicar (quando autorizar)

1. **Confirme as alterações locais e faça o commit.**
   ```powershell
   git add -A
   git commit -m "chore: release 1.0.0 of igz_solids for the IngeTrazo catalog"
   ```
2. **(Só se o código mudou) reconstrua:** `packaging\build_extension.ps1` e
   copie o `sha256` impresso para `extensions/igz_solids.toml`.
3. `git push origin main`, depois `git tag v1.0.0` e `git push origin v1.0.0`.
4. Crie a **GitHub Release `v1.0.0`** com o asset `dist/igz_solids.zip` (nome
   exatamente `igz_solids.zip`). Prefira o script:
   `packaging\publish_release.ps1 -Tag v1.0.0` (as notas vêm de
   `packaging\release_notes\v1.0.0.md`); `-DryRun` faz só a verificação, sem
   alterar nada. Ele é idempotente (reaproveita a Release da tag e só reescreve
   o texto quando difere), lê o token do Git Credential Manager e confere o
   sha256.
5. Em <https://github.com/ingelibre/ingetrazo-extensions>, copie
   `ingetrazo-extensions-submission/extensions/igz_solids.toml` para
   `extensions/igz_solids.toml` e
   `ingetrazo-extensions-submission/screenshots/igz_solids.png` para
   `screenshots/igz_solids.png` (no browser: *Add file ▸ Create new file* e
   *Add file ▸ Upload files*), e abra a pull request.
6. Preencha o checklist do template. A extensão não usa rede, não executa
   programas externos e não apaga arquivos.

O **sha256** da ficha
(`4ff96b9ff2e963f33da3406063cf96201d2d07e8125911959ebcf5e2a7dbc6ef`) é a
impressão digital do `dist/igz_solids.zip`; tem de coincidir exatamente com o
asset enviado.

---

## Notas úteis

- **Tags** do catálogo: a lista fixa inclui `drawing`, `structures`,
  `productivity`, `rendering`, `analysis`, `import-export`, `terrain`,
  `education`, `other`. Esta ficha usa `drawing`, `structures` e
  `productivity`.
- **Captura de tela**: 1201×750 px (~68 KB). A sugestão do catálogo é
  ~1200×750 e o limite é 600 KB, então há folga.
- **Uma ficha por extensão**: se preferir separar em várias entradas (por
  família de sólidos), cada uma precisaria do seu próprio arquivo baixável
  (e os ícones iriam junto, de novo via `.zip`). A entrada única é mais simples.

---

# Publishing to the IngeTrazo extension catalog (EN)

> **Status: prepared, NOT yet published.** The code, the builder, the catalog
> entry and the screenshot are ready, but the repository
> <https://github.com/em-rezende/Ingetrazo-igz-solids>, the `v1.0.0` tag and the
> GitHub Release carrying `igz_solids.zip` **do not exist yet**. A local git
> repository has been initialised with the `origin` remote configured; nothing
> has been committed, tagged or pushed. Publish only when the author authorises
> it.

Everything needed is in place (clean code, a `.zip` builder, the entry file and
a screenshot). To publish, once you authorise it:

1. Commit locally (`git add -A; git commit -m "chore: release 1.0.0 ..."`).
2. (Only if the code changed) rebuild: `packaging\build_extension.ps1` and copy
   the printed `sha256` into the entry.
3. `git push origin main`, then `git tag v1.0.0` and `git push origin v1.0.0`.
4. Create the **v1.0.0** GitHub Release and attach `dist/igz_solids.zip` as an
   asset named exactly `igz_solids.zip`. Prefer
   `packaging\publish_release.ps1 -Tag v1.0.0` over the web UI (the notes come
   from `packaging\release_notes\v1.0.0.md`), plus `-DryRun` for a read-only
   check and `-Force` to upload again an asset that is already in place. It is
   idempotent, reads the token from Git Credential Manager and verifies the
   sha256.
5. In <https://github.com/ingelibre/ingetrazo-extensions>, copy
   `ingetrazo-extensions-submission/extensions/igz_solids.toml` to
   `extensions/igz_solids.toml` and
   `ingetrazo-extensions-submission/screenshots/igz_solids.png` to
   `screenshots/igz_solids.png`, then **Create pull request**.
6. Fill in the PR template checklist and answer the prompts (the extension uses
   no network by itself, runs no external programs and deletes no files).

The **sha256** in the entry
(`4ff96b9ff2e963f33da3406063cf96201d2d07e8125911959ebcf5e2a7dbc6ef`) is the
fingerprint of `dist/igz_solids.zip` as built by the script. It **must** match
the uploaded asset; if you rebuild, update the value.
