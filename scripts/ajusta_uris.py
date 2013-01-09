#!/usr/bin/python
import re
from rdflib import Namespace, URIRef
from rdflib.namespace import RDF
from rdflib.graph import ConjunctiveGraph 

LOA = Namespace("http://vocab.e.gov.br/2012/08/loa2012#")
LOA_I = Namespace("http://orcamento.dados.gov.br/id/")
g = ConjunctiveGraph()
g.bind('loa', LOA)
g.bind('loa-i', LOA_I)
with open("rdf_loa2012_uri_dadosgovbr.ttl", "r") as f:
    g.load(f, format="n3")

def troca_uri(classe, padrao_uri, novo_padrao):
    padrao = re.compile(padrao_uri)
    for uri_antiga,p,o in g.triples((None, RDF['type'], classe)):
        match = padrao.match(uri_antiga)
        if match:
            id_instancia = match.group(1)
            uri_nova = URIRef(novo_padrao % id_instancia)
            print "Trocando %s por %s..." % (uri_antiga, uri_nova)
            g.remove((uri_antiga, RDF['type'], classe))
            g.add((uri_nova, RDF['type'], classe))
            # onde aparece como sujeito
            for s,p,o in g.triples((uri_antiga, None, None)):
                g.remove((s, p, o))
                g.add((uri_nova, p, o))
            # onde aparece como objeto
            for s,p,o in g.triples((None, None, uri_antiga)):
                g.remove((s, p, o))
                g.add((s, p, uri_nova))

troca_uri(LOA['Acao'],r"^http://orcamento.dados.gov.br/id/acao-([A-Z0-9]{4})$", LOA_I["acao/%s"])
troca_uri(LOA['ElementoDespesa'],r"^http://orcamento.dados.gov.br/id/elemento_despesa-(\d{2})$", LOA_I["elemento-despesa/%s"])
troca_uri(LOA['Esfera'],r"^http://orcamento.dados.gov.br/id/esfera-(\d{2})$", LOA_I["esfera/%s"])
troca_uri(LOA['FonteRecursos'],r"^http://orcamento.dados.gov.br/id/fonte_recursos-(\d{3})$", LOA_I["fonte-recursos/%s"])
troca_uri(LOA['Funcao'],r"^http://orcamento.dados.gov.br/id/funcao-(\d{2})$", LOA_I["funcao/%s"])
troca_uri(LOA['Subfuncao'],r"^http://orcamento.dados.gov.br/id/subfuncao-(\d{3})$", LOA_I["subfuncao/%s"])
troca_uri(LOA['GrupoNatDespesa'],r"^http://orcamento.dados.gov.br/id/gnd-(\d)$", LOA_I["gnd/%s"])
troca_uri(LOA['ModalidadeAplicacao'],r"^http://orcamento.dados.gov.br/id/modalidade_aplicacao-(\d{2})$", LOA_I["modalidade-aplicacao/%s"])
troca_uri(LOA['Orgao'],r"^http://orcamento.dados.gov.br/id/orgao-(\d{5})$", LOA_I["orgao/%s"])
troca_uri(LOA['UnidadeOrcamentaria'],r"^http://orcamento.dados.gov.br/id/unidade_orcamentaria-(\d{5})$", LOA_I["unidade-orcamentaria/%s"])
troca_uri(LOA['Programa'],r"^http://orcamento.dados.gov.br/id/programa-(\d{4})$", LOA_I["programa/%s"])
troca_uri(LOA['CategoriaEconomica'],r"^http://orcamento.dados.gov.br/id/categoria_economica-(\d)$", LOA_I["categoria-economica/%s"])
troca_uri(LOA['ResultadoPrimario'],r"^http://orcamento.dados.gov.br/id/resultado_primario-(\d)$", LOA_I["resultado-primario/%s"])
troca_uri(LOA['IndicadorUso'],r"^http://orcamento.dados.gov.br/id/indicador_uso-(\d)$", LOA_I["indicador-uso/%s"])
troca_uri(LOA['Localizador'],r"^http://orcamento.dados.gov.br/id/localizador-([A-Z0-9]{8})$", LOA_I["localizador/%s"])
troca_uri(LOA['ItemDeDespesa'],r"^http://orcamento.dados.gov.br/id/item_de_despesa-(\d+)$", LOA_I["item-de-despesa/%s"])

with open("rdf_loa2012_uri_dadosgovbr-1.ttl", "w") as f:
    f.write(g.serialize(format="n3"))

