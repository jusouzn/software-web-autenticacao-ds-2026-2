#!/usr/bin/env python3
"""Gera o PDF único de entrega da APS a partir dos arquivos Markdown em docs/.

Uso:  python3 build/build.py            (gera build/APS-Autenticacao-Web.pdf)
Requisitos: pandoc, weasyprint (pip), pyyaml; mmdc (Mermaid CLI) para --diagramas.
Marcações aceitas no Markdown:
  @meta(IT-x.y, autor, revisor)   cabeçalho do item de informação
  @ref(chave; chave)              citação bibliográfica (docs/referencias.yml)
  @fig(id) / @tbl(id)             referência a figura / tabela (numeração automática)
  @sec(1.2) -> 'Seção 1.2';  @secn(1.2) -> '1.2';  @apx(1) referência a apêndice
  @tabela_autoria                 tabela consolidada artefato / autor / revisor
"""
import html, re, subprocess, sys, pathlib, yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"
SAIDA = RAIZ / "build" / "APS-Autenticacao-Web.pdf"

MEMBROS = {
    "julia": "Júlia de Souza Nascimento",
    "kesley": "Kesley Soares da Silva",
    "veronica": "Verônica Ribeiro Oliveira Palmeira",
    "todos": "Todos os integrantes",
}
ARQUIVOS_CORPO = [
    "00-controle.md",
    "01-ambiente/1.0-introducao.md",
    "01-ambiente/1.1-componentes.md",
    "01-ambiente/1.2-inicializacao.md",
    "01-ambiente/1.3-processamento.md",
    "01-ambiente/1.4-protocolos.md",
    "02-projeto/2.1-requisitos.md",
    "02-projeto/2.2-arquitetura.md",
    "02-projeto/2.3-componentes.md",
    "02-projeto/2.4-dados.md",
    "02-projeto/2.5-api.md",
    "02-projeto/2.6-comportamento.md",
    "02-projeto/2.7-seguranca.md",
    "02-projeto/2.8-rastreabilidade.md",
]
ARQUIVOS_APENDICES = [
    "apendices/I-prompts-ia.md",
    "apendices/II-plano-equipe.md",
    "apendices/III-registros.md",
]
ROMANOS = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}

REFS = yaml.safe_load((DOCS / "referencias.yml").read_text(encoding="utf-8"))
citadas: set[str] = set()
itens: list[dict] = []
erros: list[str] = []


def cite(chaves: str) -> str:
    partes = []
    for k in [c.strip() for c in chaves.split(";") if c.strip()]:
        if k not in REFS:
            erros.append(f"referência inexistente: {k}")
            continue
        citadas.add(k)
        partes.append(f'<a class="cit" href="#ref-{k}">{html.escape(REFS[k]["rotulo"])}</a>')
    return "[" + "; ".join(partes) + "]"


def sec(num: str, so_numero: bool) -> str:
    return f'<a href="#sec-{num.replace(".", "-")}">{num if so_numero else "Seção " + num}</a>'


def preprocessar(texto: str) -> str:
    # itens de informação: refs detectadas dentro de cada item
    partes = re.split(r"(@meta\([^)]*\))", texto)
    saida = []
    for i, p in enumerate(partes):
        m = re.fullmatch(r"@meta\(([^)]*)\)", p)
        if not m:
            saida.append(p)
            continue
        campos = [c.strip() for c in m.group(1).split(",")]
        codigo, autor, revisor = campos[0], campos[1], campos[2]
        if autor == revisor and autor != "todos":
            erros.append(f"{codigo}: autor e revisor iguais")
        corpo_item = partes[i + 1] if i + 1 < len(partes) else ""
        chaves = list(dict.fromkeys(re.findall(r"@ref\(([^)]*)\)", corpo_item)))
        chaves = list(dict.fromkeys(k.strip() for c in chaves for k in c.split(";")))
        titulo = ""
        anterior = "".join(saida)
        h = re.findall(r"^#{1,3} (.+?)(?: \{.*\})?$", anterior, re.M)
        if h:
            titulo = h[-1]
        itens.append({"codigo": codigo, "titulo": titulo, "autor": autor, "revisor": revisor})
        refs_txt = "; ".join(f"@ref({k})" for k in chaves if k != "anthropic2026") or "—"
        rev = "Revisão cruzada: cada registro é revisado por integrante que não o redigiu" if revisor == "todos" else f"Revisão: {MEMBROS[revisor]}"
        saida.append(
            f'\n::: {{.meta}}\n**Item de informação {codigo}** · Autoria: {MEMBROS[autor]} · {rev}  \n'
            f'Referências do item: {refs_txt} · Apoio de IA: @ref(anthropic2026)\n:::\n'
        )
    texto = "".join(saida)
    texto = re.sub(r"@ref\(([^)]*)\)", lambda m: cite(m.group(1)), texto)
    texto = re.sub(r"@fig\(([\w-]+)\)", r'<a class="xfig" href="#fig-\1"></a>', texto)
    texto = re.sub(r"@tbl\(([\w-]+)\)", r'<a class="xtbl" href="#tbl-\1"></a>', texto)
    texto = re.sub(r"@apx\((\d)\)", lambda m: f'<a href="#apx-{m.group(1)}">Apêndice {ROMANOS[int(m.group(1))]}</a>', texto)
    texto = re.sub(r"@secn\(([\d.]+)\)", lambda m: sec(m.group(1), True), texto)
    texto = re.sub(r"@sec\(([\d.]+)\)", lambda m: sec(m.group(1), False), texto)
    return texto


