$(() => {
    const   faixa = document.querySelector('#nouislider_range'),
            minimo = 0, 
            maximo = 10000

    noUiSlider.create(faixa, {
        start: [minimo, maximo],
        connect: true,
        range: {
            'min': minimo,
            'max': maximo
        }
    })

    updateValues(faixa.noUiSlider)

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
    $('#id_minimo').val(null)
    $('#id_maximo').val(null)
    
    $('#id_inicio').mask('00/00/0000')
    $('#id_fim').mask('00/00/0000')
}

// Métodos Auxiliares
function clearFilters(){
    const   opcoes = document.querySelectorAll('.filter-option'),
            valores = document.querySelector('#nouislider_range').noUiSlider,
            tamanhos = valores.options.range
            

    for(let indice = 0; indice < opcoes.length; indice++){
        $('#' + document.querySelectorAll('select')[indice].id).val([])
        
        const options = document.querySelectorAll('.dropdown-menu.inner')[indice].children
        
        for(let posicao = 0; posicao < options.length; posicao++)
            options[posicao].classList.remove('selected')
        
        opcoes[indice].innerText = 'Nenhuma selecionada'
    }

    document.querySelector('#id_minimo').value = null
    document.querySelector('#id_maximo').value = null
    
    valores.set([tamanhos.min, tamanhos.max])
}

function moneyFormat(valor){
    let contador = 0,
        invertido = valor[valor.length - 1] + valor[valor.length - 2] + ',',
        formatado = ''

    for(let indice = valor.length - 4; indice >= 0; indice--){
        if(contador++ == 3){
            invertido += '.'
            contador = 0
        }

        invertido += valor[indice]
    }
    
    for(let indice = invertido.length - 1; indice >= 0; indice--)
        formatado += invertido[indice]

    return 'R$' + formatado
}

function updateValues(funcoes){
    funcoes.on('update', () => {
        const   minimo = funcoes.get()[0],
                maximo = funcoes.get()[1]

        $('#id_minimo').val(minimo)
        $('#id_maximo').val(maximo)
            
        $('#minimo').text(moneyFormat(minimo))
        $('#maximo').text(moneyFormat(maximo))
    })
}