$(() => {
    $('.datepicker').bootstrapMaterialDatePicker({
        format: 'DD/MM/YYYY',
        lang: 'pt-BR',
        cancelText: 'Cancelar',
        okText: 'Confirmar',
        time: false
    })
})

document.querySelectorAll('b')[11].classList.add('oculto')