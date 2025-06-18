document.addEventListener('DOMContentLoaded', function () {
    const select = document.getElementById('location-select');
    const divPreview = document.getElementById('div-preview-location');

    select.addEventListener('change', async function () {
        if (this.value != 'new' && this.value != '') {

            divPreview.style.display = 'block';
            divPreview.value = '';

            try {
                const id_location = this.value;
                const response = await fetch('/api/locations/' + id_location, {
                    method: 'GET'
                });

                if (!response.ok) {
                    throw new Error('Error al obtener las ubicaciones');
                } else {
                    const data = await response.json();

                    imgPreview = document.getElementById('location-file-preview');
                    descPreview = document.getElementById('location-description-preview');

                    imgPreview.src = 'static/uploads/locations/' + data.location.imageLocation;
                    imgPreview.style.display = 'block';
                    descPreview.value = data.location.descLocation;
                    descPreview.readOnly = true;
                }

            } catch (error) {
                console.error('Error:', error);
                alert('Hubo un problema al obtener las ubicaciones. Por favor, inténtalo de nuevo.');
            }
        } else {
            divPreview.style.display = 'none';
        }
    });
});
