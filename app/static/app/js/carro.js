var updateBtns = document.getElementsByClassName('update-carro')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productoId = this.dataset.producto
        var action = this.dataset.action
        console.log('productoId: ', productoId, 'action:', action)

        console.log('USER:', user)
        if (user === 'AnonymousUser') {
            console.log('No logeado en la página')
        } else {
            actualizarUsuarioPedido(productoId, action)
        }
    })
}

function actualizarUsuarioPedido(productoId, action) {
    console.log('Usuario está logeado, enviando informacion...')

    var url = '/actualizarProducto/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productoId': productoId, 'action': action })

    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    })


}