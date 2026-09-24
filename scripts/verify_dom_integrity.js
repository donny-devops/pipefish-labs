#!/usr/bin/env node
/**
 * PipeFish Labs - DOM & Media Integrity Verifier (Node.js)
 *
 * Verifies that all 16 critical interactive and video DOM selectors exist in index.html,
 * and confirms that the briefing-video.mp4 asset is non-empty.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const REQUIRED_ELEMENTS = [
  ['id="briefing-video-player"', 'Executive Briefing MP4 Video Player (#briefing-video-player)'],
  ['src="./briefing-video.mp4"', 'Executive Briefing MP4 Source Path (./briefing-video.mp4)'],
  ['object-fit:contain', 'Uncropped Video Aspect Ratio Rule (object-fit:contain)'],
  ['aspect-ratio: 16/9', 'Widescreen Theater Aspect Ratio Rule (aspect-ratio: 16/9)'],
  ['id="briefing-canvas"', 'Executive Briefing Video Canvas (#briefing-canvas)'],
  ['id="hcanvas"', 'Hero Node Network Canvas (#hcanvas)'],
  ['id="sec-subnav"', 'Page Index Sticky Sub-nav (#sec-subnav)'],
  ['id="demo-status-bar-text"', 'Agent Simulator Status Bar (#demo-status-bar-text)'],
  ['id="demo-rows-container"', 'Agent Simulator Rows Container (#demo-rows-container)'],
  ['id="run-demo-btn"', 'Agent Simulator Run Button (#run-demo-btn)'],
  ['id="about-team"', 'Executive Leadership & Engineering Section (#about-team)'],
  ['id="capabilities"', 'Capabilities Section (#capabilities)'],
  ['id="architecture"', 'Workflow Architecture Section (#architecture)'],
  ['id="agents"', 'Autonomous Multi-Agent Section (#agents)'],
  ['class="logo"', 'Header Logo (.logo)'],
  ['class="ft-brand"', 'Footer Brand Section (.ft-brand)'],
];

export function verifyDom(filepath = path.join(ROOT, 'index.html')) {
  if (!fs.existsSync(filepath)) {
    console.error(`[ERROR] ${filepath} not found!`);
    return 1;
  }

  // Check physical MP4 video file existence and non-zero size (>100 KB)
  const videoFile = path.join(ROOT, 'briefing-video.mp4');
  if (!fs.existsSync(videoFile) || fs.statSync(videoFile).size < 100000) {
    console.error(`[FAIL] CRITICAL MEDIA FILE MISSING OR CORRUPTED: ${videoFile}`);
    return 1;
  }

  const content = fs.readFileSync(filepath, 'utf-8');
  const missing = [];

  for (const [snippet, label] of REQUIRED_ELEMENTS) {
    if (!content.includes(snippet)) {
      missing.push(label);
    }
  }

  if (missing.length > 0) {
    console.error('[FAIL] DOM & MEDIA INTEGRITY VIOLATION DETECTED!');
    console.error('The following critical elements or video rules are missing from index.html:');
    for (const item of missing) {
      console.error(`  - ${item}`);
    }
    return 1;
  }

  console.log('[PASS] DOM & MEDIA INTEGRITY VERIFIED: All critical elements, aspect ratio rules, and MP4 video exist.');
  return 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === __filename) {
  const code = verifyDom();
  process.exit(code);
}
