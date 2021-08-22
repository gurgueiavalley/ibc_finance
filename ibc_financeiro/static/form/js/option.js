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
    }
}