document.getElementById('converter-form').addEventListener('submit', function(e) {
    const convertBtn = document.getElementById('convert-btn');
    const loading = document.getElementById('loading');
    
    // Show loading spinner
    convertBtn.disabled = true;
    convertBtn.textContent = 'Processing...';
    loading.style.display = 'block';
    
    // This will continue naturally as the form submits
    // The page will stay on the same URL but receive a file download
});
