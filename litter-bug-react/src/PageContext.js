// src/PageContext.js
import { createContext, useState, useContext } from 'react';

const PageContext = createContext();

export const PageProvider = ({ children }) => {
  const [currentPage, setCurrentPage] = useState('home');

  return (
    <PageContext.Provider value={{ currentPage, setCurrentPage }}>
      {children}
    </PageContext.Provider>
  );
};

export const usePage = () => useContext(PageContext);