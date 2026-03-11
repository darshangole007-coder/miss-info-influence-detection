// File: script.js (updated to fix URL, change country to 'in', and render to DOM as a test/fallback)
// Place this in static/script.js
// To use: Add <script src="/static/script.js"></script> to index.html <body> if you want client-side fetching.
// WARNING: Exposes API key in browser—use only for testing, prefer server-side.

document.addEventListener('DOMContentLoaded', () => {
  const apiKey = '9f007080be8b4c1aa3ac8321b1d0cbf6';  // Replace with valid key
  const url = `https://newsapi.org/v2/top-headlines?country=in&apiKey=${apiKey}&pageSize=5`;

  fetch(url)
    .then(res => {
      if (!res.ok) {
        throw new Error(`API error: ${res.status} - ${res.statusText}`);
      }
      return res.json();
    })
    .then(data => {
      if (data.status !== 'ok') {
        throw new Error(data.message);
      }
      const newsContainer = document.querySelector('.news-grid') || document.createElement('div');
      newsContainer.innerHTML = '';  // Clear existing
      data.articles.forEach(article => {
        const card = document.createElement('div');
        card.className = 'news-card';
        card.innerHTML = `
          ${article.urlToImage ? `<img src="${article.urlToImage}" alt="${article.title}" class="news-image">` : '<div class="no-image">No image</div>'}
          <h3><a href="${article.url}" target="_blank">${article.title}</a></h3>
          <p class="source">${article.source.name} • ${article.publishedAt.slice(0,10)}</p>
        `;
        newsContainer.appendChild(card);
      });
      if (!document.querySelector('.news-grid')) {
        document.querySelector('.container').appendChild(newsContainer);
      }
    })
    .catch(err => {
      console.error(err);
      const errorP = document.createElement('p');
      errorP.className = 'error';
      errorP.textContent = `Client-side news fetch failed: ${err.message}`;
      document.querySelector('.container').appendChild(errorP);
    });
});
