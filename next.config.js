/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['letterboxd.com', 'a.ltrbxd.com', 'image.tmdb.org'],
  },
  webpack: (config) => {
    config.resolve.extensions = ['.tsx', '.ts', '.js', '.jsx', ...config.resolve.extensions]
    return config
  },
}

module.exports = nextConfig