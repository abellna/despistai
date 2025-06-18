document.addEventListener('DOMContentLoaded', function () {
    const select = document.getElementById('location-select');
    const newLocDiv = document.getElementById('new-location-modal');
    const saveButton = document.getElementById('save-location-button');


    select.addEventListener('change', function () {
        if (this.value === 'new') {
            newLocDiv.style.display = 'block';
            newLocDiv.value = '';
        } else {
            newLocDiv.style.display = 'none';
        }
    });

    saveButton.addEventListener('click', async function (e) {
        e.preventDefault();

        const nameLocation = document.getElementById('name-new-location-input').value;
        const imageLocation = document.getElementById('image-new-location-input');
        const imageLocationFile = imageLocation.files[0];
        const descriptionLocation = document.getElementById('desc-new-location-input').value;


        if (!nameLocation || !imageLocationFile) {
            alert('Por favor, completa los campos: Nombre de la ubicación e Imagen de la ubicación.');
            return;
        }     

        const formData = new FormData();
        formData.append('nameLocation', nameLocation);
        formData.append('imageLocation', imageLocationFile);
        formData.append('descLocation', descriptionLocation);

        try {
            const response = await fetch('/crear-ubicacion', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Error al guardar la ubicación');
            } else {
                const data = await response.json();
                alert('Ubicación guardada exitosamente');
                
                const option = document.createElement('option');
                const imgPreview = document.getElementById('location-file-preview');
                const descPreview = document.getElementById('location-description-preview');
                const divPreview = document.getElementById('div-preview-location');

                option.value = data.location_id;
                option.textContent = data.nameLocation;
                select.insertBefore(option, select.lastElementChild);
                select.value = data.location_id;
                newLocDiv.style.display = 'none';

                divPreview.style.display = 'block';
                imgPreview.src = 'static/uploads/locations/' + data.imageLocation;
                imgPreview.style.display = 'block';
                descPreview.value = data.descLocation;
                descPreview.readOnly = true;
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Hubo un problema al guardar la ubicación. Por favor, inténtalo de nuevo.');
        }
    });
});

function cerrarModal() {
  document.getElementById('new-location-modal').style.display = 'none';
}