import React, { useState } from 'react';

function DistanceForm() {
  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');
  const [result, setResult] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult('');
    setError('');

    try {
      const response = await fetch('https://distance-app-backend-80cd0460510b.herokuapp.com/distance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          source_address: source,
          destination_address: destination,
        }),
      });

      if (!response.ok) {
        const errorBody = await response.json();
        const errMessage = errorBody.detail || 'Request failed';
        throw new Error(errMessage);
      }

      // Parse successful response
      const data = await response.json();
      setResult(`Distance: ${data.distance_km.toFixed(2)} km`);
    } catch (err) {
      setError(`Error: ${err.message}`);
    }
  };

  return (
    <div style={{ margin: '20px' }}>
      <form onSubmit={handleSubmit} style={{ marginBottom: '10px' }}>
        <div style={{ marginBottom: '10px' }}>
          <label>
            Source Address:
            <input
              type="text"
              value={source}
              onChange={(e) => setSource(e.target.value)}
              placeholder="e.g., Avenida Paulista, 1578, São Paulo, SP, Brazil"
              required
              style={{ marginLeft: '10px', width: '300px' }}
            />
          </label>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>
            Destination Address:
            <input
              type="text"
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              placeholder="e.g., Rua da Consolação, 500, São Paulo, SP, Brazil"
              required
              style={{ marginLeft: '10px', width: '300px' }}
            />
          </label>
        </div>

        <button type="submit">Calculate Distance</button>
      </form>

      {/* Display result or error messages */}
      {result && <p>{result}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default DistanceForm;
