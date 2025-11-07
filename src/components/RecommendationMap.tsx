'use client'

import { useState, useRef, useEffect } from 'react'
import * as d3 from 'd3'

interface MovieNode {
  id: string
  title: string
  rating?: number
  genres: string[]
  themes: string[]
  year: number
  x?: number
  y?: number
  fx?: number | null
  fy?: number | null
}

interface MovieConnection {
  source: string
  target: string
  similarity: number
  reasons: string[]
}

interface RecommendationMapProps {
  movies: MovieNode[]
  connections: MovieConnection[]
  centerMovie?: string
  onMovieClick?: (movie: MovieNode) => void
}

export default function RecommendationMap({ 
  movies, 
  connections, 
  centerMovie,
  onMovieClick 
}: RecommendationMapProps) {
  const svgRef = useRef<SVGSVGElement>(null)
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 })
  const [selectedMovie, setSelectedMovie] = useState<MovieNode | null>(null)

  useEffect(() => {
    if (!svgRef.current || movies.length === 0) return

    const svg = d3.select(svgRef.current)
    svg.selectAll('*').remove()

    const { width, height } = dimensions

    // Create force simulation
    const simulation = d3.forceSimulation<MovieNode>(movies)
      .force('link', d3.forceLink<MovieNode, MovieConnection>(connections)
        .id(d => d.id)
        .distance(d => 100 + (1 - d.similarity) * 200)
        .strength(d => d.similarity * 0.5)
      )
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(30))

    // Create container group
    const container = svg.append('g')
    
    // Add zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        container.attr('transform', event.transform)
      })
    
    svg.call(zoom)

    // Create gradient definitions for connections
    const defs = svg.append('defs')
    
    // Connection lines
    const links = container.selectAll('.link')
      .data(connections)
      .enter()
      .append('line')
      .attr('class', 'link')
      .style('stroke', '#999')
      .style('stroke-opacity', d => d.similarity * 0.6)
      .style('stroke-width', d => Math.max(1, d.similarity * 4))

    // Movie nodes
    const nodes = container.selectAll('.node')
      .data(movies)
      .enter()
      .append('g')
      .attr('class', 'node')
      .style('cursor', 'pointer')

    // Node circles
    nodes.append('circle')
      .attr('r', d => {
        if (d.id === centerMovie) return 25
        if (d.rating && d.rating >= 4) return 20
        if (d.rating && d.rating >= 3) return 15
        return 12
      })
      .style('fill', d => {
        if (d.id === centerMovie) return '#ff8000'  // Letterboxd orange
        if (d.rating && d.rating >= 4) return '#00e054'  // High rating green
        if (d.rating && d.rating >= 3) return '#40bcf4'  // Medium rating blue
        return '#9ab'  // Default light color
      })
      .style('stroke', '#fff')
      .style('stroke-width', 2)

    // Node labels
    nodes.append('text')
      .text(d => d.title.length > 20 ? d.title.substring(0, 20) + '...' : d.title)
      .attr('dy', d => d.id === centerMovie ? 35 : 25)
      .attr('text-anchor', 'middle')
      .style('font-size', '12px')
      .style('font-weight', d => d.id === centerMovie ? 'bold' : 'normal')
      .style('fill', '#fff')
      .style('pointer-events', 'none')

    // Year labels
    nodes.append('text')
      .text(d => `(${d.year})`)
      .attr('dy', d => d.id === centerMovie ? 48 : 38)
      .attr('text-anchor', 'middle')
      .style('font-size', '10px')
      .style('fill', '#ccc')
      .style('pointer-events', 'none')

    // Add interaction handlers
    nodes
      .on('click', (event, d) => {
        setSelectedMovie(d)
        if (onMovieClick) onMovieClick(d)
      })
      .on('mouseover', function(event, d) {
        d3.select(this).select('circle')
          .transition()
          .duration(200)
          .attr('r', (originalR) => {
            const currentR = d3.select(this).select('circle').attr('r')
            return Number(currentR) * 1.2
          })
          .style('stroke-width', 3)

        // Highlight connected movies
        links
          .style('stroke-opacity', link => {
            return (link.source === d.id || link.target === d.id) ? 1 : 0.1
          })
          .style('stroke-width', link => {
            return (link.source === d.id || link.target === d.id) ? 
              Math.max(2, link.similarity * 6) : 1
          })
      })
      .on('mouseout', function(event, d) {
        d3.select(this).select('circle')
          .transition()
          .duration(200)
          .attr('r', () => {
            if (d.id === centerMovie) return 25
            if (d.rating && d.rating >= 4) return 20
            if (d.rating && d.rating >= 3) return 15
            return 12
          })
          .style('stroke-width', 2)

        // Reset link opacity
        links
          .style('stroke-opacity', d => d.similarity * 0.6)
          .style('stroke-width', d => Math.max(1, d.similarity * 4))
      })

    // Update positions on simulation tick
    simulation.on('tick', () => {
      links
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y)

      nodes
        .attr('transform', (d: any) => `translate(${d.x},${d.y})`)
    })

    // Add drag behavior
    const drag = d3.drag<SVGGElement, MovieNode>()
      .on('start', (event, d) => {
        if (!event.active) simulation.alphaTarget(0.3).restart()
        d.fx = d.x
        d.fy = d.y
      })
      .on('drag', (event, d) => {
        d.fx = event.x
        d.fy = event.y
      })
      .on('end', (event, d) => {
        if (!event.active) simulation.alphaTarget(0)
        d.fx = null
        d.fy = null
      })

    nodes.call(drag)

  }, [movies, connections, centerMovie, dimensions, onMovieClick])

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      if (svgRef.current) {
        const rect = svgRef.current.parentElement?.getBoundingClientRect()
        if (rect) {
          setDimensions({ width: rect.width, height: rect.height })
        }
      }
    }

    window.addEventListener('resize', handleResize)
    handleResize()

    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return (
    <div className="w-full h-full relative bg-gray-900 rounded-lg overflow-hidden">
      <svg
        ref={svgRef}
        width={dimensions.width}
        height={dimensions.height}
        className="w-full h-full"
      />
      
      {selectedMovie && (
        <div className="absolute top-4 right-4 bg-gray-800 rounded-lg p-4 border border-gray-700 max-w-xs">
          <button 
            onClick={() => setSelectedMovie(null)}
            className="absolute top-2 right-2 text-gray-400 hover:text-white"
          >
            ✕
          </button>
          <h3 className="font-bold text-white mb-2">{selectedMovie.title}</h3>
          <p className="text-gray-300 text-sm mb-2">Year: {selectedMovie.year}</p>
          {selectedMovie.rating && (
            <p className="text-gray-300 text-sm mb-2">
              Rating: {selectedMovie.rating}/5 ⭐
            </p>
          )}
          <div className="mb-2">
            <p className="text-gray-400 text-xs mb-1">Genres:</p>
            <div className="flex flex-wrap gap-1">
              {selectedMovie.genres.slice(0, 3).map(genre => (
                <span key={genre} className="bg-gray-700 text-xs px-2 py-1 rounded">
                  {genre}
                </span>
              ))}
            </div>
          </div>
          {selectedMovie.themes && selectedMovie.themes.length > 0 && (
            <div>
              <p className="text-gray-400 text-xs mb-1">Themes:</p>
              <div className="flex flex-wrap gap-1">
                {selectedMovie.themes.slice(0, 2).map(theme => (
                  <span key={theme} className="bg-blue-600 text-xs px-2 py-1 rounded">
                    {theme}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Legend */}
      <div className="absolute bottom-4 left-4 bg-gray-800 rounded-lg p-3 border border-gray-700">
        <h4 className="text-white font-semibold mb-2 text-sm">Legend</h4>
        <div className="space-y-2 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-orange-500"></div>
            <span className="text-gray-300">Center Movie</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-gray-300">High Rating (4+)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-400"></div>
            <span className="text-gray-300">Good Rating (3+)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-gray-400"></div>
            <span className="text-gray-300">Recommendation</span>
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="absolute top-4 left-4 bg-gray-800 rounded-lg p-3 border border-gray-700">
        <p className="text-white text-sm mb-2">Controls:</p>
        <div className="text-xs text-gray-300 space-y-1">
          <p>• Drag nodes to reposition</p>
          <p>• Scroll to zoom in/out</p>
          <p>• Click nodes for details</p>
          <p>• Hover to highlight connections</p>
        </div>
      </div>
    </div>
  )
}