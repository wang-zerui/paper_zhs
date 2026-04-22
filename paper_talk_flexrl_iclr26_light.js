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
pptx.subject = 'FlexRL ICLR 2026 paper talk - light version';
pptx.title = 'FlexRL: Scaling VLM RL Training via Efficient Load Balancing';
pptx.lang = 'en-US';
pptx.theme = {
  headFontFace: 'Times New Roman',
  bodyFontFace: 'Arial',
  lang: 'en-US',
};
pptx.defineLayout({ name: 'WIDE_SAFE', width: 13.333, height: 7.5 });
pptx.layout = 'WIDE_SAFE';

const W = 13.333;
const H = 7.5;
const M = 0.52;
const COLORS = {
  text: '111111',
  subtext: '222222',
  muted: '6B6B6B',
  border: 'B8B8B8',
  light: 'FFFFFF',
  lighter: 'F6F6F6',
  blue: '111111',
  blueLite: 'FAFAFA',
  green: '111111',
  greenLite: 'FAFAFA',
  red: '111111',
  redLite: 'FAFAFA',
  amber: '111111',
  amberLite: 'FAFAFA',
  purple: '111111',
  purpleLite: 'FAFAFA',
  slate: 'EFEFEF',
};

const TYPE = {
  slideTitle: 26.5,
  coverTitle: 27,
  cardTitle: 15.5,
  sectionLead: 14.5,
  body: 11.5,
  bodySmall: 10.6,
  bullet: 14,
  metric: 28,
  metricMid: 21,
  metricSmall: 15.5,
  conclusion: 16.5,
};

const ASSET = (name) =>
  path.join(__dirname, '.cache', 'flexrl_talk_build', 'assets', name);

function addSlideBase(slide, title, subtitle = '') {
  slide.background = { color: 'FFFFFF' };
  slide.addText(title, {
    x: 0.82,
    y: 0.48,
    w: 10.4,
    h: 0.42,
    fontFace: 'Times New Roman',
    fontSize: TYPE.slideTitle,
    bold: true,
    color: COLORS.text,
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.82,
    y: 1.06,
    w: 11.65,
    h: 0.016,
    line: { color: COLORS.text, transparency: 100 },
    fill: { color: COLORS.text },
  });
}

function addFooter(slide, pageNum) {
  slide.addText(String(pageNum), {
    x: 12.55,
    y: 7.13,
    w: 0.25,
    h: 0.14,
    fontFace: 'Arial',
    fontSize: 8.5,
    color: COLORS.muted,
    align: 'right',
    margin: 0,
  });
}

function addCard(slide, x, y, w, h, title, body, opts = {}) {
  slide.addText(title, {
    x: x + 0.02,
    y: y + 0.02,
    w: w - 0.04,
    h: 0.24,
    fontFace: 'Times New Roman',
    fontSize: opts.titleSize || TYPE.cardTitle,
    bold: true,
    color: COLORS.text,
    margin: 0,
  });
  slide.addText(body, {
    x: x + 0.02,
    y: y + 0.34,
    w: w - 0.04,
    h: h - 0.38,
    fontFace: 'Arial',
    fontSize: opts.bodySize || TYPE.body,
    color: COLORS.subtext,
    margin: 0,
    valign: 'top',
    breakLine: false,
  });
}