def md_para_html(texto: str) -> str:
    r = subprocess.run(
        ["pandoc", "-f", "markdown-implicit_figures+fenced_divs+bracketed_spans", "-t", "html5", "--no-highlight", "--wrap=none"],
        input=texto.encode(), capture_output=True, check=True,
    )
    return r.stdout.decode()


def tabela_autoria() -> str:
    linhas = ["| Item | Artefato | Autoria | Revisão |", "|---|---|---|---|"]
    for it in itens:
        rev = "Cruzada entre integrantes" if it["revisor"] == "todos" else MEMBROS[it["revisor"]]
        linhas.append(f"| {it['codigo']} | {it['titulo']} | {MEMBROS[it['autor']]} | {rev} |")
    return "\n".join(linhas)


def main():
    faltando = [f for f in ARQUIVOS_CORPO + ARQUIVOS_APENDICES if not (DOCS / f).exists()]
    if faltando:
        print("Aviso – arquivos ainda não commitados (ignorados):", ", ".join(faltando))
    ler = lambda lista: "\n\n".join(preprocessar((DOCS / f).read_text(encoding="utf-8")) for f in lista if (DOCS / f).exists())
    corpo_md, apend_md = ler(ARQUIVOS_CORPO), ler(ARQUIVOS_APENDICES)
    # a tabela de autoria só pode ser montada depois de todos os itens lidos
    corpo_md = corpo_md.replace("@tabela_autoria", tabela_autoria())

    refs_ord = sorted(citadas, key=lambda k: REFS[k]["texto"].lower())
    refs_md = "# Referências {#sec-referencias .nonum}\n\n" + "\n\n".join(
        f'::: {{.ref #ref-{k}}}\n{REFS[k]["texto"]}\n:::' for k in refs_ord
    )
    nao_citadas = set(REFS) - citadas
    if nao_citadas:
        print("Aviso – referências não citadas (omitidas):", ", ".join(sorted(nao_citadas)))

    corpo = md_para_html(corpo_md)
    referencias = md_para_html(refs_md)
    apendices = md_para_html(apend_md)

    # sumário a partir dos títulos h1/h2/h3
    todo = corpo + referencias + apendices
    sumario = []
    for nivel, ident, titulo in re.findall(r'<h([123]) id="([^"]+)"[^>]*>(.*?)</h\1>', todo, re.S):
        sumario.append(f'<li class="n{nivel}"><a href="#{ident}">{titulo}</a></li>')
    # confere âncoras usadas
    ids = set(re.findall(r'id="([^"]+)"', todo))
    for alvo in re.findall(r'href="#([^"]+)"', todo):
        if alvo not in ids:
            erros.append(f"âncora inexistente: #{alvo}")
    if faltando:  # versão parcial: links para itens ainda ausentes viram aviso
        avisos = [e for e in erros if e.startswith("âncora")]
        erros[:] = [e for e in erros if not e.startswith("âncora")]
        if avisos:
            print("Aviso – links para itens ausentes:", len(avisos))
    if erros:
        print("ERROS:\n  " + "\n  ".join(sorted(set(erros))))
        sys.exit(1)

    capa = (RAIZ / "build" / "capa.html").read_text(encoding="utf-8")
    documento = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">
<title>APS – Software Web para Autenticação de Usuários</title>
<meta name="author" content="Júlia de Souza Nascimento; Kesley Soares da Silva; Verônica Ribeiro Oliveira Palmeira">
<link rel="stylesheet" href="estilo.css"></head><body>
{capa}
<nav class="sumario"><h1 class="semnum-toc">Sumário</h1><ul>{''.join(sumario)}</ul></nav>
<main>{corpo}{referencias}</main><section class="apendices">{apendices}</section>
</body></html>"""
    html_path = RAIZ / "build" / "APS.html"
    html_path.write_text(documento, encoding="utf-8")
    from weasyprint import HTML
    HTML(filename=str(html_path), base_url=str(DOCS)).write_pdf(
        str(SAIDA), stylesheets=[str(RAIZ / "build" / "estilo.css")]
    )
    print(f"PDF gerado: {SAIDA}  ({len(itens)} itens, {len(citadas)} referências)")


if __name__ == "__main__":
    if "--diagramas" in sys.argv:
        for mmd in sorted((DOCS / "diagramas").glob("*.mmd")):
            subprocess.run(["mmdc", "-i", str(mmd), "-o", str(DOCS / "img" / (mmd.stem + ".png")),
                            "-s", "3", "-b", "white", "-c", str(DOCS / "diagramas" / "mermaid.json"), "-q"], check=True)
    main()
