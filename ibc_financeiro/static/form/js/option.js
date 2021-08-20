const Option = {
    div : window.opener.$,
    text : null,
    value : null,

    create : function(className, name, id){
        this.div = this.div(`#id_${className.toLowerCase()}`).parent()
        this.text = name
        this.value = id
    }
}