interface ResponsePanelProps {
  response: string | null;
  error: string | null;
  onClear: () => void;
}

export function ResponsePanel({ response, error, onClear }: ResponsePanelProps) {
  if (!response && !error) {
    return (
      <div className="response-panel response-panel--empty">
        <div className="response-panel__placeholder">
          <svg className="response-panel__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={1.5} 
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" 
            />
          </svg>
          <p>Ответ от сервера появится здесь</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`response-panel ${error ? 'response-panel--error' : 'response-panel--success'}`}>
      <div className="response-panel__header">
        <span className="response-panel__title">
          {error ? 'Ошибка' : 'Ответ сервера'}
        </span>
        <button onClick={onClear} className="response-panel__clear" title="Очистить">
          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M6 18L18 6M6 6l12 12" 
            />
          </svg>
        </button>
      </div>
      <div className="response-panel__content">
        {error ? (
          <div className="response-panel__error">
            <svg className="response-panel__error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
              />
            </svg>
            <p>{error}</p>
          </div>
        ) : (
          <pre className="response-panel__text">{response}</pre>
        )}
      </div>
    </div>
  );
}
