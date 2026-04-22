const path = require('path');
const { execFileSync } = require('child_process');
const PptxGenJS = require('pptxgenjs');
const { imageSizingContain } = require('./.cache/flexrl_talk_build/pptxgenjs_helpers/image');
const {
  warnIfSlideHasOverlaps,
  warnIfSlideElementsOutOfBounds,
} = require('./.cache/flexrl_talk_build/pptxgenjs_helpers/layout');

const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'OpenAI Codex';
pptx.company = 'wangzerui';
pptx.subject = 'FlexRL ICLR 2026 paper talk';
pptx.title = 'FlexRL: Scaling VLM RL Training via Efficient Load Balancing';
pptx.lang = 'en-US';
pptx.theme = {
  headFontFace: 'Arial',
  bodyFontFace: 'Arial',
  lang: 'en-US',
};
pptx.defineLayout({ name: 'WIDE_SAFE', width: 13.333, height: 7.5 });
pptx.layout = 'WIDE_SAFE';

const W = 13.333;
const H = 7.5;
const M = 0.52;
const COLORS = {
  bg: '050816',
  text: 'F8FAFC',
  subtext: 'CBD5E1',
  muted: '94A3B8',
  border: '334155',
  light: '0F172A',
  lighter: '111827',
  blue: '60A5FA',
  blueLite: '102A43',
  green: '34D399',
  greenLite: '0C2B24',
  red: 'F87171',
  redLite: '331818',
  amber: 'FBBF24',
  amberLite: '34270A',
  purple: 'A78BFA',
  purpleLite: '25163E',
  slate: '1E293B',
};

const ASSET = (name) =>
  path.join(__dirname, '.cache', 'flexrl_talk_build', 'assets', name);

function addSlideBase(slide, title, subtitle = '') {
  slide.background = { color: COLORS.bg };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: W,
    h: 0.14,
    line: { color: COLORS.blue, transparency: 100 },
    fill: { color: COLORS.blue },
  });
  slide.addText(title, {
    x: M,
    y: 0.28,
    w: 9.6,
    h: 0.38,
    fontFace: 'Arial',
    fontSize: 24,
    bold: true,
    color: COLORS.text,
    margin: 0,
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: M,
      y: 0.69,
      w: 10.6,
      h: 0.24,
      fontFace: 'Arial',
      fontSize: 10.5,
      color: COLORS.muted,
      margin: 0,
    });
  }
  slide.addShape(pptx.ShapeType.rect, {
    x: M,
    y: 0.98,
    w: W - 2 * M,
    h: 0.02,
    line: { color: COLORS.border, transparency: 100 },
    fill: { color: COLORS.border },
  });
  slide.addText('FlexRL · ICLR 2026', {
    x: 10.55,
    y: 0.32,
    w: 2.25,
    h: 0.2,
    fontFace: 'Arial',
    fontSize: 9,
    color: COLORS.muted,
    align: 'right',
    margin: 0,
  });
}

function addFooter(slide, pageNum) {
  slide.addText(String(pageNum), {
    x: 12.55,
    y: 7.13,
    w: 0.25,
    h: 0.14,
    fontFace: 'Arial',
    fontSize: 9,
    color: COLORS.muted,
    align: 'right',
    margin: 0,
  });
}

function addCard(slide, x, y, w, h, title, body, opts = {}) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h,
    rectRadius: 0.08,
    line: { color: opts.border || COLORS.border, pt: 1 },
    fill: { color: opts.fill || COLORS.light },
  });
  slide.addText(title, {
    x: x + 0.2,
    y: y + 0.16,
    w: w - 0.4,
    h: 0.24,
    fontFace: 'Arial',
    fontSize: opts.titleSize || 15,
    bold: true,
    color: opts.titleColor || COLORS.text,
    margin: 0,
  });
  slide.addText(body, {
    x: x + 0.2,
    y: y + 0.48,
    w: w - 0.4,
    h: h - 0.62,
    fontFace: 'Arial',
    fontSize: opts.bodySize || 11.5,
    color: opts.bodyColor || COLORS.subtext,
    margin: 0,
    valign: 'top',
    breakLine: false,
  });
}