function addMetricCard(slide, x, y, w, h, label, value, note, opts = {}) {
  slide.addText(label, {
    x: x,
    y: y + 0.02,
    w,
    h: 0.18,
    fontFace: 'Arial',
    fontSize: TYPE.bodySmall,
    bold: true,
    color: COLORS.muted,
    margin: 0,
    align: 'center',
  });
  slide.addText(value, {
    x: x,
    y: y + 0.38,
    w,
    h: 0.55,
    fontFace: 'Times New Roman',
    fontSize: opts.valueSize || TYPE.metric,
    bold: true,
    color: COLORS.text,
    align: 'center',
    margin: 0,
  });
  const noteHeight = h - 1.28;
  if (note && noteHeight > 0.08) {
    slide.addText(note, {
      x,
      y: y + 1.0,
      w,
      h: noteHeight,
      fontFace: 'Arial',
      fontSize: TYPE.bodySmall,
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
    fontSize: opts.fontSize || TYPE.bullet,
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
    line: { color: COLORS.border, pt: 0.8 },
    fill: { color: 'FFFFFF' },
  });
  slide.addText(text, {
    x,
    y: y + 0.08,
    w,
    h: 0.14,
    fontFace: 'Arial',
    fontSize: TYPE.bodySmall,
    color: COLORS.text,
    bold: true,
    align: 'center',
    margin: 0,
  });
}

function addCaption(slide, text, x, y, w) {
  return;
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
  slide.background = { color: 'FFFFFF' };
  slide.addText('FlexRL:\nScaling VLM RL Training via Efficient Load Balancing', {
    x: 1.18,
    y: 1.58,
    w: 10.95,
    h: 1.0,
    fontFace: 'Times New Roman',
    fontSize: TYPE.coverTitle,
    bold: true,
    color: COLORS.text,
    margin: 0,
    align: 'center',
    valign: 'mid',
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 3.25,
    y: 2.72,
    w: 6.83,
    h: 0.02,
    line: { color: COLORS.text, transparency: 100 },
    fill: { color: COLORS.text },
  });
  slide.addText('Zerui Wang, Qinghao Hu, Chang Chen, Jiecheng Zhou,\nHaojie Duanmu, Xingcheng Zhang, Peng Sun, Dahua Lin', {
    x: 1.15,
    y: 3.0,
    w: 11.0,
    h: 0.44,
    fontFace: 'Arial',
    fontSize: TYPE.bodySmall,
    color: COLORS.subtext,
    margin: 0,
    align: 'center',
  });
  slide.addText('Shanghai Jiao Tong University · Shanghai AI Lab · MIT · USTC · Peking University · CUHK', {
    x: 1.1,
    y: 3.48,
    w: 11.1,
    h: 0.28,
    fontFace: 'Arial',
    fontSize: 10,
    color: COLORS.muted,
    margin: 0,
    align: 'center',
  });
  slide.addText('ShadowLoader for data loading.\nFlexUlysses for execution balancing.', {
    x: 2.35,
    y: 4.52,
    w: 8.65,
    h: 0.54,
    fontFace: 'Arial',
    fontSize: TYPE.sectionLead,
    color: COLORS.subtext,
    margin: 0,
    align: 'center',
  });
  finalizeSlide(slide, 1);
}

// Slide 2
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'Executive Summary', 'What the paper diagnoses, builds, and demonstrates end-to-end.');
  addCard(slide, 0.65, 1.35, 3.95, 4.95, '1. Problem',
    'Two bottlenecks dominate VLM RL:\n\n• data loading is centralized on one controller\n• heterogeneous batches create compute / memory imbalance across GPUs\n• fixing only one side is not enough',
    { fill: COLORS.light }
  );
  addCard(slide, 4.69, 1.35, 3.95, 4.95, '2. System',
    'FlexRL has two pieces:\n\n• ShadowLoader: metadata-only scheduling on the controller; workers do preprocessing\n• FlexUlysses: adaptive sharding, hierarchical device groups, and overlapped execution',
    { fill: COLORS.light }
  );
  addCard(slide, 8.73, 1.35, 3.95, 4.95, '3. Impact',
    'On 7B / 32B models and two 128-GPU clusters:\n\n• up to 8.47× end-to-end speedup\n• 117.42× data-loading speedup\n• balance ratio reaches 1.0 in the Ulysses comparison',
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
  addBullet(slide, 'Image/video decoding, frame sampling, and preprocessing are CPU- and I/O-heavy.', 0.95, 2.0, 5.1, 0.54, { fontSize: TYPE.bullet, color: COLORS.subtext });
  addBullet(slide, 'In the veRL multimodal baseline, data loading takes 57.1% of the iteration time.', 0.95, 2.64, 5.1, 0.54, { fontSize: TYPE.bullet, color: COLORS.subtext });
  addBullet(slide, 'As batch size grows, the controller becomes the single straggler and can hit host-memory OOM.', 0.95, 3.28, 5.1, 0.72, { fontSize: TYPE.bullet, color: COLORS.subtext });
  addMetricCard(slide, 1.05, 4.48, 2.35, 1.42, 'Observed in baseline', '57.1%', 'of step time spent on data loading', {
    fill: 'FFFFFF',
    border: 'A7F3D0',
    valueColor: COLORS.green,
    valueSize: TYPE.metricMid,
  });
  addMetricCard(slide, 3.65, 4.48, 2.35, 1.42, 'Failure mode', 'OOM', 'Controller-side CPU memory becomes the bottleneck', {
    fill: 'FFFFFF',
    border: 'A7F3D0',
    valueColor: COLORS.red,
    valueSize: TYPE.metricMid,
  });

  addCard(slide, 6.85, 1.34, 5.8, 4.95, 'Bottleneck B — Cross-GPU execution imbalance', '', {
    fill: COLORS.blueLite,
    border: 'BFDBFE',
    titleColor: COLORS.blue,
  });
  addBullet(slide, 'Attention compute grows quadratically with sequence length, while activation memory grows linearly.', 7.12, 2.0, 5.1, 0.72, { fontSize: TYPE.bullet, color: COLORS.subtext });
  addBullet(slide, 'Text length is a poor proxy for visual cost: image counts and video frame counts change both compute and memory.', 7.12, 2.78, 5.1, 0.76, { fontSize: TYPE.bullet, color: COLORS.subtext });
  addBullet(slide, 'Length-only bucketing can still leave one DP rank as the straggler—or even OOM on long contexts.', 7.12, 3.62, 5.1, 0.76, { fontSize: TYPE.bullet, color: COLORS.subtext });
  addMetricCard(slide, 7.25, 4.48, 2.35, 1.42, 'Skew source', 'Mixed modalities', 'short image-text + long video-text in the same RL batch', {
    fill: 'FFFFFF',
    border: 'BFDBFE',
    valueColor: COLORS.blue,
    valueSize: TYPE.metricSmall,
  });
  addMetricCard(slide, 9.85, 4.48, 2.35, 1.42, 'Why prior work falls short', 'Bucketing ≠ balancing', 'fixed parallelism or coarse buckets cannot eliminate stragglers', {
    fill: 'FFFFFF',
    border: 'BFDBFE',
    valueColor: COLORS.red,
    valueSize: TYPE.metricSmall,
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
    fontSize: TYPE.cardTitle,
    bold: true,
    color: COLORS.text,
    margin: 0,
  });
  addBullet(slide, 'ShadowLoader decentralizes multimodal preprocessing and keeps only lightweight metadata on the controller.', 0.8, 1.88, 3.65, 0.78, { fontSize: TYPE.bullet, color: COLORS.subtext });
  addBullet(slide, 'FlexUlysses shards only the sequences that need it, balancing both compute and memory at sub-sequence granularity.', 0.8, 2.78, 3.65, 0.92, { fontSize: TYPE.bullet, color: COLORS.subtext });
  addBullet(slide, 'The two components are co-designed so sharding decisions can guide slice-aware data loading and reduce transfer volume.', 0.8, 3.88, 3.65, 0.94, { fontSize: TYPE.bullet, color: COLORS.subtext });
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
    fontSize: TYPE.cardTitle,
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
    slide.addText(b[0], {
      x: x + 0.15,
      y: flowY + 0.18,
      w: boxW - 0.3,
      h: 0.35,
      fontFace: 'Arial',
      fontSize: 14.5,
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
      fontSize: TYPE.bodySmall,
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
        fontSize: 16,
        bold: true,
        color: COLORS.muted,
        margin: 0,
        align: 'center',
      });
    }
  });

  addCard(slide, 0.8, 4.1, 5.55, 1.7, 'Key mechanisms',
    '• keep only metadata on the controller\n• overlap preprocessing / transfer with GPU work\n• fetch only the slices needed after sharding is decided',
    { fill: COLORS.light, bodySize: TYPE.body }
  );

  addMetricCard(slide, 6.72, 4.3, 2.55, 1.2, 'ShadowLoader', '84.09×', '', {
    fill: COLORS.greenLite,
    border: 'A7F3D0',
    valueColor: COLORS.green,
  });
  addMetricCard(slide, 9.55, 4.3, 2.55, 1.2, 'ShadowLoader + FlexUlysses', '117.42×', '', {
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
    fill: COLORS.light, bodySize: TYPE.bodySmall, titleSize: 14.8
  });
  addCard(slide, 4.72, 6.28, 3.9, 0.78, 'Observation 2', 'For longer contexts, fixed buckets may still OOM or leave severe attention imbalance.', {
    fill: COLORS.light, bodySize: TYPE.bodySmall, titleSize: 14.8
  });
  addCard(slide, 8.69, 6.28, 3.9, 0.78, 'Key insight', 'Use Ulysses chunks as scheduling units, and shard sequences only as much as needed.', {
    fill: COLORS.purpleLite, border: 'C4B5FD', titleColor: COLORS.purple, bodySize: TYPE.bodySmall, titleSize: 14.8
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
  slide.addText('Vision tower balancing is handled separately by evenly distributing images and video frames across GPUs.', {
    x: 3.18,
    y: 6.4,
    w: 7.0,
    h: 0.24,
    fontFace: 'Arial',
    fontSize: TYPE.body,
    italic: true,
    color: COLORS.muted,
    margin: 0,
    align: 'center',
  });
  finalizeSlide(slide, 7);
}

// Slide 8
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'Evaluation Setup', 'Large-scale experiments cover two hardware platforms, two model scales, and three workload mixes.');
  addCard(slide, 0.72, 1.42, 3.9, 4.95, 'Hardware',
    '• two 128-GPU clusters\n• H800 and H200\n• NVLink / NVSwitch intra-node\n• RoCEv2 RDMA inter-node',
    { fill: COLORS.light }
  );
  addCard(slide, 4.74, 1.42, 3.9, 4.95, 'Models & training',
    '• MiMo-VL-7B-RL and Qwen2.5-VL-32B\n• GRPO\n• response length = 1024\n• p_max = 8',
    { fill: COLORS.light }
  );
  addCard(slide, 8.76, 1.42, 3.9, 4.95, 'Datasets & baselines',
    '• Geo3K, NExTQA, LongVILA-Reason\n• image-heavy / video-heavy / only-video\n• baselines: veRL+Bucketing and fixed-degree Ulysses-SP',
    { fill: COLORS.light }
  );
  finalizeSlide(slide, 8);
}

