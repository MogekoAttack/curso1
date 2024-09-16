function UserType(type) {
    if (type !== `owner` && type !== `vet`) {
        alert(`ERROR, PLEASE NOT MODIFY THIS PAGE c: ${type}`)
        return
    }
    document.querySelector(`#user-type`).style.display = `none`
    let element = document.querySelector(`#user-${type}`)
    element.style.display = `flex`
    
}

function Return(type) {
    if (type !== `owner` && type !== `vet`) {
        alert(`ERROR, PLEASE NOT MODIFY THIS PAGE c: ${type}`)
        return
    }
    document.querySelector(`#user-type`).style.display = `flex`
    document.querySelector(`#user-${type}`).style.display = `none`
}