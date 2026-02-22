import { useState } from 'react';
import type { Book, SearchResult } from './types';

function App() {
  const [activeTab, setActiveTab] = useState<'search' | 'generate'>('search');
  
  // Search state
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResult, setSearchResult] = useState<SearchResult | null>(null);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);

  // Generate state
  const [generateAmount, setGenerateAmount] = useState<number>(5);
  const [generateResult, setGenerateResult] = useState<Book[] | null>(null);
  const [generateLoading, setGenerateLoading] = useState(false);
  const [generateError, setGenerateError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setSearchLoading(true);
    setSearchError(null);
    setSearchResult(null);

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_message: searchQuery }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: SearchResult = await response.json();
      setSearchResult(data);
    } catch (err) {
      setSearchError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setSearchLoading(false);
    }
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (generateAmount < 1 || generateAmount > 100) {
      setGenerateError('Amount must be between 1 and 100');
      return;
    }

    setGenerateLoading(true);
    setGenerateError(null);
    setGenerateResult(null);

    try {
      const response = await fetch(`/api/generate?amount=${generateAmount}`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: Book[] = await response.json();
      setGenerateResult(data);
    } catch (err) {
      setGenerateError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setGenerateLoading(false);
    }
  };

  const renderBooks = (books: Book[]) => (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {books.map((book, index) => (
        <div key={index} className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
            {book.book_title}
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">{book.author_name}</p>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
              {book.year}
            </span>
            <span className="text-xs bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 px-2 py-1 rounded">
              ⭐ {book.rating}
            </span>
          </div>
          <div className="flex flex-wrap gap-1 mb-2">
            {book.genre_names.map((genre, i) => (
              <span
                key={i}
                className="text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 px-2 py-1 rounded"
              >
                {genre}
              </span>
            ))}
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">{book.description}</p>
        </div>
      ))}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <h1 className="text-3xl font-bold text-center text-gray-900 dark:text-white mb-8">
          Book Agent API
        </h1>

        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab('search')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'search'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-700'
            }`}
          >
            Search
          </button>
          <button
            onClick={() => setActiveTab('generate')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'generate'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-700'
            }`}
          >
            Generate
          </button>
        </div>

        {/* Search Tab */}
        {activeTab === 'search' && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Search Books
            </h2>
            <form onSubmit={handleSearch} className="mb-6">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Например: Есть ли книги Л. Толстого?"
                  className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button
                  type="submit"
                  disabled={searchLoading}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-blue-400 transition-colors"
                >
                  {searchLoading ? 'Searching...' : 'Search'}
                </button>
              </div>
            </form>

            {searchError && (
              <div className="bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 text-red-700 dark:text-red-200 px-4 py-3 rounded-lg mb-4">
                {searchError}
              </div>
            )}

            {searchResult && (
              <div className="mt-4">
                {searchResult.type === 'books' && Array.isArray(searchResult.data) && (
                  <>{renderBooks(searchResult.data as Book[])}</>
                )}
                {searchResult.type === 'count' && typeof searchResult.data === 'number' && (
                  <p className="text-gray-700 dark:text-gray-300">
                    Найдено книг: <span className="font-bold">{searchResult.data}</span>
                  </p>
                )}
                {searchResult.type === 'text' && typeof searchResult.data === 'string' && (
                  <p className="text-gray-700 dark:text-gray-300">{searchResult.data}</p>
                )}
                {searchResult.type === 'error' && (
                  <p className="text-red-600 dark:text-red-400">{String(searchResult.data)}</p>
                )}
              </div>
            )}
          </div>
        )}

        {/* Generate Tab */}
        {activeTab === 'generate' && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Generate Books
            </h2>
            <form onSubmit={handleGenerate} className="mb-6">
              <div className="flex gap-2 items-center">
                <label className="text-gray-700 dark:text-gray-300">
                  Amount:
                </label>
                <input
                  type="number"
                  value={generateAmount}
                  onChange={(e) => setGenerateAmount(parseInt(e.target.value) || 0)}
                  min="1"
                  max="100"
                  className="w-20 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button
                  type="submit"
                  disabled={generateLoading}
                  className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-green-400 transition-colors"
                >
                  {generateLoading ? 'Generating...' : 'Generate'}
                </button>
              </div>
            </form>

            {generateError && (
              <div className="bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 text-red-700 dark:text-red-200 px-4 py-3 rounded-lg mb-4">
                {generateError}
              </div>
            )}

            {generateResult && (
              <div className="mt-4">
                {renderBooks(generateResult)}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
