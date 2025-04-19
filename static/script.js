document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('download-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const url = document.getElementById('url').value;
      const statusDiv = document.getElementById('status');
      const downloadLinkDiv = document.getElementById('download-link');

      statusDiv.textContent = 'Processing...';
      downloadLinkDiv.innerHTML = '';

      try {
          const response = await fetch('/download', {
              method: 'POST',
              body: new FormData(document.getElementById('download-form')),
          });
          
          const result = await response.json();

          if (response.ok) {
              statusDiv.textContent = 'Success!';
              downloadLinkDiv.innerHTML = `<a href="/download_file/${encodeURIComponent(result.audio_path)}" download>Download MP3</a>`;
          } else {
              statusDiv.textContent = `Error: ${result.error}`;
          }
      } catch (error) {
          statusDiv.textContent = `Error: ${error.message}`;
      }
  });
});