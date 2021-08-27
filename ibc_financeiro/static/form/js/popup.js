const Option = {
    page : window.opener.$,
    object : null, text : null, value : null,

    add : function(object, name, id){
        this.object = object, this.text = name, this.value = id
        
        const div = this.page(`#id_${object.toLowerCase()}`).parent()

        this.insert(div)
        this.select(div)
        this.notify()

        window.close()
    },

    insert : function(div){
        const text = this.text
        
        div.find('select').append($('<option>', {value : this.value, text : text}))

        div.find('li:nth-child(1)').after($('<li>', {
            attr : {'data-original-index' : div.find('li').length}
        }).append($('<a>').append($('<span>', {text : text}))))
    },

    notify : function(){
        const object = this.object, letter = object == 'Fornecedor' || object == 'Membro' ? 'o' : 'a'
        
        this.page.notify({
            title : `<strong> ${object} Inserid${letter} </strong> <br>`,
            message : `${letter.toUpperCase()} ${object.toLowerCase()} <strong> ${this.text} </strong> foi adicionad${letter} e selecionad${letter}`
        }, {
            type : 'success',
            offset : 10,
            spacing : 5,
            delay : 0,
            animate : {
                enter : 'animated zoomInRight',
                exit : 'animated zoomOutRight'
            }
        })
    },

    select : function(div){
        div.find('a').each((index) => {
            div.find(`li:nth-child(${++index}) a`).click(function(){
                div.find('.select').each(function(){this.classList.remove('select')})
                this.parentElement.classList.add('select')
            })
        })
        
        div.find('li:nth-child(2) a').click()
    },
}