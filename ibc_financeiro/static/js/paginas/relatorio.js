document.querySelectorAll('.header')[4].onclick = () => {
    const   setaBaixo = document.querySelector('#setaBaixo'),
            setaCima = document.querySelector('#setaCima'),
            filtrosAdicionais = document.querySelector('#filtrosAdicionais')

    if(setaBaixo.style.display == '' || setaBaixo.style.display == 'block'){
        setaBaixo.style.display = 'none'
        setaCima.style.display = 'block'
        filtrosAdicionais.style.display = 'block'
    }

    else{
        setaBaixo.style.display = 'block'
        setaCima.style.display = 'none'
        filtrosAdicionais.style.display = 'none'
    }
}