function addMetricCard(slide, x, y, w, h, label, value, note, opts = {}) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h,
    rectRadius: 0.08,
    line: { color: opts.border || COLORS.border, pt: 1 },
    fill: { color: opts.fill || COLORS.light },
  });
  slide.addText(label, {
    x: x + 0.18,
    y: y + 0.14,
    w: w - 0.36,
    h: 0.18,
    fontFace: 'Arial',
    fontSize: 11,
    bold: true,
    color: opts.labelColor || COLORS.subtext,
    margin: 0,
    align: 'center',
  });
  slide.addText(value, {
    x: x + 0.1,
    y: y + 0.5,
    w: w - 0.2,
    h: 0.55,
    fontFace: 'Arial',
    fontSize: opts.valueSize || 24,
    bold: true,
    color: opts.valueColor || COLORS.blue,
    align: 'center',
    margin: 0,
  });
  const noteHeight = h - 1.28;
  if (note && noteHeight > 0.08) {
    slide.addText(note, {
      x: x + 0.15,
      y: y + 1.16,
      w: w - 0.3,
      h: noteHeight,
      fontFace: 'Arial',
      fontSize: 10.5,
      color: COLORS.subtext,
      align: 'center',
      valign: 'mid',
      margin: 0,
    });
  }
}

function addBullet(slide, text, x, y, w, h = 0.46, opts = {}) {
  slide.addText(text, {
    x,
    y,
    w,
    h,
    fontFace: 'Arial',
    fontSize: opts.fontSize || 15,
    color: opts.color || COLORS.text,
    margin: 0,
    valign: 'mid',
    bullet: { indent: opts.indent || 16 },
  });
}

function addPill(slide, text, x, y, w, fill, color) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h: 0.34,
    rectRadius: 0.08,
    line: { color: fill, transparency: 100 },
    fill: { color: fill },
  });
  slide.addText(text, {
    x,
    y: y + 0.08,
    w,
    h: 0.14,
    fontFace: 'Arial',
    fontSize: 10,
    color,
    bold: true,
    align: 'center',
    margin: 0,
  });
}

function addCaption(slide, text, x, y, w) {
  slide.addText(text, {
    x,
    y,
    w,
    h: 0.16,
    fontFace: 'Arial',
    fontSize: 8.5,
    italic: true,
    color: COLORS.muted,
    margin: 0,
    align: 'center',
  });
}

function finalizeSlide(slide, pageNum) {
  addFooter(slide, pageNum);
  warnIfSlideHasOverlaps(slide, pptx, {
    muteContainment: true,
    ignoreLines: true,
    ignoreDecorativeShapes: true,
  });
  warnIfSlideElementsOutOfBounds(slide, pptx);
}

