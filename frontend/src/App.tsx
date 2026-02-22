import { useSearch } from './hooks/useSearch';
import { SearchForm, ResponsePanel, LoadingIndicator } from './components';
import './App.css';

function App() {
  const { response, loading, error, sendSearch, clearResponse } = useSearch();

  return (
    <div className="app">
      <header className="app__header">
        <h1 className="app__title">Book Agent Search</h1>
        <p className="app__subtitle">Поиск книг в базе данных</p>
      </header>

      <main className="app__main">
        <div className="app__content">
          <section className="app__request">
            <h2 className="section-title">Ваш запрос</h2>
            <SearchForm onSubmit={sendSearch} disabled={loading} />
          </section>

          <section className="app__response">
            <h2 className="section-title">Ответ сервера</h2>
            {loading ? (
              <LoadingIndicator />
            ) : (
              <ResponsePanel 
                response={response} 
                error={error} 
                onClear={clearResponse} 
              />
            )}
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;
