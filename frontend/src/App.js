import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [links, setLinks] = useState([]);

  // Función para manejar la adición de un enlace
  const handleAddLink = async () => {
    if (!url) return;

    try {
      // Petición al backend para agregar el enlace y que devuelva la categoría inferida
      const response = await fetch('http://localhost:5000/api/links', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }), // Solo envía el enlace, sin categoría
      });
      const data = await response.json();

      if (response.ok) {
        // Agregar el enlace y la categoría inferida a la lista
        setLinks((prevLinks) => [...prevLinks, { url: data.url, category: data.category }]);
        setUrl(''); // Limpiar el campo de entrada después de agregar el enlace
      } else {
        console.error(data.error || 'Error desconocido al agregar el enlace');
      }
    } catch (error) {
      console.error("Error al agregar el enlace:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>LinkScribe - Organizador de Enlaces Inteligente</h1>
      </header>

      <div className="link-form">
        <input 
          type="text" 
          value={url} 
          placeholder="Ingresa el enlace" 
          onChange={(e) => setUrl(e.target.value)} 
        />
        <button onClick={handleAddLink}>Agregar Enlace</button>
      </div>

      <div className="link-list">
        <h2>Mis Enlaces</h2>
        {links.length === 0 ? (
          <p>No hay enlaces agregados</p>
        ) : (
          <ul>
            {links.map((link, index) => (
              <li key={index}>
                <a href={link.url} target="_blank" rel="noopener noreferrer">{link.url}</a> - <strong>{link.category}</strong>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