// Slide 1
{
  const slide = pptx.addSlide();
  slide.background = { color: COLORS.bg };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: W,
    h: 0.18,
    line: { color: COLORS.blue, transparency: 100 },
    fill: { color: COLORS.blue },
  });
  slide.addText('FlexRL: Scaling VLM RL Training via Efficient Load Balancing', {
    x: 0.72,
    y: 1.08,
    w: 8.6,
    h: 0.95,
    fontFace: 'Arial',
    fontSize: 24,
    bold: true,
    color: COLORS.text,
    margin: 0,
    valign: 'mid',
  });
  slide.addText('ICLR 2026 camera-ready', {
    x: 0.74,
    y: 2.12,
    w: 2.2,
    h: 0.2,
    fontFace: 'Arial',
    fontSize: 9.8,
    bold: true,
    color: COLORS.muted,
    margin: 0,
  });
  slide.addText('Zerui Wang, Qinghao Hu, Chang Chen, Jiecheng Zhou,\nHaojie Duanmu, Xingcheng Zhang, Peng Sun, Dahua Lin', {
    x: 0.74,
    y: 2.36,
    w: 8.1,
    h: 0.44,
    fontFace: 'Arial',
    fontSize: 10.6,
    color: COLORS.subtext,
    margin: 0,
  });
  slide.addText('Shanghai Jiao Tong University · Shanghai AI Lab · MIT · USTC · Peking University · CUHK', {
    x: 0.74,
    y: 2.88,
    w: 8.1,
    h: 0.28,
    fontFace: 'Arial',
    fontSize: 10.2,
    color: COLORS.muted,
    margin: 0,
  });
  slide.addText('An end-to-end system for VLM RL: ShadowLoader removes multimodal data bottlenecks, and FlexUlysses balances heterogeneous compute and memory across GPUs.', {
    x: 0.76,
    y: 3.18,
    w: 5.55,
    h: 1.05,
    fontFace: 'Arial',
    fontSize: 16,
    color: COLORS.text,
    margin: 0,
    valign: 'mid',
  });
  addPill(slide, 'ShadowLoader', 0.78, 4.5, 1.52, COLORS.greenLite, COLORS.green);
  addPill(slide, 'FlexUlysses', 2.44, 4.5, 1.52, COLORS.blueLite, COLORS.blue);
  addPill(slide, '128-GPU clusters', 4.1, 4.5, 1.76, COLORS.amberLite, COLORS.amber);
  addMetricCard(slide, 9.45, 1.18, 3.0, 2.2, 'Peak end-to-end speedup', '8.47×', 'Compared with veRL bucketing or fixed-degree Ulysses-SP, depending on feasibility.', {
    fill: COLORS.blueLite,
    border: 'BFDBFE',
    valueColor: COLORS.blue,
  });
  addMetricCard(slide, 9.45, 3.74, 3.0, 1.82, 'Core system components', '2', 'ShadowLoader for data loading; FlexUlysses for execution load balancing.', {
    fill: COLORS.greenLite,
    border: 'A7F3D0',
    valueColor: COLORS.green,
    valueSize: 24,
  });
  slide.addText('Talk outline: problem → system design → evaluation → takeaways', {
    x: 9.55,
    y: 6.13,
    w: 2.8,
    h: 0.45,
    fontFace: 'Arial',
    fontSize: 11,
    color: COLORS.subtext,
    align: 'center',
    margin: 0,
  });
  finalizeSlide(slide, 1);
}

// Slide 2
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'Executive Summary', 'What the paper diagnoses, builds, and demonstrates end-to-end.');
  addCard(slide, 0.65, 1.35, 3.95, 4.95, '1. Problem',
    'VLM RL training breaks down for two separate reasons:\n\n• Multimodal data loading is centralized on a single controller, causing CPU I/O stragglers and host-memory pressure.\n\n• Batches mix short image-text prompts with long video contexts, creating severe per-GPU compute and memory imbalance.\n\nOptimizing only one side still leaves the other as the dominant bottleneck.',
    { fill: COLORS.light }
  );
  addCard(slide, 4.69, 1.35, 3.95, 4.95, '2. System',
    'FlexRL combines two tightly coupled components:\n\n• ShadowLoader: metadata-only scheduling on the controller, with worker-side preprocessing, caching, and asynchronous materialization.\n\n• FlexUlysses: adaptive sub-sequence sharding, hierarchical device groups, and deadlock-free overlapped execution.\n\nThe two pieces are co-designed so sharding decisions can inform data loading early.',
    { fill: COLORS.light }
  );
  addCard(slide, 8.73, 1.35, 3.95, 4.95, '3. Impact',
    'Across MiMo-VL-7B-RL and Qwen2.5-VL-32B on two 128-GPU clusters, FlexRL delivers:\n\n• up to 8.47× end-to-end throughput improvement\n• 117.42× data-loading throughput improvement\n• balance ratio driven down to 1.0 in the Ulysses comparison\n\nThe gains grow as workloads become more multimodal and sequence skew becomes more extreme.',
    { fill: COLORS.light }
  );
  finalizeSlide(slide, 2);
}

