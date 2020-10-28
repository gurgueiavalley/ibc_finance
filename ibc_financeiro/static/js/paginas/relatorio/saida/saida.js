$(() => {
    $('#bs_datepicker_range_container').datepicker({
        autoclose: false,
        container: '#bs_datepicker_range_container',
        language: 'pt-BR'
    })
})

document.querySelector('#botao').onclick = () => {
    const   descricao   = document.querySelector('.header small'),
            adicionar   = document.querySelector('#adicionar'),
            deletar     = document.querySelector('#deletar'),
            filtros     = document.querySelector('#filtros')

    if(filtros.style.display == 'none'){
        filtros.style.display = 'block'
        
        adicionar.style.display = 'none'
        deletar.style.display = 'block'
        
        descricao.innerText = 'Remover todos os filtros e gerar um relatório mais abrangente'
    }

    else{
        clearFilters()
        filtros.style.display = 'none'

        deletar.style.display = 'none'
        adicionar.style.display = 'block'

        descricao.innerText = 'Adicionar filtros para gerar um relátorio mais refinado'
    }
}

window.onload = () => {    
    $('#id_inicio').mask('00/00/0000')
    $('#id_fim').mask('00/00/0000')
}

// Métodos Auxiliares
function clearFilters(){
    const opcoes = document.querySelectorAll('.filter-option')

    for(let indice = 0; indice < opcoes.length; indice++){
        $('#' + document.querySelectorAll('select')[indice].id).val([])
        
        const options = document.querySelectorAll('.dropdown-menu.inner')[indice].children
        
        for(let posicao = 0; posicao < options.length; posicao++)
            options[posicao].classList.remove('selected')
        
        opcoes[indice].innerText = 'Nenhuma selecionada'
    }
}