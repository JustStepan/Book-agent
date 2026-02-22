export function LoadingIndicator() {
  return (
    <div className="loading-indicator">
      <div className="loading-indicator__spinner"></div>
      <p className="loading-indicator__text">Обработка запроса...</p>
    </div>
  );
}