// Slide 3
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'Why VLM RL Training is Hard', 'The paper identifies one data bottleneck and one execution bottleneck.');
  addCard(slide, 0.68, 1.34, 5.8, 4.95, 'Bottleneck A — Data preparation on the controller', '', {
    fill: COLORS.greenLite,
    border: 'A7F3D0',
    titleColor: COLORS.green,
  });
  addBullet(slide, 'Image/video decoding, frame sampling, and preprocessing are CPU- and I/O-heavy.', 0.95, 2.0, 5.1, 0.54, { fontSize: 15, color: COLORS.subtext });
  addBullet(slide, 'In the veRL multimodal baseline, data loading takes 57.1% of the iteration time.', 0.95, 2.64, 5.1, 0.54, { fontSize: 15, color: COLORS.subtext });
  addBullet(slide, 'As batch size grows, the controller becomes the single straggler and can hit host-memory OOM.', 0.95, 3.28, 5.1, 0.72, { fontSize: 15, color: COLORS.subtext });
  addMetricCard(slide, 1.05, 4.48, 2.35, 1.42, 'Observed in baseline', '57.1%', 'of step time spent on data loading', {
    fill: COLORS.lighter,
    border: 'A7F3D0',
    valueColor: COLORS.green,
    valueSize: 22,
  });
  addMetricCard(slide, 3.65, 4.48, 2.35, 1.42, 'Failure mode', 'OOM', 'Controller-side CPU memory becomes the bottleneck', {
    fill: COLORS.lighter,
    border: 'A7F3D0',
    valueColor: COLORS.red,
    valueSize: 22,
  });

  addCard(slide, 6.85, 1.34, 5.8, 4.95, 'Bottleneck B — Cross-GPU execution imbalance', '', {
    fill: COLORS.blueLite,
    border: 'BFDBFE',
    titleColor: COLORS.blue,
  });
  addBullet(slide, 'Attention compute grows quadratically with sequence length, while activation memory grows linearly.', 7.12, 2.0, 5.1, 0.72, { fontSize: 15, color: COLORS.subtext });
  addBullet(slide, 'Text length is a poor proxy for visual cost: image counts and video frame counts change both compute and memory.', 7.12, 2.78, 5.1, 0.76, { fontSize: 15, color: COLORS.subtext });
  addBullet(slide, 'Length-only bucketing can still leave one DP rank as the straggler—or even OOM on long contexts.', 7.12, 3.62, 5.1, 0.76, { fontSize: 15, color: COLORS.subtext });
  addMetricCard(slide, 7.25, 4.48, 2.35, 1.42, 'Skew source', 'Mixed modalities', 'short image-text + long video-text in the same RL batch', {
    fill: COLORS.lighter,
    border: 'BFDBFE',
    valueColor: COLORS.blue,
    valueSize: 16,
  });
  addMetricCard(slide, 9.85, 4.48, 2.35, 1.42, 'Why prior work falls short', 'Bucketing ≠ balancing', 'fixed parallelism or coarse buckets cannot eliminate stragglers', {
    fill: COLORS.lighter,
    border: 'BFDBFE',
    valueColor: COLORS.red,
    valueSize: 15,
  });
  finalizeSlide(slide, 3);
}

// Slide 4
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'FlexRL Overview', 'The system addresses data loading and execution imbalance together, not in isolation.');
  slide.addText('Core idea', {
    x: 0.75,
    y: 1.42,
    w: 2.1,
    h: 0.25,
    fontFace: 'Arial',
    fontSize: 16,
    bold: true,
    color: COLORS.text,
    margin: 0,
  });
  addBullet(slide, 'ShadowLoader decentralizes multimodal preprocessing and keeps only lightweight metadata on the controller.', 0.8, 1.88, 3.65, 0.78, { fontSize: 15, color: COLORS.subtext });
  addBullet(slide, 'FlexUlysses shards only the sequences that need it, balancing both compute and memory at sub-sequence granularity.', 0.8, 2.78, 3.65, 0.92, { fontSize: 15, color: COLORS.subtext });
  addBullet(slide, 'The two components are co-designed so sharding decisions can guide slice-aware data loading and reduce transfer volume.', 0.8, 3.88, 3.65, 0.94, { fontSize: 15, color: COLORS.subtext });
  addMetricCard(slide, 0.88, 5.45, 3.25, 0.95, 'Design principle', 'Optimize the whole RL loop', 'Remove CPU bubbles and GPU stragglers at the same time.', {
    fill: COLORS.light,
    border: COLORS.border,
    valueColor: COLORS.text,
    valueSize: 14,
  });

  const overview = ASSET('real_overview__v3.png');
  slide.addImage({ path: overview, ...imageSizingContain(overview, 4.8, 1.32, 7.9, 5.8) });
  addCaption(slide, 'Paper figure: traditional pipeline vs. FlexRL (ShadowLoader + FlexUlysses).', 5.15, 6.72, 7.2);
  finalizeSlide(slide, 4);
}