// Slide 9
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'Main Results', 'Peak end-to-end speedup reported in the paper, by workload mix.');
  addMetricCard(slide, 0.88, 1.7, 3.65, 2.2, 'Image-heavy', '7.35×', '5 : 2 : 1 mix', {
    fill: COLORS.blueLite,
    border: 'BFDBFE',
    valueColor: COLORS.blue,
    valueSize: TYPE.metric,
  });
  addMetricCard(slide, 4.86, 1.7, 3.65, 2.2, 'Video-heavy', '5.35×', '1 : 2 : 5 mix', {
    fill: COLORS.greenLite,
    border: 'A7F3D0',
    valueColor: COLORS.green,
    valueSize: TYPE.metric,
  });
  addMetricCard(slide, 8.84, 1.7, 3.65, 2.2, 'Only-video', '8.47×', 'LongVILA-Reason only', {
    fill: COLORS.redLite,
    border: 'FCA5A5',
    valueColor: COLORS.red,
    valueSize: TYPE.metric,
  });
  slide.addText('Largest gains appear when multimodal skew is strongest.', {
    x: 0.88,
    y: 5.35,
    w: 12.0,
    h: 0.22,
    fontFace: 'Arial',
    fontSize: 12.2,
    color: COLORS.subtext,
    margin: 0,
    align: 'center',
  });
  finalizeSlide(slide, 9);
}

