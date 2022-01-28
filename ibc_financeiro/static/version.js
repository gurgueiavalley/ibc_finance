$(() => {
    try{
        // Pegando dados de todas as tags do repositório
        $.getJSON('https://api.github.com/repos/gurgueiavalley/ibc_finance/tags', (data) => {
            const div = $('#version')   // Div da versão
            
            data = data[0]      // Pegando todo o dicionário

            // Inserindo a versão
            div.html(`<b> Versão: </b> ${data['name']}`)
            
            // Leva ao último commit da versão detalhadamente no GitHub em outra aba ao clicar
            div.click(() => {
                window.open(
                    `https://github.com/gurgueiavalley/ibc_finance/commit/${data['commit']['sha']}?diff=split`,
                    '_blank'
                )
            })

            // Criando e definindo o popover
            div.popover({
                container : 'body',     // Aparece fora do seu espaço
                placement : 'top',      // Aparece em cima
                trigger : 'hover'       // Aparece quando passa o mouse por cima
            })

            // Atribuindo o conteúdo do popover
            $.getJSON(data['commit']['url'], (data) => {
                // Pegando data e hora do commit convertendo o formato
                const datetime = new Date(data['commit']['author']['date']).toLocaleString()

                div.attr({
                    'data-original-title' : `Atualizações (${datetime})`,   // Título com a data e hora
                    'data-content' : data['commit']['message']              // Mensagem do commit
                })
            })
        })
    }

    catch(erro){}      // Não faz nada se ocorrer erro
})