// Slide 5
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'ShadowLoader', 'Metadata-driven loading that removes the single-controller bottleneck.');

  slide.addText('Workflow', {
    x: 0.74,
    y: 1.38,
    w: 1.25,
    h: 0.22,
    fontFace: 'Arial',
    fontSize: 16,
    bold: true,
    color: COLORS.text,
    margin: 0,
  });

  const flowY = 1.95;
  const boxW = 2.2;
  const gap = 0.32;
  const x0 = 0.78;
  const boxes = [
    ['Proxy\nDataloader', 'Controller keeps FakeTensor metadata only'],
    ['Local\nPreprocessor', 'Worker-side decode, frame sampling, and caching'],
    ['MetaStore', 'Track sample ID → physical location mapping'],
    ['Materializer', 'Workers fetch actual visual tensors on demand'],
  ];
  boxes.forEach((b, i) => {
    const x = x0 + i * (boxW + gap);
    slide.addShape(pptx.ShapeType.roundRect, {
      x,
      y: flowY,
      w: boxW,
      h: 1.4,
      rectRadius: 0.08,
      line: { color: i % 2 === 0 ? 'A7F3D0' : 'BFDBFE', pt: 1 },
      fill: { color: i % 2 === 0 ? COLORS.greenLite : COLORS.blueLite },
    });
    slide.addText(b[0], {
      x: x + 0.15,
      y: flowY + 0.18,
      w: boxW - 0.3,
      h: 0.35,
      fontFace: 'Arial',
      fontSize: 15,
      bold: true,
      color: COLORS.text,
      align: 'center',
      margin: 0,
    });
    slide.addText(b[1], {
      x: x + 0.15,
      y: flowY + 0.62,
      w: boxW - 0.3,
      h: 0.55,
      fontFace: 'Arial',
      fontSize: 11,
      color: COLORS.subtext,
      align: 'center',
      valign: 'mid',
      margin: 0,
    });
    if (i < boxes.length - 1) {
      slide.addText('→', {
        x: x + boxW + 0.06,
        y: flowY + 0.5,
        w: 0.18,
        h: 0.18,
        fontFace: 'Arial',
        fontSize: 18,
        bold: true,
        color: COLORS.muted,
        margin: 0,
        align: 'center',
      });
    }
  });

  addCard(slide, 0.8, 4.02, 5.55, 2.22, 'Key mechanisms',
    '• FakeTensor placeholders preserve compatibility with the RL pipeline while storing only metadata on the controller.\n\n• Prefetching and asynchronous materialization overlap I/O, CPU preprocessing, and network transfer with GPU computation.\n\n• FlexUlysses-aware loading fetches only the needed slices (e.g., frame ranges) once sharding is decided.',
    { fill: COLORS.light, bodySize: 10.9 }
  );

  addMetricCard(slide, 6.72, 4.18, 2.55, 1.7, 'ShadowLoader alone', '84.09×', 'data-loading throughput improvement', {
    fill: COLORS.greenLite,
    border: 'A7F3D0',
    valueColor: COLORS.green,
  });
  addMetricCard(slide, 9.55, 4.18, 2.55, 1.7, 'With FlexUlysses', '117.42×', 'data-loading throughput improvement', {
    fill: COLORS.blueLite,
    border: 'BFDBFE',
    valueColor: COLORS.blue,
  });
  finalizeSlide(slide, 5);
}

