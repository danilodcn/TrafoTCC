import itertools as it

try:
    from .Populacao import Populacao
    from .Individuo import Individuo
except ImportError:
    from Populacao import Populacao
    from Individuo import Individuo

class AG():
    def __init__(self, **kwargs):
        # import ipdb; ipdb.set_trace()
        self.variacoes = kwargs["variacoes"]
        self.numero_populacao = kwargs["numero_populacao"]
        self.constantes = kwargs["constantes"]
        self.max_geracoes = kwargs["max_geracoes"]
        self.constantes_ag = kwargs["constantes_ag"]
        
        self.geracao_atual = 0
        
        # import ipdb; ipdb.set_trace()
        self.startUp()
        # self.run_geracao()
        
    def startUp(self):
        # Individuo.trafo.constantes = self.constantes
        # Individuo.trafo.calculo_de_dados_do_trafo()
        
        self.populacao = Populacao(
            constantes=self.constantes,
            numero_populacao=self.numero_populacao,
            variacoes=self.variacoes
        )
    
        
    def run_geracao(self, geracao):
        self.geracao_atual = geracao
        #Inicia Selecionando os Indivíduos para o cruzamento
        # import ipdb; ipdb.set_trace()
        taxa_crossover = self.constantes_ag["taxa_crossover"]
        taxa_mutacao = self.constantes_ag["taxa_mutacao"]
        n_frentes = self.constantes_ag["n_frentes"]
        # import ipdb; ipdb.set_trace(context=10)
        n_populacao = len(self.populacao.individuos)
        n_individuos_para_crossover = round(taxa_crossover * n_populacao)
        # individuos_para_crossover_heuristico = self.populacao.selecao(n_selecionados=taxa_cruzamento)
        self.populacao.crossover_heuristico(
            qtd_heuristico=n_individuos_para_crossover,
            numero_individuos=n_populacao,
            n_frentes=n_frentes,
        )
        
        # # import ipdb; ipdb.set_trace(context=10)
        self.populacao.crossover_aritmetico(
            qtd_aritmetico=n_individuos_para_crossover,
            numero_individuos=n_populacao,
            n_frentes=n_frentes,
        )
        
        # self.populacao.mutacao(
        #     qtd=n_populacao,
        #     numero_individuos=0,
        #     taxa=taxa_mutacao,
        #     n_frentes=n_frentes,
        # )
        # # import ipdb; ipdb.set_trace(context=10)
        
        # self.populacao.crossover_heuristico(qtd_heuristico, numero_individuos)
        # import ipdb; ipdb.set_trace(context=20)
    
    def gerar_populacao_inicial(self, n):
        individuos = it.chain(*(self.populacao.gera_individuos() for i in range(n)))
        self.populacao.individuos.update(individuos)
        self.populacao.individuos = self.populacao.selecao(
            n_selecionados=self.numero_populacao,
            n_frentes=8,
        )
        
    def run(self):
        self.gerar_populacao_inicial(3)
        for geracao in range(1, self.max_geracoes + 1):
            print("geração: ", geracao)
            # import ipdb; ipdb.set_trace()
            self.run_geracao(geracao)
            yield geracao

