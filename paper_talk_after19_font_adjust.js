#!/usr/bin/env node

const fs = require('node:fs/promises');
const path = require('node:path');
const JSZip = require('jszip');

const DEFAULT_SIZE_REPLACEMENTS = [
  ['sz="1060"', 'sz="1120"'], // 10.6pt -> 11.2pt
  ['sz="1150"', 'sz="1230"'], // 11.5pt -> 12.3pt
  ['sz="1220"', 'sz="1300"'], // 12.2pt -> 13.0pt
  ['sz="1320"', 'sz="1400"'], // 13.2pt -> 14.0pt
  ['sz="1340"', 'sz="1400"'], // 13.4pt -> 14.0pt
  ['sz="1360"', 'sz="1400"'], // 13.6pt -> 14.0pt
];

const SHAPE_OVERRIDES = {
  21: {
    // Keep this dense caption slightly smaller than the global 11.2pt bump
    // so it does not grow too aggressively.
    'Text 23': [['sz="1120"', 'sz="1100"']],
  },
};

function replaceAll(haystack, from, to) {
  return haystack.split(from).join(to);
}

function applyReplacements(xml, replacements) {
  let out = xml;
  let count = 0;
  for (const [from, to] of replacements) {
    const occurrences = out.split(from).length - 1;
    if (occurrences > 0) {
      out = replaceAll(out, from, to);
      count += occurrences;
    }
  }
  return { xml: out, count };
}

function transformSlideXml(slideNumber, xml) {
  const shapeRegex = /<p:sp\b[\s\S]*?<\/p:sp>/g;
  let replacementCount = 0;

  const transformed = xml.replace(shapeRegex, (shapeXml) => {
    const nameMatch = shapeXml.match(/<p:cNvPr[^>]*name="([^"]+)"/);
    const shapeName = nameMatch?.[1] || '';

    let next = shapeXml;
    const defaultResult = applyReplacements(next, DEFAULT_SIZE_REPLACEMENTS);
    next = defaultResult.xml;
    replacementCount += defaultResult.count;

    const overrideReplacements = SHAPE_OVERRIDES[slideNumber]?.[shapeName];
    if (overrideReplacements) {
      const overrideResult = applyReplacements(next, overrideReplacements);
      next = overrideResult.xml;
      replacementCount += overrideResult.count;
    }

    return next;
  });

  return { xml: transformed, replacementCount };
}

async function main() {
  const [, , inputPath, outputPath] = process.argv;
  if (!inputPath || !outputPath) {
    console.error('Usage: node adjust_font_sizes.js <input.pptx> <output.pptx>');
    process.exit(1);
  }

  const inputBuffer = await fs.readFile(inputPath);
  const zip = await JSZip.loadAsync(inputBuffer);

  const slideSummaries = [];
  for (let slideNumber = 20; slideNumber <= 30; slideNumber += 1) {
    const slidePath = `ppt/slides/slide${slideNumber}.xml`;
    const file = zip.file(slidePath);
    if (!file) continue;

    const xml = await file.async('string');
    const result = transformSlideXml(slideNumber, xml);
    zip.file(slidePath, result.xml);
    slideSummaries.push({
      slideNumber,
      replacements: result.replacementCount,
    });
  }

  const outputBuffer = await zip.generateAsync({
    type: 'nodebuffer',
    compression: 'DEFLATE',
    compressionOptions: { level: 9 },
  });

  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, outputBuffer);

  console.log('Font adjustments complete.');
  for (const { slideNumber, replacements } of slideSummaries) {
    console.log(`slide ${slideNumber}: ${replacements} size token replacements`);
  }
  console.log(`Wrote: ${outputPath}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
