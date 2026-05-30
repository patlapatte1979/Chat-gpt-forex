import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const dashboardRoot = dirname(fileURLToPath(import.meta.url));
const workspaceRoot = resolve(dashboardRoot, '..');

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  turbopack: {
    root: workspaceRoot,
  },
};

export default nextConfig;
