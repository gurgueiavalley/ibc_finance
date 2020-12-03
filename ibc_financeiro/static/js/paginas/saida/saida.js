$(() => {
    $('.datepicker').bootstrapMaterialDatePicker({
        format: 'dddd, DD/MM/YYYY',
        lang: 'pt-BR',
        cancelText: 'Cancelar',
        okText: 'Confirmar',
        time: false
    })
})

$('.dropzone').dropzone({
    acceptedFiles: 'image/jpg, image/jpeg, image/png, .pdf',
    maxFiles: 1,
    parallelUploads: 1,
    addRemoveLinks: true,
    dictRemoveFile: 'Remover',
    maxfilesexceeded: function(file){
        this.removeAllFiles()
        this.addFile(file)
    }
})