import { useState, useCallback } from 'react';
import type { SearchRequest, SearchResponse } from '../types/api';

interface UseSearchResult {
  response: string | null;
  loading: boolean;
  error: string | null;
  sendSearch: (message: string) => Promise<void>;
  clearResponse: () => void;
}

export function useSearch(): UseSearchResult {
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendSearch = useCallback(async (message: string) => {
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const requestBody: SearchRequest = { user_message: message };
      
      const res = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data: SearchResponse = await res.json();
      setResponse(data.message);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, []);

  const clearResponse = useCallback(() => {
    setResponse(null);
    setError(null);
    setLoading(false);
  }, []);

  return { response, loading, error, sendSearch, clearResponse };
}
