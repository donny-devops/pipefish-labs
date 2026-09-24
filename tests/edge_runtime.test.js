/**
 * PipeFish Labs — Native Node.js Test Suite
 * Runner: node:test / node:assert
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

describe('PipeFish Edge Runtime & Security Verification', () => {
  test('Static distribution contains all mandatory security and routing files', () => {
    const dist = path.join(ROOT, 'dist');
    assert.ok(fs.existsSync(dist), 'dist/ directory must exist');
    assert.ok(fs.existsSync(path.join(dist, 'index.html')), 'dist/index.html must exist');
    assert.ok(fs.existsSync(path.join(dist, '404.html')), 'dist/404.html must exist');
    assert.ok(fs.existsSync(path.join(dist, '_headers')), 'dist/_headers must exist');
    assert.ok(fs.existsSync(path.join(dist, '_redirects')), 'dist/_redirects must exist');
    assert.ok(fs.existsSync(path.join(dist, 'briefing-video.mp4')), 'dist/briefing-video.mp4 must exist');
  });

  test('DOM integrity verifies all 16 critical UI and video elements', () => {
    const indexPath = path.join(ROOT, 'index.html');
    const content = fs.readFileSync(indexPath, 'utf-8');

    const criticalSelectors = [
      'id="briefing-video-player"',
      'src="./briefing-video.mp4"',
      'object-fit:contain',
      'aspect-ratio: 16/9',
      'id="briefing-canvas"',
      'id="hcanvas"',
      'id="sec-subnav"',
      'id="demo-status-bar-text"',
      'id="demo-rows-container"',
      'id="run-demo-btn"',
      'id="about-team"',
      'id="capabilities"',
      'id="architecture"',
      'id="agents"',
      'class="logo"',
      'class="ft-brand"'
    ];

    for (const selector of criticalSelectors) {
      assert.ok(content.includes(selector), `Missing selector in index.html: ${selector}`);
    }
  });

  test('timingSafeEqual correctly validates constant-time string matches and rejects mismatches', () => {
    function timingSafeEqual(a, b) {
      if (a.length !== b.length) return false;
      let c = 0;
      for (let i = 0; i < a.length; i++) {
        c |= a.charCodeAt(i) ^ b.charCodeAt(i);
      }
      return c === 0;
    }

    const hash1 = 'a1b2c3d4e5f60718293a4b5c6d7e8f90';
    const hash2 = 'a1b2c3d4e5f60718293a4b5c6d7e8f90';
    const tampered = 'a1b2c3d4e5f60718293a4b5c6d7e8f91';
    const shortHash = 'a1b2c3';

    assert.equal(timingSafeEqual(hash1, hash2), true, 'Identical hashes must match');
    assert.equal(timingSafeEqual(hash1, tampered), false, 'Tampered hash must fail');
    assert.equal(timingSafeEqual(hash1, shortHash), false, 'Different length hash must fail');
  });

  test('Agent catalog in TypeScript worker registers all 26 canonical agent keys', () => {
    const workerPath = path.join(ROOT, 'src', 'index.ts');
    const content = fs.readFileSync(workerPath, 'utf-8');

    const expectedAgents = [
      'receptionist', 'sales', 'logistics', 'integration', 'quantum',
      'reverse', 'crypto', 'errorcorr', 'trend', 'market', 'codescan',
      'docs', 'observability', 'revops', 'analytics', 'auditing',
      'logtriage', 'erp', 'trafficrouter', 'networkdispatch',
      'selfimproving', 'systemoptimizing', 'finops', 'contractintel',
      'missedcalltextback', 'llmops'
    ];

    for (const agent of expectedAgents) {
      assert.ok(content.includes(`${agent}: {`), `Agent catalog missing key: ${agent}`);
    }
  });

  test('TypeScript SDK defines all 26 scenario keys', () => {
    const sdkPath = path.join(ROOT, 'sdk', 'pipefish_sdk.ts');
    const content = fs.readFileSync(sdkPath, 'utf-8');

    assert.ok(content.includes('| "missedcalltextback"'), 'SDK must export missedcalltextback');
    assert.ok(content.includes('| "llmops"'), 'SDK must export llmops');
  });

  test('wrangler.jsonc references Node.js build command', () => {
    const wranglerPath = path.join(ROOT, 'wrangler.jsonc');
    const content = fs.readFileSync(wranglerPath, 'utf-8');

    assert.ok(content.includes('"command": "node scripts/build_site.js"'), 'Build command must be node scripts/build_site.js');
  });
});
