document.querySelectorAll('.header')[4].onclick = () => {
    const   adicionar = document.querySelector('#adicionar'),
            deletar = document.querySelector('#deletar'),
            filtros = document.querySelector('#filtros'),
            opcoes = document.querySelectorAll('.dropdown-menu')[3].children[0].children,
            descricao = document.querySelector('.header small')

    if(adicionar.style.display == '' || adicionar.style.display == 'block'){
        adicionar.style.display = 'none'
        deletar.style.display = 'block'
        filtros.style.display = 'block'

        descricao.innerText = 'Remover todos os filtros e gerar um relátorio mais abrangente'
    }

    else{
        adicionar.style.display = 'block'
        deletar.style.display = 'none'
        filtros.style.display = 'none'

        descricao.innerText = 'Adicionar filtros para gerar um relátorio mais refinado'
        document.querySelector('.filter-option').innerText = 'Nenhuma selecionada'

        for(let indice = 0; indice < opcoes.length; indice++){
            opcoes[indice].classList.remove('selected')
            document.querySelector('#id_categoria').remove(0)
        }
    }
}