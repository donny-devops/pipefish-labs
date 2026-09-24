#!/usr/bin/env node
/**
 * PipeFish Labs - Static Site Build (Node.js)
 *
 * Assembles the publicly servable website into ./dist so that it can be uploaded
 * as Cloudflare Workers static assets.
 *
 * Pure Node.js with zero external dependencies.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const ALLOWED_SUFFIXES = new Set([
  '.html',
  '.css',
  '.js',
  '.mjs',
  '.png',
  '.jpg',
  '.jpeg',
  '.gif',
  '.svg',
  '.webp',
  '.avif',
  '.ico',
  '.mp4',
  '.webm',
  '.woff',
  '.woff2',
  '.txt',
  '.xml',
  '.webmanifest',
  '.pdf',
]);

const EXCLUDED_DIRS = new Set([
  '.git',
  '.github',
  '.githooks',
  '.venv',
  '.wrangler',
  '__pycache__',
  'node_modules',
  'dist',
  'ansible',
  'bots',
  'charts',
  'db',
  'docs',
  'examples',
  'infra',
  'linkedin',
  'mcp',
  'postman',
  'pipefish_labs.egg-info',
  'sales',
  'scripts',
  'security',
  'src',
  'terraform',
  'tests',
]);

const EXTRA_FILES = [
  'CNAME',
  '_headers',
  '_redirects',
  'admin/config.yml',
  'sdk/openapi.yaml',
  'sdk/asyncapi.yaml',
  'site.webmanifest',
  '.well-known/security.txt',
];

const MAX_ASSET_BYTES = 25 * 1024 * 1024;

const EXCLUDED_FILES = new Set([
  'briefing-video-poster.png',
  'briefing-video-poster.jpg',
]);

function isPublishable(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const basename = path.basename(filePath);
  return ALLOWED_SUFFIXES.has(ext) && !EXCLUDED_FILES.has(basename);
}

function walkDir(currentDir, relativePrefix, fileList) {
  const entries = fs.readdirSync(currentDir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(currentDir, entry.name);
    const relPath = relativePrefix ? path.join(relativePrefix, entry.name) : entry.name;

    if (entry.isDirectory()) {
      if (EXCLUDED_DIRS.has(entry.name)) {
        continue;
      }
      walkDir(fullPath, relPath, fileList);
    } else if (entry.isFile()) {
      if (isPublishable(fullPath)) {
        fileList.push(relPath);
      }
    }
  }
}

export function build(rootDir = ROOT, outDir = path.resolve(ROOT, 'dist')) {
  if (outDir === rootDir || outDir.startsWith(rootDir + path.sep) && path.relative(rootDir, outDir) === '') {
    console.error(`error: refusing to use ${outDir} as the output directory`);
    return 1;
  }

  const fileList = [];
  walkDir(rootDir, '', fileList);

  const seen = new Set(fileList.map((f) => path.normalize(f)));
  const missing = [];

  for (const extra of EXTRA_FILES) {
    const fullPath = path.join(rootDir, extra);
    if (!fs.existsSync(fullPath)) {
      missing.push(extra);
      continue;
    }
    const norm = path.normalize(extra);
    if (!seen.has(norm)) {
      fileList.push(extra);
      seen.add(norm);
    }
  }

  if (missing.length > 0) {
    for (const name of missing) {
      console.error(`error: required file is missing: ${name}`);
    }
    return 1;
  }

  if (fileList.length === 0) {
    console.error('error: no publishable files found');
    return 1;
  }

  if (fs.existsSync(outDir)) {
    fs.rmSync(outDir, { recursive: true, force: true });
  }
  fs.mkdirSync(outDir, { recursive: true });

  let totalBytes = 0;
  const oversized = [];

  // Sort files for deterministic builds
  fileList.sort();

  for (const relative of fileList) {
    const source = path.join(rootDir, relative);
    const stat = fs.statSync(source);
    totalBytes += stat.size;

    if (stat.size > MAX_ASSET_BYTES) {
      oversized.push([relative, stat.size]);
    }

    const destination = path.join(outDir, relative);
    const destDir = path.dirname(destination);
    fs.mkdirSync(destDir, { recursive: true });
    fs.copyFileSync(source, destination);
  }

  if (oversized.length > 0) {
    for (const [rel, size] of oversized) {
      console.error(
        `error: ${rel} is ${(size / 1048576).toFixed(1)} MiB, over the ${(MAX_ASSET_BYTES / 1048576).toFixed(0)} MiB Cloudflare asset limit`
      );
    }
    return 1;
  }

  for (const required of ['index.html', '404.html']) {
    if (!fs.existsSync(path.join(outDir, required))) {
      console.error(`error: ${required} missing from build output`);
      return 1;
    }
  }

  console.log(`Built ${fileList.length} files (${(totalBytes / 1048576).toFixed(1)} MiB) into ${outDir}`);
  return 0;
}

// Direct CLI execution
if (process.argv[1] && path.resolve(process.argv[1]) === __filename) {
  let outArg = path.resolve(ROOT, 'dist');
  const outIdx = process.argv.indexOf('--out');
  if (outIdx !== -1 && process.argv[outIdx + 1]) {
    outArg = path.resolve(process.argv[outIdx + 1]);
  }
  const code = build(ROOT, outArg);
  process.exit(code);
}