// Slide 6
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'FlexUlysses Motivation', 'Bucketing cannot fully solve multimodal skew in either the short- or long-sequence regime.');
  const imbalance = ASSET('imbalance.png');
  slide.addImage({ path: imbalance, ...imageSizingContain(imbalance, 0.64, 1.25, 12.05, 4.85) });
  addCaption(slide, 'Paper figure: left shows token-length distributions; middle/right compare bucketing with FlexUlysses on shorter and longer sequences.', 1.1, 6.02, 11.1);
  addCard(slide, 0.75, 6.28, 3.9, 0.78, 'Observation 1', 'Even when memory does not force SP, one long sample can dominate the entire RL step.', {
    fill: COLORS.light, bodySize: 10.8
  });
  addCard(slide, 4.72, 6.28, 3.9, 0.78, 'Observation 2', 'For longer contexts, fixed buckets may still OOM or leave severe attention imbalance.', {
    fill: COLORS.light, bodySize: 10.8
  });
  addCard(slide, 8.69, 6.28, 3.9, 0.78, 'Key insight', 'Use Ulysses chunks as scheduling units, and shard sequences only as much as needed.', {
    fill: COLORS.purpleLite, border: 'C4B5FD', titleColor: COLORS.purple, bodySize: 10.8
  });
  finalizeSlide(slide, 6);
}

// Slide 7
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'FlexUlysses Design', 'Adaptive sharding is only useful if planning and execution remain low-overhead and deadlock-free.');
  addCard(slide, 0.72, 1.42, 3.95, 4.85, '1. Adaptive sharding degree',
    'For each sequence i, choose p_i ∈ {1, 2, 4, …, p_max} based on its length and the current batch composition.\n\nMost sequences stay unsharded or lightly sharded, which preserves compute efficiency and avoids paying communication on every sample.',
    { fill: COLORS.blueLite, border: 'BFDBFE', titleColor: COLORS.blue }
  );
  addCard(slide, 4.82, 1.42, 3.95, 4.85, '2. Hierarchical device groups',
    'Candidate groups are nested (for example, on 8 GPUs: [0-7], [0-3]/[4-7], [0,1]/[2,3]/…).\n\nThis laminar structure makes placement simpler: any two groups are either disjoint or one contains the other, which is the basis for deadlock-free scheduling.',
    { fill: COLORS.greenLite, border: 'A7F3D0', titleColor: COLORS.green }
  );
  addCard(slide, 8.92, 1.42, 3.7, 4.85, '3. Highest-Sharding-First + overlap',
    'All ranks execute larger collectives before smaller ones, ensuring a consistent order across nested groups.\n\nWithin this schedule, FlexRL packs short sequences into sequence groups and overlaps all2all communication with attention computation to reduce GPU bubbles.',
    { fill: COLORS.amberLite, border: 'FCD34D', titleColor: COLORS.amber }
  );
  addCard(slide, 3.08, 6.14, 7.2, 0.98, 'Important implementation detail',
    'Vision tower balancing is handled separately by evenly distributing images and video frames across GPUs.',
    {
    fill: COLORS.light,
    border: COLORS.border,
    titleSize: 12,
    bodySize: 11.4,
  });
  finalizeSlide(slide, 7);
}

// Slide 8
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'Evaluation Setup', 'Large-scale experiments cover two hardware platforms, two model scales, and three workload mixes.');
  addCard(slide, 0.72, 1.42, 3.9, 4.95, 'Hardware',
    '• Two 128-GPU clusters (16 nodes × 8 GPUs)\n• NVIDIA H800 and NVIDIA H200\n• NVLink/NVSwitch intra-node bandwidth: 400 GB/s (H800) and 900 GB/s (H200)\n• RoCEv2 RDMA inter-node connectivity',
    { fill: COLORS.light }
  );
  addCard(slide, 4.74, 1.42, 3.9, 4.95, 'Models & training',
    '• MiMo-VL-7B-RL and Qwen2.5-VL-32B\n• GRPO for all experiments\n• max response length = 1024\n• max sharding budget p_max = 8',
    { fill: COLORS.light }
  );
  addCard(slide, 8.76, 1.42, 3.9, 4.95, 'Datasets & baselines',
    '• Geo3K (image-text), NExTQA (short video), LongVILA-Reason (long video)\n• Image-heavy = 5:2:1\n• Video-heavy = 1:2:5\n• Only-video = LongVILA-Reason only\n• Baselines: veRL+Bucketing and fixed-degree Ulysses-SP',
    { fill: COLORS.light }
  );
  addPill(slide, 'H800', 1.2, 6.55, 0.86, COLORS.blueLite, COLORS.blue);
  addPill(slide, 'H200', 2.16, 6.55, 0.86, COLORS.greenLite, COLORS.green);
  addPill(slide, '7B', 5.18, 6.55, 0.72, COLORS.amberLite, COLORS.amber);
  addPill(slide, '32B', 5.99, 6.55, 0.82, COLORS.redLite, COLORS.red);
  addPill(slide, 'Geo3K', 8.98, 6.55, 1.0, COLORS.blueLite, COLORS.blue);
  addPill(slide, 'NExTQA', 10.08, 6.55, 1.05, COLORS.greenLite, COLORS.green);
  addPill(slide, 'LongVILA-Reason', 11.23, 6.55, 1.38, COLORS.purpleLite, COLORS.purple);
  finalizeSlide(slide, 8);
}

