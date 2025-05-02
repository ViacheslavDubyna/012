async function loadData(params) {
    try {
        const response = await fetch('./data json')
        const dsata = await response.json()
        // const 
        

    } catch (error) {
        console.error ("Похибка обробки JSON",error)
    }
}


// Get the canvas element and its 2D drawing context
const canvas = document.getElementById('myCanvas')
const ctx = canvas.