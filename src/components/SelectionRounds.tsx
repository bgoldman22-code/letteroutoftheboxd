'use client';

import { useState, useEffect } from 'react';

interface Movie {
  title: string;
  year?: string;
  director?: string;
  genres?: string[];
  poster?: string;
  rating?: number;
  actors?: string[];
  plot?: string;
  runtime?: string;
}

interface SelectionRoundsProps {
  movies: Movie[];
  onComplete: (selectedMovies: Movie[]) => void;
  onBack: () => void;
}

export default function SelectionRounds({ movies, onComplete, onBack }: SelectionRoundsProps) {
  const [currentRound, setCurrentRound] = useState(1);
  const [roundMovies, setRoundMovies] = useState<Movie[]>([]);
  const [selectedInRound, setSelectedInRound] = useState<Set<string>>(new Set());
  const [round1Selections, setRound1Selections] = useState<Movie[]>([]);
  const [round2Selections, setRound2Selections] = useState<Movie[]>([]);
  const [round1Shown, setRound1Shown] = useState<Movie[]>([]); // Track all Round 1 movies
  const [round2Shown, setRound2Shown] = useState<Movie[]>([]); // Track all Round 2 movies
  const [instruction, setInstruction] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const TOTAL_ROUNDS = 3; // Reduced from 5 to work with ~30-50 movies from RSS

  // Load round movies on mount and round changes
  useEffect(() => {
    loadRound();
  }, [currentRound]); // eslint-disable-line react-hooks/exhaustive-deps

  async function loadRound() {
    setLoading(true);
    setError('');
    setSelectedInRound(new Set());

    try {
      const response = await fetch('/.netlify/functions/get-selection-rounds', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          movies,
          round1Selections,
          round2Selections,
          round1Shown, // Pass shown movies to exclude from next rounds
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to load round');
      }

      const data = await response.json();
      setRoundMovies(data.movies);
      setInstruction(data.instruction);
      
      // Track which movies were shown in this round
      if (currentRound === 1) {
        setRound1Shown(data.movies);
      } else if (currentRound === 2) {
        setRound2Shown(data.movies);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function toggleSelection(movie: Movie) {
    const key = `${movie.title}-${movie.year}`;
    const newSelected = new Set(selectedInRound);

    if (newSelected.has(key)) {
      newSelected.delete(key);
    } else {
      if (newSelected.size < 3) {
        newSelected.add(key);
      }
    }

    setSelectedInRound(newSelected);
  }

  function getSelectedMovies(): Movie[] {
    return roundMovies.filter(m => 
      selectedInRound.has(`${m.title}-${m.year}`)
    );
  }

  async function handleNextRound() {
    const selected = getSelectedMovies();

    if (currentRound === 1) {
      setRound1Selections(selected);
      setCurrentRound(2);
      await loadRound();
    } else if (currentRound === 2) {
      setRound2Selections(selected);
      setCurrentRound(3);
      await loadRound();
    } else {
      // Round 3 complete - combine all selections (9 movies total)
      const allSelected = [
        ...round1Selections,
        ...round2Selections,
        ...selected
      ];
      onComplete(allSelected);
    }
  }

  const canProceed = selectedInRound.size === 3;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <button
            onClick={onBack}
            className="mb-4 text-purple-300 hover:text-purple-100 transition-colors"
          >
            ← Back
          </button>
          
          <h1 className="text-4xl font-bold text-white mb-2">
            Discover Your Cinematic Taste
          </h1>
          
          {/* Progress */}
          <div className="flex justify-center items-center gap-2 mb-4">
            {[1, 2, 3].map(round => (
              <div
                key={round}
                className={`w-16 h-2 rounded-full transition-all ${
                  round < currentRound
                    ? 'bg-green-500'
                    : round === currentRound
                    ? 'bg-purple-500'
                    : 'bg-gray-600'
                }`}
              />
            ))}
          </div>
          
          <p className="text-xl text-purple-200">
            Round {currentRound} of {TOTAL_ROUNDS}
          </p>
          
          <p className="text-lg text-gray-300 mt-2">
            {instruction}
          </p>
          
          <p className="text-sm text-gray-400 mt-1">
            Selected: {selectedInRound.size}/3
          </p>
        </div>

        {/* Error */}
        {error && (
          <div className="mb-6 bg-red-500/20 border border-red-500 text-red-200 px-6 py-4 rounded-lg">
            {error}
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="text-center text-white text-xl">
            Loading movies...
          </div>
        )}

        {/* Movie Grid */}
        {!loading && roundMovies.length > 0 && (
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
            {roundMovies.map((movie) => {
              const key = `${movie.title}-${movie.year}`;
              const isSelected = selectedInRound.has(key);

              return (
                <button
                  key={key}
                  onClick={() => toggleSelection(movie)}
                  className={`group relative aspect-[2/3] rounded-lg overflow-hidden transition-all transform hover:scale-105 ${
                    isSelected
                      ? 'ring-4 ring-purple-500 scale-105'
                      : 'ring-1 ring-gray-700 hover:ring-purple-400'
                  }`}
                >
                  {/* Poster */}
                  {movie.poster ? (
                    <img
                      src={movie.poster}
                      alt={movie.title}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full bg-gradient-to-br from-purple-900 to-gray-800 flex items-center justify-center p-4">
                      <p className="text-white text-center text-sm font-semibold">
                        {movie.title}
                      </p>
                    </div>
                  )}

                  {/* Overlay */}
                  <div className={`absolute inset-0 bg-gradient-to-t from-black/90 via-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-3 ${
                    isSelected ? 'opacity-100' : ''
                  }`}>
                    <p className="text-white font-bold text-sm mb-1">
                      {movie.title}
                    </p>
                    <p className="text-gray-300 text-xs">
                      {movie.year || 'Unknown'} • {movie.director || 'Unknown'}
                    </p>
                    
                    {isSelected && (
                      <div className="absolute top-2 right-2 bg-purple-500 rounded-full w-8 h-8 flex items-center justify-center">
                        <span className="text-white font-bold">✓</span>
                      </div>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        )}

        {/* Next Button */}
        {!loading && roundMovies.length > 0 && (
          <div className="text-center">
            <button
              onClick={handleNextRound}
              disabled={!canProceed}
              className={`px-12 py-4 rounded-lg font-bold text-lg transition-all ${
                canProceed
                  ? 'bg-purple-600 hover:bg-purple-700 text-white shadow-lg shadow-purple-500/50 transform hover:scale-105'
                  : 'bg-gray-700 text-gray-400 cursor-not-allowed'
              }`}
            >
              {currentRound === TOTAL_ROUNDS ? 'Analyze My Taste' : 'Next Round →'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