// Slide 9
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'Main Results', 'Peak end-to-end speedup reported in the paper, by workload mix.');
  addMetricCard(slide, 0.88, 1.65, 3.65, 3.35, 'Image-heavy', '7.35×', 'Geo3K : NExTQA : LongVILA-Reason = 5 : 2 : 1', {
    fill: COLORS.blueLite,
    border: 'BFDBFE',
    valueColor: COLORS.blue,
    valueSize: 30,
  });
  addMetricCard(slide, 4.86, 1.65, 3.65, 3.35, 'Video-heavy', '5.35×', 'Geo3K : NExTQA : LongVILA-Reason = 1 : 2 : 5', {
    fill: COLORS.greenLite,
    border: 'A7F3D0',
    valueColor: COLORS.green,
    valueSize: 30,
  });
  addMetricCard(slide, 8.84, 1.65, 3.65, 3.35, 'Only-video', '8.47×', 'LongVILA-Reason only; longest and most heterogeneous sequences', {
    fill: COLORS.redLite,
    border: 'FCA5A5',
    valueColor: COLORS.red,
    valueSize: 30,
  });
  addCard(slide, 0.88, 5.35, 5.82, 1.15, 'What this means',
    'FlexRL delivers the largest gains exactly where multimodal skew is the strongest: larger models, longer videos, and more heterogeneous batches.',
    { fill: COLORS.light, bodySize: 12 }
  );
  addCard(slide, 6.9, 5.35, 5.6, 1.15, 'Baseline note',
    'Speedups are computed against veRL Bucketing when it is feasible; otherwise the paper compares against fixed-degree Ulysses-SP because Bucketing OOMs.',
    { fill: COLORS.light, bodySize: 12 }
  );
  finalizeSlide(slide, 9);
}

// Slide 10
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'Comparison with Fixed-Degree Ulysses-SP', 'Adaptive sharding outperforms fixed SP because it avoids over-sharding short sequences.');
  const comm = ASSET('comm_overhead_h200_detailed_v4.png');
  slide.addImage({ path: comm, ...imageSizingContain(comm, 0.72, 1.32, 12.0, 4.55) });
  addCaption(slide, 'Paper figure: fixed-degree Ulysses-SP vs. FlexUlysses on per-stage time, throughput, and balance ratio.', 1.0, 5.9, 11.4);
  addCard(slide, 0.86, 6.1, 3.85, 0.92, 'Takeaway 1', 'Higher fixed SP degrees improve balance, but communication overhead quickly dominates.', { fill: COLORS.light, bodySize: 10.2 });
  addCard(slide, 4.82, 6.1, 3.85, 0.92, 'Takeaway 2', 'FlexUlysses reaches a balance ratio of 1.0 without paying fixed communication on all sequences.', { fill: COLORS.light, bodySize: 10.2 });
  addCard(slide, 8.78, 6.1, 3.85, 0.92, 'Takeaway 3', 'In this comparison, FlexUlysses improves throughput by 1.50× over the veRL baseline.', { fill: COLORS.purpleLite, border: 'C4B5FD', titleColor: COLORS.purple, bodySize: 10.2 });
  finalizeSlide(slide, 10);
}

