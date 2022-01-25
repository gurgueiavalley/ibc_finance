// Notificação de erro
const error = () => {
    $.notify({
        title : '<b> Página Não Encontrada </b> <br>',
        message : `A página <strong> "${window.location.pathname}" </strong> não existe. Navegue pelo menu`
    }, {
        type : 'danger',
        placement : {
            align : 'center'
        },
        delay : 0,
        animate : {
            enter : 'animated fadeInDown',
            exit : 'animated fadeOutUp'
        }
    })
}