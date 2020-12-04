$(() => {
    $('.datepicker').bootstrapMaterialDatePicker({
        format: 'dddd, DD/MM/YYYY',
        lang: 'pt-BR',
        cancelText: 'Cancelar',
        okText: 'Confirmar',
        time: false
    })
})

$('.btn-success').click(() => {
    const formulario = document.querySelector('#formulario')

    if(formulario.checkValidity())
        formulario.submit()

    formulario.reportValidity()
})