// Slide 10
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'Comparison with Fixed-Degree Ulysses-SP', 'Adaptive sharding outperforms fixed SP because it avoids over-sharding short sequences.');
  const comm = ASSET('comm_overhead_h200_detailed_v4.png');
  slide.addImage({ path: comm, ...imageSizingContain(comm, 0.72, 1.32, 12.0, 4.55) });
  addCaption(slide, 'Paper figure: fixed-degree Ulysses-SP vs. FlexUlysses on per-stage time, throughput, and balance ratio.', 1.0, 5.9, 11.4);
  addCard(slide, 0.86, 6.08, 3.85, 0.78, 'Takeaway 1', 'Higher fixed SP improves balance, but communication quickly dominates.', { fill: COLORS.light, bodySize: TYPE.bodySmall, titleSize: 14.8 });
  addCard(slide, 4.82, 6.08, 3.85, 0.78, 'Takeaway 2', 'FlexUlysses reaches balance ratio 1.0 without fixed communication on all sequences.', { fill: COLORS.light, bodySize: TYPE.bodySmall, titleSize: 14.8 });
  addCard(slide, 8.78, 6.08, 3.85, 0.78, 'Takeaway 3', 'Throughput is 1.50× higher than the veRL baseline in this comparison.', { fill: COLORS.purpleLite, border: 'C4B5FD', titleColor: COLORS.purple, bodySize: TYPE.bodySmall, titleSize: 14.8 });
  finalizeSlide(slide, 10);
}

