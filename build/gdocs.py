"""Gera HTML simplificado para importação no Google Docs (build/APS-gdocs.html)."""
import re, html, sys, pathlib
sys.argv=[sys.argv[0]]
import importlib.util
spec=importlib.util.spec_from_file_location("b","build/build.py"); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
corpo_md="\n\n".join(b.preprocessar((b.DOCS/f).read_text()) for f in b.ARQUIVOS_CORPO)
apend_md="\n\n".join(b.preprocessar((b.DOCS/f).read_text()) for f in b.ARQUIVOS_APENDICES)
corpo_md=corpo_md.replace("@tabela_autoria", b.tabela_autoria())
refs=sorted(b.citadas,key=lambda k:b.REFS[k]["texto"].lower())
refs_md="# Referências {#sec-referencias}\n\n"+"\n\n".join(b.REFS[k]["texto"] for k in refs)
h=b.md_para_html(corpo_md)+b.md_para_html(refs_md)+b.md_para_html(apend_md)
# numerar figuras e tabelas na ordem
figs={};tbls={}
for m in re.finditer(r'<div id="(fig|tbl)-([\w-]+)" class="(figura|tabela)[^"]*"',h):
    d=figs if m.group(1)=="fig" else tbls; d[m.group(2)]=len(d)+1
h=re.sub(r'<a class="xfig" href="#fig-([\w-]+)"></a>',lambda m:f"Figura {figs[m.group(1)]}",h)
h=re.sub(r'<a class="xtbl" href="#tbl-([\w-]+)"></a>',lambda m:f"Tabela {tbls[m.group(1)]}",h)
# legendas
def leg(div):
    kind,ident=div.group(1),div.group(2); inner=div.group(3)
    n=figs[ident] if kind=="fig" else tbls[ident]; rot="Figura" if kind=="fig" else "Tabela"
    inner=re.sub(r'<p><span class="legenda">(.*?)</span></p>',lambda m:f'<p style="text-align:center"><b>{rot} {n} – {m.group(1)}</b></p>',inner,count=1)
    inner=re.sub(r'<p><img src="img/([^"]+)"[^>]*/></p>',lambda m:f'<p style="text-align:center;background-color:#fff3b0"><b>[INSERIR IMAGEM: docs/img/{m.group(1)}]</b></p>',inner)
    inner=re.sub(r'<p><span class="fonte">(.*?)</span></p>',r'<p><span style="font-size:9pt">\1</span></p>',inner)
    return inner
h=re.sub(r'<div id="(fig|tbl)-([\w-]+)" class="[^"]*">(.*?)</div>',leg,h,flags=re.S)
h=re.sub(r'<div class="meta">\s*<p>(.*?)</p>\s*</div>',r'<p style="background-color:#eef3f8;font-size:9pt">\1</p>',h,flags=re.S)
h=re.sub(r'<div class="prompt">(.*?)</div>',r'<blockquote>\1</blockquote>',h,flags=re.S)
h=re.sub(r'<span class="preencher">(.*?)</span>',r'<span style="background-color:#fff3b0"><b>\1</b></span>',h,flags=re.S)
h=re.sub(r'<a class="cit" href="#[^"]*">(.*?)</a>',r'\1',h)
h=re.sub(r'<a href="#[^"]*">(.*?)</a>',r'\1',h)
h=re.sub(r'<(h[1-3])[^>]*>',r'<\1>',h)
h=re.sub(r'<pre><code>(.*?)</code></pre>',lambda m:'<p style="font-family:Courier New;font-size:8.5pt;background-color:#f3f3f3">'+m.group(1).replace("\n","<br>")+'</p>',h,flags=re.S)
h=re.sub(r'<(table|thead|tbody|tr|th|td|colgroup|col|code|pre)[^>]*?( /)?>',lambda m:f"<{m.group(1)}>",h)
h=re.sub(r'<colgroup>.*?</colgroup>','',h,flags=re.S)
h=h.replace('<code>','<span style="font-family:Courier New">').replace('</code>','</span>')
h=h.replace('<table>','<table border="1" style="border-collapse:collapse;font-size:9pt">')
h=re.sub(r'>\s*\n\s*<','><',h)
capa=('<p style="text-align:center"><b>Universidade Federal de Goiás – Instituto de Informática<br>Bacharelado em Engenharia de Software<br>'
 'Disciplina: Domínios de Software – semestre 2026/2<br>Docente: Profa. Adriana Silveira de Souza</b></p>'
 '<p style="text-align:center">Atividades Práticas Supervisionadas (APS)</p>'
 '<h1 style="text-align:center">Projeto de Software Web para Autenticação de Usuários</h1>'
 '<p style="text-align:center"><i>Ambiente operacional, arquitetura e desenho detalhado de componentes</i></p>'
 '<p style="text-align:center">Autoria (ordem alfabética): Júlia de Souza Nascimento; Kesley Soares da Silva; Verônica Ribeiro Oliveira Palmeira</p>'
 '<p style="text-align:center">Repositório: github.com/jusouzn/software-web-autenticacao-ds-2026-2 · Goiânia, 27 de outubro de 2026 · versão 1.0</p>')
out='<html><body style="font-family:Times New Roman;font-size:12pt">'+capa+h+'</body></html>'
pathlib.Path("build/APS-gdocs.html").write_text(out)
print(len(out), len(out.encode()))
out=out.replace('<pre><span style="font-family:Courier New">','<pre style="font-family:Courier New;font-size:8.5pt;background-color:#f3f3f3">').replace('</span></pre>','</pre>')
pathlib.Path("build/APS-gdocs.html").write_text(out); print("final",len(out))
out=out.replace('<span style="font-family:Courier New">','<code>')
out=re.sub(r'<code>(.*?)</span>',r'<code>\1</code>',out)
out=out.replace('<table border="1" style="border-collapse:collapse;font-size:9pt">','<table border="1">')
out=out.replace('<br />\n','<br>')
out=out.replace('<strong>','<b>').replace('</strong>','</b>').replace('<em>','<i>').replace('</em>','</i>')
pathlib.Path("build/APS-gdocs.html").write_text(out); print("final2",len(out))
