document.addEventListener('DOMContentLoaded', function () {
    // const showErrorDiv = document.getElementById('item-error-message');
    const saveButton = document.getElementById('save-item-button');

    saveButton.addEventListener('click', async function (e) {
        e.preventDefault();
        
        const nameItem = document.getElementById('item-name').value;
        const imageItem = document.getElementById('item-image');
        const imageItemFile = imageItem.files[0];
        const descriptionItem = document.getElementById('item-description').value;
        const locationItem = document.getElementById('location-select').value;

        if (!nameItem || !imageItemFile) {
            alert('Por favor, completa los campos: Nombre del objeto e Imagen del objeto.');
            return;
        }     

        const formData = new FormData();
        formData.append('itemName', nameItem);
        formData.append('itemImage', imageItemFile);
        formData.append('itemDescription', descriptionItem);
        formData.append('itemLocation', locationItem);

        try {
            const response = await fetch('/crear-item', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Error al guardar el objeto');
            } else {
                const data = await response.json();
                alert('Objeto guardado exitosamente');
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Hubo un problema al guardar el objeto. Por favor, inténtalo de nuevo.');
        }
    });
});