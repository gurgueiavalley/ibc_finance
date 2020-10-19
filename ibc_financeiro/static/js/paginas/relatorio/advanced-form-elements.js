$(() => {
    const rangeSlider = document.getElementById('nouislider_range_example')

    noUiSlider.create(rangeSlider, {
        start: [25000, 100000],
        connect: true,
        range: {
            'min': 25000,
            'max': 100000
        }
    })

    getNoUISliderValue(rangeSlider)
})

function getNoUISliderValue(slider){
    slider.noUiSlider.on('update', () => {
        const   valMin = 'R$' + format(slider.noUiSlider.get()[0]),
                valMax = 'R$' + format(slider.noUiSlider.get()[1]);

        $(slider).parent().find('span.js-nouislider-valueMin').text(valMin);
        $(slider).parent().find('span.js-nouislider-valueMax').text(valMax);
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