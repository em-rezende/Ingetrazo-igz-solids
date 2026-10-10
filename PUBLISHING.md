# Publicar no catálogo de Extensões do IngeTrazo

> **Status: publicado no GitHub e SUBMETIDO ao catálogo (PR #69, aberta).**
> O repositório <https://github.com/em-rezende/Ingetrazo-igz-solids> está
> publicado (branch `main`), com a tag `v1.0.0` e a **Release `igz_solids 1.0.0`**
> a servir o asset `igz_solids.zip` (sha256 conferido). A submissão foi enviada
> em 2026-10-10: <https://github.com/ingelibre/ingetrazo-extensions/pull/69> —
> o `check` automático passou. Como `igz_solids` é uma entrada **nova**, o
> *automerge* (que só funde versões novas de extensões já listadas) não se
> aplica: aguarda a revisão de um mantenedor.

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
| Artefato | `dist/igz_solids.zip` | Já construído. **sha256** = `9bc82a17b203d43aa770a19d573bdb197797cdeb3ab49cc11e2c2f5a7ac7a4c8`. |
| Release publicada | <https://github.com/em-rezende/Ingetrazo-igz-solids/releases/tag/v1.0.0> | `igz_solids 1.0.0` (id `409135616`), publicada em 2026-10-10; asset `igz_solids.zip` com 138 030 bytes e o sha256 acima (conferido pelo `digest` da API). |
| Ficha do catálogo | `ingetrazo-extensions-submission/extensions/igz_solids.toml` | Copiar para `extensions/igz_solids.toml` no repositório do catálogo. |
| Captura de tela | `ingetrazo-extensions-submission/screenshots/igz-solids.png` | Copiar para `screenshots/igz-solids.png` no repositório do catálogo (1200×750, ~96 KB). |

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

A extensão cumpre as regras de
[`docs/plugins.md`](https://github.com/ingelibre/ingetrazo/blob/main/docs/plugins.md)
(pacote com `__init__.py`, isolamento de erros, imports relativos sem
`sys.path`, mutações apenas pela camada de comandos e `setup(app)` da API 2);
a tabela de conformidade, regra a regra, está em
[`ingetrazo-extensions-submission/README.md`](ingetrazo-extensions-submission/README.md).

---

## Passos para publicar (quando autorizar)

> Os passos **1–6 já foram executados**: commits, tag `v1.0.0`, `push`, Release
> com o asset verificada, e a submissão ao catálogo — **PR #69**
> (<https://github.com/ingelibre/ingetrazo-extensions/pull/69>), aberta em
> 2026-10-10 com o `check` automático limpo. Como a entrada é nova, aguarda a
> revisão de um mantenedor (o *automerge* só funde versões novas de extensões já
> listadas).

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
   `ingetrazo-extensions-submission/screenshots/igz-solids.png` para
   `screenshots/igz-solids.png` (no browser: *Add file ▸ Create new file* e
   *Add file ▸ Upload files*), e abra a pull request.
6. Preencha o checklist do template. A extensão não usa rede, não executa
   programas externos e não apaga arquivos.

O **sha256** da ficha
(`9bc82a17b203d43aa770a19d573bdb197797cdeb3ab49cc11e2c2f5a7ac7a4c8`) é a
impressão digital do `dist/igz_solids.zip`; tem de coincidir exatamente com o
asset enviado.

---

## Notas úteis

- **Tags** do catálogo: a lista fixa inclui `drawing`, `structures`,
  `productivity`, `rendering`, `analysis`, `import-export`, `terrain`,
  `education`, `other`. Esta ficha usa `drawing`, `structures` e
  `productivity`.
- **Captura de tela**: 1200×750 px (~96 KB). A sugestão do catálogo é
  ~1200×750 e o limite é 600 KB, então há folga.
- **Uma ficha por extensão**: se preferir separar em várias entradas (por
  família de sólidos), cada uma precisaria do seu próprio arquivo baixável
  (e os ícones iriam junto, de novo via `.zip`). A entrada única é mais simples.

---

# Publishing to the IngeTrazo extension catalog (EN)

> **Status: published on GitHub and SUBMITTED to the catalogue (PR #69, open).**
> The repository <https://github.com/em-rezende/Ingetrazo-igz-solids> is live
> (`main`), with the `v1.0.0` tag and the **`igz_solids 1.0.0` Release** serving
> the `igz_solids.zip` asset (sha256 verified). The submission went in on
> 2026-10-10: <https://github.com/ingelibre/ingetrazo-extensions/pull/69> — the
> automatic `check` passed. As `igz_solids` is a **new** entry, the *automerge*
> rule (which only takes new versions of extensions already listed) does not
> apply: it awaits a maintainer's review.

Everything is done: steps 1–6 (commits, tag `v1.0.0`, push, the Release with a
verified asset, and the catalogue submission — **PR #69**,
<https://github.com/ingelibre/ingetrazo-extensions/pull/69>, opened on
2026-10-10 with a clean `check`). As the entry is new, it awaits a maintainer's
review (the *automerge* rule only takes new versions of extensions already
listed).

For reference, the steps were:

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
   `ingetrazo-extensions-submission/screenshots/igz-solids.png` to
   `screenshots/igz-solids.png`, then **Create pull request**.
6. Fill in the PR template checklist and answer the prompts (the extension uses
   no network by itself, runs no external programs and deletes no files).

The extension follows the plugin rules in
[`docs/plugins.md`](https://github.com/ingelibre/ingetrazo/blob/main/docs/plugins.md);
the rule-by-rule compliance table is in
[`ingetrazo-extensions-submission/README.md`](ingetrazo-extensions-submission/README.md).

The **sha256** in the entry
(`9bc82a17b203d43aa770a19d573bdb197797cdeb3ab49cc11e2c2f5a7ac7a4c8`) is the
fingerprint of `dist/igz_solids.zip` as built by the script. It **must** match
the uploaded asset; if you rebuild, update the value.