// Slide 11
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'Ablation Study', 'ShadowLoader and FlexUlysses are complementary.');
  addCard(slide, 0.74, 1.45, 4.25, 1.22, 'ShadowLoader alone', '84.09× data loading\n4.68× end-to-end\n5.35× lower step time', { fill: COLORS.greenLite, border: 'A7F3D0', titleColor: COLORS.green, bodySize: 13.6, titleSize: 15.2 });
  addCard(slide, 0.74, 2.9, 4.25, 1.22, 'FlexUlysses alone', '2.01× rollout\n1.28× training\n1.17× end-to-end when data loading still dominates', { fill: COLORS.blueLite, border: 'BFDBFE', titleColor: COLORS.blue, bodySize: 13.2, titleSize: 15.2 });
  addCard(slide, 0.74, 4.35, 4.25, 1.28, 'Both together = FlexRL', '117.42× data loading\n7.67× end-to-end\n7.68× lower overall step time', { fill: COLORS.purpleLite, border: 'C4B5FD', titleColor: COLORS.purple, bodySize: 13.6, titleSize: 15.2 });
  const abl = ASSET('flexrl_ablation.png');
  slide.addImage({ path: abl, ...imageSizingContain(abl, 5.32, 1.5, 7.2, 4.8) });
  addCaption(slide, 'Paper figure: stage-wise throughput and step-time breakdown under the ablation study.', 5.68, 6.28, 6.5);
  finalizeSlide(slide, 11);
}

// Slide 12
{
  const slide = pptx.addSlide();
  addSlideBase(slide, 'Takeaways', 'Why this paper matters as a systems contribution for multimodal RL.');
  addCard(slide, 0.78, 1.5, 12.0, 1.0, '1. Diagnose the whole pipeline',
    'VLM RL is bottlenecked by both multimodal data handling and execution imbalance.',
    { fill: COLORS.light, bodySize: 13.4, titleSize: 15.2 }
  );
  addCard(slide, 0.78, 2.9, 12.0, 1.0, '2. Co-design loading and execution',
    'ShadowLoader and FlexUlysses are coupled through metadata, slice-aware loading, and hierarchical placement.',
    { fill: COLORS.light, bodySize: 13.4, titleSize: 15.2 }
  );
  addCard(slide, 0.78, 4.3, 12.0, 1.0, '3. Real gains on real clusters',
    'Across 7B/32B VLMs and two 128-GPU clusters, throughput improves by up to 8.47×.',
    { fill: COLORS.light, bodySize: 13.4, titleSize: 15.2 }
  );
  slide.addText('FlexRL makes large-scale VLM RL training practical by balancing both data and compute.', {
    x: 1.2,
    y: 6.15,
    w: 10.9,
    h: 0.28,
    fontFace: 'Times New Roman',
    fontSize: TYPE.conclusion,
    bold: true,
    color: COLORS.text,
    align: 'center',
    margin: 0,
  });
  finalizeSlide(slide, 12);
}

async function main() {
  const out = path.join(__dirname, 'paper_talk_flexrl_iclr26_light.pptx');
  await pptx.writeFile({ fileName: out });
  execFileSync('python3', [
    '-c',
    `
import os, re, zipfile, tempfile
from pathlib import Path

pptx_path = Path(${JSON.stringify(path.join(__dirname, 'paper_talk_flexrl_iclr26_light.pptx'))})
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
