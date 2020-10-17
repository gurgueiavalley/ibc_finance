document.querySelectorAll('.header')[4].onclick = () => {
    const   adicionar = document.querySelector('#adicionar'),
            deletar = document.querySelector('#deletar'),
            filtros = document.querySelector('#filtros'),
            descricao = document.querySelector('.header small')

    if(adicionar.style.display == '' || adicionar.style.display == 'block'){
        adicionar.style.display = 'none'

        filtros.style.display = 'block'
        deletar.style.display = 'block'

        descricao.innerText = 'Remover todos os filtros e gerar um relátorio mais abrangente'
    }

    else{
        filtros.style.display = 'none'
        deletar.style.display = 'none'

        adicionar.style.display = 'block'

        descricao.innerText = 'Adicionar filtros para gerar um relátorio mais refinado'
        
        removeAllSelected()
    }
}

function removeAllSelected(){
    const opcoes = document.querySelectorAll('.filter-option')

    for(let indice = 0; indice < opcoes.length; indice++){
        opcoes[indice].innerText = 'Nenhuma selecionada'
        
        const options = document.querySelectorAll('.dropdown-menu.inner')[indice].children
            
        for(let posicao = 0; posicao < options.length; posicao++)
            options[posicao].classList.remove('selected')

        $('#' + document.querySelectorAll('select')[indice].id).val([])
    }
}