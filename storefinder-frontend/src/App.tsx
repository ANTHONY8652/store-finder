/*
import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
*/
import { useEffect, useState } from 'react';


interface StoreResult {
  store: string;
  price: number;
  distance_km: number

}

function App() {
  const [location, setLocation] = useState<{ latitude: number; longitude: number; }>();
/*
 latitude: 0;
longitude: 0;
*/
  const [product, setProduct] = useState('');
  const [results, setResults] = useState<StoreResult[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((pos) => {
      setLocation({ latitude: pos.coords.latitude, longitude: pos.coords.longitude });
    });
  }, []);

  const fetchResults = async () => {
    if (!location || !product) return;
    setLoading(true);

    try {
      const res = await fetch(`http://127.0.0.1:8000/nearest-stores/?latitude=${location.latitude}&longitude${location.longitude}&product=${product}`);
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error(err);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-4">StoreFinder 🛒</h1>
      <input
      type="text"
      placeholder="Enter product e.g. milk"
      value={product}
      onChange={(e) => setProduct(e.target.value)}
      className="border p-2 rounded w-64 mb-4"
      />
      <button
        onClick={fetchResults}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
       >
      search
      </button> 

      {loading && <p className="mt-4">Loading results please wait....</p>}

      <ul className="mt-6 w-full max-w-md space-y-2">
        {results.map((store, index) => (
          <li key={index} className="bg-white p-4 rounded shadow">
            <p className="tet-lg font-semibold">{store.store}</p>
            <p>Price: <span className="font-medium">Ksh {store.price}</span></p>
            <p> Distance: {store.distance_km} km</p>
          </li>
        ))}
      </ul>
    </div>
  );

}

export default App;


/*
function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
*/
