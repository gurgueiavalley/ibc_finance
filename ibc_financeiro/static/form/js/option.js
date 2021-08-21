const Option = {
    div : window.opener.$,
    text : null,
    value : null,

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
    }
}