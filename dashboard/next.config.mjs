import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const dashboardRoot = dirname(fileURLToPath(import.meta.url));

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  turbopack: {
    root: dashboardRoot,
  },
};

export default nextConfig;
