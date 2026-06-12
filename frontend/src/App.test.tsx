import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

describe('VisualLearn AI Frontend Tests', () => {
  test('renders login header and greeting screen text', () => {
    render(<App />);
    const headerElement = screen.getByText(/VisualLearn AI/i);
    expect(headerElement).toBeInTheDocument();
    
    const subtitleElement = screen.getByText(/Making learning visual & fun!/i);
    expect(subtitleElement).toBeInTheDocument();
  });
});
