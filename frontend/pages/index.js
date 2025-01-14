import { useState } from 'react';
import Chat from '../components/Chat';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });
    const data = await response.json();
    setResults(data.results);
  };

  return (
    <div>
      <h1>Jira Ticket Query</h1>
      <form onSubmit={handleQuerySubmit}>
        <input
          type="text"
          value={query}
          onChange={handleQueryChange}
          placeholder="Enter your query"
        />
        <button type="submit">Search</button>
      </form>
      <Chat results={results} />
    </div>
  );
}
