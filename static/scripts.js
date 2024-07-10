async function uploadFiles() {
    const groupInfoFile = document.getElementById('groupInfoFile').files[0];
    const hostelInfoFile = document.getElementById('hostelInfoFile').files[0];
    
    const formData = new FormData();
    formData.append('groupInfoFile', groupInfoFile);
    formData.append('hostelInfoFile', hostelInfoFile);
    
    try {
        const response = await fetch('/allocate', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();

        if (result.status === 'success') {
            window.location.href = '/results';
        } else {
            alert('Failed to allocate rooms: ' + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to allocate rooms. Please try again.');
    }
}
