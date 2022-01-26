// Insere a versão
const version = () => {
    try{
        // Pegando dados de todas as tags
        $.getJSON('https://api.github.com/repos/gurgueiavalley/ibc_finance/tags', (dados) => {
            const   json = dados[0],
                    div = $('.version')
            
            // Clique para redirecionar ao commit detalhado
            div.click(() => window.open(`https://github.com/gurgueiavalley/ibc_finance/commit/${json['commit']['sha']}?diff=split`, '_blank'))

            // Pegando dados do último commit
            $.getJSON(json['commit']['url'], (data) => {
                const date = new Date(data['commit']['committer']['date']).toLocaleString()     // Data
                
                // Atribuindo os dados para mostrar no popover
                div.attr({
                    'data-original-title' : `Novidades (${date})`,      // Título com a data
                    'data-content' : data['commit']['message']          // Mensagem do commit
                })
            })

            div.html(`<b> Versão: </b> ${json['name']}`)    // Atribuindo a versão
            
            // Atribuindo o popover
            div.popover({
                container : 'body',     // Mostra sobre a div
                placement : 'top',      // Mostra para cima
                trigger : 'hover'       // Mostra quando o mouse passa por cima
            })
        })
    }
    catch(e){}    
}

// Executa os métodos
$(() => {
    version()
})