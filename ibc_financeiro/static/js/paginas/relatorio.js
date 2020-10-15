document.querySelectorAll('.header')[4].onclick = () => {
    const   setaBaixo = document.querySelector('#setaBaixo'),
            setaCima = document.querySelector('#setaCima'),
            formulario = document.querySelector('#formulario')

    if(setaBaixo.style.display == '' || setaBaixo.style.display == 'block'){
        setaBaixo.style.display = 'none'
        setaCima.style.display = 'block'
        formulario.style.display = 'block'
    }

    else{
        setaBaixo.style.display = 'block'
        setaCima.style.display = 'none'
        formulario.style.display = 'none'
    }
}