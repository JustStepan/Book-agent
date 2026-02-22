export interface Book {
  author_name: string;
  book_title: string;
  year: number;
  genre_names: string[];
  rating: number;
  description: string;
}

export interface SearchResult {
  type: 'books' | 'count' | 'text' | 'error';
  data: Book[] | number | string;
}
