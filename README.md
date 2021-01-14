# EDC TP2
Projeto de EDC - Pokédex

## Instruções
 1. Instalar requirements 

        pip install -r requirements.txt 
        
 2. Criar o repositório de dados
    - Na GUI do GraphDB: Criar um novo repositório com o nome edc-pokemon. 
    - Os ficheiros de input de RDF estão na pasta data/triples na raíz do projecto. Todos os ficheiros .nt nesta pasta devem ser importados para o repositório criado.
    - As opções devem permanecer todas em default.
 
 3. Manter o GraphDB aberto, a correr no port default (em princípio, 7200).
 
 4. Correr a aplicação 
    
        python3 manage.py runserver

## Notas

### Inferências na página de Pokémon - Linha Evolutiva
Na página de um Pokémon, se ele tiver evoluções, é apresentada a linha evolutiva.
No dataset original, apenas existe a relação A evolui para B (evolves_to).
Para apresentar a linha evolutiva completa, nos casos em que o Pokémon selecionado não é a primeira
evolução, foi necessário deduzir os Pokémons de estágios anteriores a esse.
Para tal foi preciso compreender que Pokémons é que evoluiam para o selecionado, criando
assim, virtualmente, uma relação de B evolui de A (evolves_from).


### Inferências na página de Equipa
Na página de uma equipa, ao carregar no botão de informação (no canto superior direito),
é possível gerar a tabela de vantagens/desvantagens de todos os pokémons dessa equipa.
Esta tabela é inferida porque:

- Um Pokémon tem um ou dois tipos.
- Cada um desses tipo tem as suas vantagens e desvantagens.
- Se um tipo tem desvantagem sobre outro tem valor x2, se tiver vantagem tem
valor 1/2, se for Neutro tem x1 e se for imune é dado como Immune.
- Estes valores no jogo traduzem-se nas defesas de um dado Pokémon, contra ataques de outros, quanto menor o valor mais defesa tem o Pokémon contra um dado tipo.  
- Se um pokémon tem 2 tipos, e ambos tem vantagem em relação a outro tipo,
podemos inferir que o tipo tem vantagem dupla, sendo o seu valor 1/2*1/2 = 1/4.
- Se um dos tipos é immune contra outro, o Pokémon é automaticamente imune independente
da vantagem ou desvantagem do seu segundo tipo.
- Por outro lado, também podemos inferir casos de desvantagem dupla, onde os dois tipos tem desvantagem, 
que nesta tabela é ilustrado por um x4.