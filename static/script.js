// Esperamos a que todo el HTML cargue antes de ejecutar el script
document.addEventListener('DOMContentLoaded', () => {
    // Seleccionamos todos los botones de las pestañas
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // Le agregamos un "escuchador de clics" a cada botón
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // 1. Ocultar todos los formularios
            tabContents.forEach(tab => tab.style.display = 'none');
            
            // 2. Quitar el color "activo" de todos los botones
            tabBtns.forEach(b => b.classList.remove('active'));

            // 3. Mostrar el formulario del botón al que le dimos clic
            const target = btn.getAttribute('data-target');
            document.getElementById(target + '-tab').style.display = 'block';
            
            // 4. Marcar este botón como "activo"
            btn.classList.add('active');
        });
    });
});
