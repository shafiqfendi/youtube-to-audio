document.getElementById('converter-form').addEventListener('submit', function(e) {
    const convertBtn = document.getElementById('convert-btn');
    const loading = document.getElementById('loading');
    const urlInput = document.querySelector('input[name="youtube_url"]');
    
    // Validate URL format before submitting
    const youtubeRegex = /^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+/;
    if (!youtubeRegex.test(urlInput.value)) {
        alert('Please enter a valid YouTube URL');
        e.preventDefault();
        return;
    }
    
    // Show loading state
    convertBtn.disabled = true;
    convertBtn.textContent = 'Processing...';
    loading.style.display = 'block';
});
