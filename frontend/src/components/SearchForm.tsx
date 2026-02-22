import { useState } from 'react';
import type { FormEvent } from 'react';

interface SearchFormProps {
  onSubmit: (message: string) => void;
  disabled: boolean;
}

export function SearchForm({ onSubmit, disabled }: SearchFormProps) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;
    onSubmit(message);
  };

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <div className="search-input-wrapper">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Введите ваш запрос..."
          className="search-input"
          disabled={disabled}
        />
        <button type="submit" className="search-button" disabled={disabled}>
          <svg 
            className="search-icon" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" 
            />
          </svg>
          <span>Поиск</span>
        </button>
      </div>
    </form>
  );
}
