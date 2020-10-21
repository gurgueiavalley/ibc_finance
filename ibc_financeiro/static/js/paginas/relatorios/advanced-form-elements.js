$(() => {
    const   rangeSlider = document.getElementById('nouislider_range_example'),
            minimo = parseFloat(document.querySelector('#id_minimo').min) || 0,
            maximo = parseFloat(document.querySelector('#id_maximo').max) || 10000

    noUiSlider.create(rangeSlider, {
        start: [minimo, maximo],
        connect: true,
        range: {
            'min': minimo,
            'max': maximo
        }
    })

    getNoUISliderValue(rangeSlider)
})

function getNoUISliderValue(slider){
    slider.noUiSlider.on('update', () => {
        const   valMin = format(slider.noUiSlider.get()[0]),
                valMax = format(slider.noUiSlider.get()[1]);

        document.querySelector('#id_minimo').value = slider.noUiSlider.get()[0]
        document.querySelector('#id_maximo').value = slider.noUiSlider.get()[1]
            
        $(slider).parent().find('span.js-nouislider-valueMin').text('R$' + valMin);
        $(slider).parent().find('span.js-nouislider-valueMax').text('R$' + valMax);
    })
}

function format(valor){
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
    
    for(let indice = invertido.length - 1; indice >= 0; indice--){
        formatado += invertido[indice]
    }

    return formatado
}