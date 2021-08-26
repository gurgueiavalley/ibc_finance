const Option = {
    div : window.opener.$,
    text : null,
    value : null,

    addToList : function(){
        this.div.find('li:nth-child(1)').after($('<li>', {
            attr : {
                'data-original-index' : this.div.find('li').length
            }
        }).append($('<a>').append($(`<span> ${this.text} </span>`))))
    },

    addToSelect : function(){
        this.div.find('select').append($('<option>', {
            value : this.value,
            text : this.text
        }))
    },

    insert : function(className, name, id){
        this.div = this.div(`#id_${className.toLowerCase()}`).parent()
        this.text = name
        this.value = id

        this.addToSelect()
        this.addToList()
        this.unselect()
        this.select()
        this.notify(className)

        window.close()
    },

    notify : function(className){
        const sex = className == 'Fornecedor' || className == 'Membro' ? 'o' : 'a'
        
        window.opener.$.notify({
            title : `<strong> ${className} Inserid${sex} </strong> <br>`,
            message : `${sex.toUpperCase()} ${className.toLowerCase()} <strong> ${this.text} </strong> foi adicionad${sex} e selecionad${sex}`
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

    select : function(){
        this.div.find('li:nth-child(2) a').click()
    },

    unselect : function(){
        this.div.find('a').each((index) => {
            this.div.find(`li:nth-child(${++index}) a`).click(function(){
                this.parentElement.parentElement.querySelectorAll('.select').forEach((li) => li.classList.remove('select'))
                this.parentElement.classList.add('select')
            })
        })
    }
}