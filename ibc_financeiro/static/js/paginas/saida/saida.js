$(() => {
    $('.datepicker').bootstrapMaterialDatePicker({
        format: 'dddd, DD/MM/YYYY',
        lang: 'pt-BR',
        cancelText: 'Cancelar',
        okText: 'Confirmar',
        time: false
    })
})