// Slide 11
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'Ablation Study', 'ShadowLoader and FlexUlysses are complementary.');
  addCard(slide, 0.74, 1.45, 4.25, 1.35, 'ShadowLoader alone', '84.09× data-loading throughput\n4.68× end-to-end throughput\n5.35× lower step time', { fill: COLORS.greenLite, border: 'A7F3D0', titleColor: COLORS.green, bodySize: 14.5 });
  addCard(slide, 0.74, 3.0, 4.25, 1.35, 'FlexUlysses alone', '2.01× rollout throughput\n1.28× training throughput\nOnly 1.17× end-to-end when data loading still dominates', { fill: COLORS.blueLite, border: 'BFDBFE', titleColor: COLORS.blue, bodySize: 14.2 });
  addCard(slide, 0.74, 4.55, 4.25, 1.48, 'Both together = FlexRL', '117.42× data-loading throughput\n7.67× end-to-end throughput\n7.68× reduction in overall step time', { fill: COLORS.purpleLite, border: 'C4B5FD', titleColor: COLORS.purple, bodySize: 14.5 });
  const abl = ASSET('flexrl_ablation.png');
  slide.addImage({ path: abl, ...imageSizingContain(abl, 5.32, 1.5, 7.2, 4.8) });
  addCaption(slide, 'Paper figure: stage-wise throughput and step-time breakdown under the ablation study.', 5.68, 6.28, 6.5);
  finalizeSlide(slide, 11);
}

// Slide 12
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'Takeaways', 'Why this paper matters as a systems contribution for multimodal RL.');
  addCard(slide, 0.78, 1.5, 12.0, 1.25, '1. Diagnose the whole pipeline, not just one kernel',
    'The paper shows that VLM RL is bottlenecked by both multimodal data handling and execution imbalance; solving only one of them leaves the other as the dominant straggler.',
    { fill: COLORS.light, bodySize: 14 }
  );
  addCard(slide, 0.78, 3.0, 12.0, 1.25, '2. Co-design data movement and execution planning',
    'ShadowLoader and FlexUlysses are coupled by metadata, slice-aware loading, hierarchical placement, and overlapped execution—this is what turns isolated ideas into an end-to-end system.',
    { fill: COLORS.light, bodySize: 14 }
  );
  addCard(slide, 0.78, 4.5, 12.0, 1.25, '3. Real gains on real clusters',
    'Across 7B/32B VLMs and two 128-GPU clusters, FlexRL improves throughput by up to 8.47× and removes the controller-side bottleneck that makes multimodal RL hard to scale in practice.',
    { fill: COLORS.light, bodySize: 14 }
  );
  addMetricCard(slide, 3.55, 6.18, 6.25, 0.82, 'Bottom line', 'FlexRL makes large-scale VLM RL training practical by balancing both data and compute.', '', {
    fill: COLORS.blueLite,
    border: 'BFDBFE',
    valueColor: COLORS.text,
    valueSize: 13.5,
  });
  finalizeSlide(slide, 12);
}

async function main() {
  const out = path.join(__dirname, 'paper_talk_flexrl_iclr26_dark.pptx');
  await pptx.writeFile({ fileName: out });
  execFileSync('python3', [
    '-c',
    `
import os, re, zipfile, tempfile
from pathlib import Path

pptx_path = Path(${JSON.stringify(path.join(__dirname, 'paper_talk_flexrl_iclr26_dark.pptx'))})
tmp_path = pptx_path.with_suffix('.tmp.pptx')

with zipfile.ZipFile(pptx_path, 'r') as zin:
    names = set(zin.namelist())
    actual_slide_masters = {
        f'/' + name
        for name in names
        if re.fullmatch(r'ppt/slideMasters/slideMaster\\d+\\.xml', name)
    }
    content_types = zin.read('[Content_Types].xml').decode('utf-8')
    content_types = re.sub(
        r'<Override PartName=\"(/ppt/slideMasters/slideMaster\\d+\\.xml)\" ContentType=\"application/vnd.openxmlformats-officedocument.presentationml.slideMaster\\+xml\"\\s*/>',
        lambda m: m.group(0) if m.group(1) in actual_slide_masters else '',
        content_types,
    )

    with zipfile.ZipFile(tmp_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == '[Content_Types].xml':
                data = content_types.encode('utf-8')
            zout.writestr(info, data)

os.replace(tmp_path, pptx_path)
`,
  ]);
  console.log(out);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
