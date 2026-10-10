# igz_solids — sólidos paramétricos para o IngeTrazo

`igz_solids` é uma extensão de barra de ferramentas para o
**[IngeTrazo](https://github.com/ingelibre/ingetrazo)** que cria sólidos 3D
paramétricos: caixa, cápsula, cilindro/tubo, esfera, cone/pirâmide, esfera
geodésica (incluindo uma bola de futebol), hélice, prisma e toro.

Cada sólido é construído como uma **malha fechada (watertight)**, inserido
como o **seu próprio Grupo** e gravado como **um passo de undo**.

- **Autor:** Ezequiel M. Rezende
- **Data:** 2026-10-10
- **Versão:** 1.0.0
- **Licença:** [GPL-3.0-or-later](https://www.gnu.org/licenses/gpl-3.0.html)
  (mesma do IngeTrazo — ver [LICENSE](https://github.com/ingelibre/ingetrazo/blob/main/LICENSE))

  ---

![IngeTrazo com a barra "Solids"](screenshots/igz-solids.png)

*A barra **Solids**, diálogo de Esfera Geodésica e possíveis sólidos construídos.*

---

## Recursos

- **14 botões** na barra (ver a tabela abaixo), espelhados em
  **Extensões ▸ Sólidos** (*Extensions ▸ Solids*).
- **Diálogo de parâmetros** por sólido; medidas em metros.
- **Dois modos de inserção** — *No cursor (clique)*: um aramado de
  pré-visualização acompanha o rato e cada clique coloca um sólido; ou
  *Na origem (0, 0, 0)*.
- **Grupos** — cada sólido entra como um Grupo, com o nome do botão e já
  selecionado. Como tem malha própria, nunca se solda ao modelo e continua
  fácil de selecionar, mover e editar. Se estiveres a editar um grupo ou
  componente, o novo sólido é criado dentro dele.
- **Watertight e com normais corretas** — a malha é orientada para fora e as
  costuras curvas ficam suaves (arestas *soft*), enquanto as tampas planas
  mantêm os rebordos vivos.
- **Internacionalizado** — inglês (fonte), espanhol, português do Brasil e
  italiano; segue o idioma da interface do IngeTrazo.
- **Ícones SVG com tema** para a interface escura e clara.
- **Sem dependências extra** — usa apenas o IngeTrazo (o PySide6 vem com ele).

## Requisitos

- **IngeTrazo** (0.x — API de extensões versão 2).
- Windows ou Linux (qualquer plataforma onde o IngeTrazo corra).
- Não é preciso `pip install`.

## Instalação

O mais simples: no IngeTrazo, abre **Extensões ▸ Abrir pasta de plugins**,
coloca lá a pasta `igz_solids` e **reinicia o IngeTrazo**. A barra **Sólidos**
e o submenu **Extensões ▸ Sólidos** aparecem no arranque.

Manualmente, copia a pasta para a tua pasta de plugins do utilizador:

- **Windows:** `%APPDATA%\IngeTrazo\plugins\igz_solids`
- **Linux:** `~/.local/share/ingetrazo/plugins/igz_solids`
  (ou `$XDG_DATA_HOME/ingetrazo/plugins/igz_solids`)

## Como usar

1. Clica num botão da barra **Sólidos** (ou em **Extensões ▸ Sólidos**).
2. Preenche o diálogo e pressiona **OK**.
3. Escolhe o **Posicionamento**:
   - **No cursor (clique):** move o rato — o sólido é pré-visualizado como
     aramado — e clica para o colocar. A ferramenta fica ativa para colocares
     vários; pressiona **Esc** para sair.
   - **Na origem (0, 0, 0):** o sólido é criado na origem do mundo.
4. O novo sólido chega como **Grupo**, já selecionado, num único passo de undo.

> As medidas são em **metros** (unidade interna do IngeTrazo).

## Os sólidos

| Botão | Ícone | Forma | Opções do diálogo |
|---|---|---|---|
| **Box** (Caixa) | ![Caixa](icons/tb_box.svg) | Caixa retangular | Largura (X), Comprimento (Y), Altura (Z) |
| **Wedge** (Cunha) | ![Cunha](icons/tb_wedge.svg) | Cunha triangular reta (prisma) | Largura (X), Comprimento (Y), Altura (Z) |
| **Capsule** (Cápsula) | ![Cápsula](icons/tb_capsule.svg) | Cilindro com duas calotas esféricas | Raio, Altura do corpo, Segmentos horizontais, Segmentos por calota |
| **Cylinder** (Cilindro) | ![Cilindro](icons/tb_cylinder.svg) | Cilindro circular | Raio externo, Segmentos, Altura |
| **Tube** (Tubo) | ![Tubo](icons/tb_tube.svg) | Tubo circular vazado | Raio externo, Raio interno, Segmentos, Altura |
| **Sphere** (Esfera) | ![Esfera](icons/tb_sphere.svg) | Esfera UV completa | Raio, Segmentos horizontais, Segmentos verticais |
| **Domus** | ![Domus](icons/tb_domus.svg) | Semiesfera com base plana | Raio, Segmentos horizontais / verticais |
| **Wedge** (Gomo) | ![Gomo](icons/tb_segment.svg) | Cunha esférica (gomo) | Raio, Segmentos horizontais / verticais, Ângulo da cunha |
| **Cone** | ![Cone](icons/tb_cone.svg) | Cone (curvo, ≥ 12 lados) | Raio da base, Raio do topo (0 = ponta), Altura, Lados |
| **Pyramid** (Pirâmide) | ![Pirâmide](icons/tb_pyramid.svg) | Pirâmide facetada | Raio da base, Raio do topo (0 = tronco), Altura, Lados |
| **Geodesic Sphere** (Esfera Geodésica) | ![Esfera Geodésica](icons/tb_geodesic.svg) | Esfera geodésica (ver abaixo) | Geometria base, Raio, Frequência, Acabamento |
| **Helix** (Hélice) | ![Hélice](icons/tb_helix.svg) | Hélice sólida (mola tubular) | Raio da hélice, Raio do tubo, Altura total, Voltas, Segmentos por volta, Segmentos do tubo |
| **Prism** (Prisma) | ![Prisma](icons/tb_prism.svg) | Prisma regular de N lados (≥ 12 fica curvo) | Raio da base, Altura, Lados |
| **Torus** (Toro) | ![Toro](icons/tb_torus.svg) | Toro (anel) | Raio maior (anel), Raio menor (seção), Segmentos do anel, Segmentos da seção |

Os botões **Box/Wedge**, **Cylinder/Tube**, **Sphere/Domus/Wedge** e
**Cone/Pyramid** partilham um pulldown *Tipo*, pelo que todas as variantes
também estão acessíveis pelo diálogo.

### Esfera geodésica

O diálogo **Esfera Geodésica** oferece quatro geometrias base:

- **Tetraedro**, **Octaedro**, **Icosaedro** — subdivididos *Frequência*
  vezes (0–4) e projetados na esfera.
- **Bola de futebol (icosaedro truncado)** — o **icosaedro truncado** exato:
  12 pentágonos + 20 hexágonos (60 vértices, 90 arestas, 32 faces,
  V − E + F = 2). O campo *Frequência* não se aplica a ela.

O *Acabamento* escolhe **Não suavizar** (arestas dos painéis/facetas vivas —
o visual clássico da bola) ou **Suavizar** (costuras suaves).

## Estrutura dos ficheiros

```
igz_solids/
├── __init__.py        # ponto de entrada da extensão (expõe setup(app))
├── _core.py           # motor privado: diálogo, ferramenta de inserção, grupos, i18n, ícones
├── tb_list.txt        # os botões da barra, por ordem
├── tb_box.py          # um módulo por família de sólidos (SPEC + build)
├── tb_capsule.py
├── tb_cylinder.py
├── tb_sphere.py
├── tb_frustrum.py
├── tb_geodesic.py
├── tb_helix.py
├── tb_prism.py
├── tb_torus.py
├── i18n/              # en.json (fonte), es.json, pt-BR.json, it.json
├── icons/             # SVGs com tema: tb_<nome>.svg e tb_<nome>_light.svg
├── README.md          # versão em inglês
├── README_ptBR.md     # este ficheiro
├── LICENSE            # GNU GPL v3.0
├── THIRD-PARTY.md     # avisos de terceiros
└── Referencias codigo Rubi/   # as ferramentas Ruby originais (só referência)
```

O `_core.py` tem prefixo `_` **de propósito**: o carregador do IngeTrazo
instancia com zero argumentos todas as subclasses de `Tool` *definidas no
módulo do plugin* (`__init__.py`), pelo que a `Tool` interativa tem de viver
num submódulo que o carregador ignora.

## Adicionar um sólido teu

Cada `tb_*.py` expõe duas coisas:

- `SPEC` — os metadados do diálogo (nome, ícone, dica e campos) mais as
  entradas da barra em `ACTIONS`, para que um único módulo possa alimentar
  vários botões.
- `build(params, origin)` — a geometria pura, devolvendo
  `(faces, cap_indices, smooth)`, onde `faces` é uma lista de faces — um laço
  de vértices (`QVector3D`, metros) ou um par `(laço, [furos])` para uma face
  plana com furos (o anel de um tubo) — `cap_indices` indexa as faces planas
  cujos rebordos ficam vivos, e `smooth` pede costuras suaves.

Para adicionar: cria `tb_myosolid.py`, acrescenta o nome do módulo numa linha
do `tb_list.txt` e reinicia o IngeTrazo.

Os campos de escolha usam `{"value": <token estável>, "label": <fonte em
inglês>}`, para que o rótulo possa ser traduzido sem alterar aquilo com que o
`build()` compara.

## Internacionalização

O inglês é a língua **fonte**: as strings passadas ao `tr()` estão em inglês.
A extensão traz catálogos `{inglês: tradução}` em `i18n/`, e o `tr()` resolve
por esta ordem: **catálogo do plugin → catálogo do IngeTrazo → inglês**. O
idioma ativo é o do IngeTrazo (`core.i18n.current_language()`); como o
IngeTrazo aplica a mudança de idioma ao reiniciar, a barra volta a rotular-se
no arranque seguinte.

Para acrescentar um idioma, copia `i18n/it.json` para `i18n/<código>.json`
(usa o código que o IngeTrazo usa, p. ex. `id`, `zh-CN`) e traduz os valores.

## Ícones

Cada ação da barra procura `icons/<nome>.svg`. Conforme a paleta da janela, o
`load_icon()` prefere `icons/<nome>_light.svg`, com fallback para o outro
ficheiro se o escolhido faltar. A convenção é controlada pela constante
`LIGHT_ICONS_FOR_DARK_THEME` em `_core.py`.

## Créditos

- **IngeTrazo** — a aplicação anfitriã e a sua API de plugins.
- As **ferramentas Ruby originais**

## Licença

**GPL-3.0-or-later.** Veja [`LICENSE`](LICENSE) (o texto da GNU GPL v3.0) e
[`THIRD-PARTY.md`](THIRD-PARTY.md) para os avisos de terceiros.


